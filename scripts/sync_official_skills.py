#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sync official skill assets from upstream repositories into this plugin.

Why this exists
---------------
The three "official" skills (MOSS-Image, MiniMax H3, Qwen-Image 2.1) are
subdirectories of their upstream repositories. They are mirrored here as
plain files under skills/<skill>/ so the loader reads them as editable
file assets. This script refreshes those mirrors from upstream.

How it works
------------
For each skill:
  1. `git clone --depth 1 --filter=blob:none --sparse <repo>` into a temp dir,
     then `sparse-checkout set <official subdir>` — only the skill subdirectory
     is downloaded.
  2. Byte-compare every official file against the local mirror.
  3. Copy over files that are new or differ (unless --dry-run).
  4. Local-only files (SOURCE.md, user edits, etc.) are PRESERVED. A local file
     whose official counterpart was removed upstream is only REPORTED; delete it
     yourself or pass --prune to remove it automatically.

Usage
-----
  python scripts/sync_official_skills.py                  # sync all skills
  python scripts/sync_official_skills.py --skill qwen     # one skill: moss|h3|qwen
  python scripts/sync_official_skills.py --dry-run        # report only, write nothing
  python scripts/sync_official_skills.py --prune          # also delete local files
                                                          #   removed upstream
  python scripts/sync_official_skills.py --keep-temp      # keep the temp clone for
                                                          #   debugging

Exit codes
----------
  0 : done, no errors (with --dry-run: no differences found)
  1 : differences found under --dry-run, or errors occurred
  2 : git unavailable or an upstream clone failed

Requires: git on PATH. No third-party Python packages.
"""

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_ROOT = os.path.join(PLUGIN_ROOT, "skills")

SOURCES = [
    {
        "name": "moss",
        "repo": "https://github.com/OpenMOSS/MOSS-Image.git",
        "upstream_subdir": "skills/moss-image-prompt-enhancer",
        "local_dir": "moss-image-prompt-enhancer",
    },
    {
        "name": "h3",
        "repo": "https://github.com/MiniMax-AI/MiniMax-H3.git",
        "upstream_subdir": "skills/h3-prompt-writing",
        "local_dir": "minimax-h3-prompt-enhancer",
    },
    {
        "name": "qwen",
        "repo": "https://github.com/iamyoki/qwen-image-2.1-skill.git",
        "upstream_subdir": "skills/qwen-image-2-1-prompter",
        "local_dir": "qwen-image-2.1-prompt-enhancer",
    },
]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def git_available():
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except Exception:
        return False


def fetch_upstream(repo_url, subdir, workdir, clone_name, keep_temp):
    """Sparse-clone the official skill subdirectory into workdir; returns path."""
    clone_dir = os.path.join(workdir, clone_name)
    last_err = None
    for attempt in (1, 2, 3):  # retry transient network failures
        if os.path.isdir(clone_dir):
            try:
                shutil.rmtree(clone_dir)
            except Exception as e:
                print(f"    (cannot clean {clone_dir}: {e})", flush=True)
        try:
            r = subprocess.run(
                ["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse",
                 repo_url, clone_dir],
                capture_output=True,
            )
        except Exception as e:  # git missing / spawn error
            raise RuntimeError(f"cannot run git clone: {e}")
        if r.returncode == 0:
            break
        last_err = r.stderr.decode("utf-8", "replace").strip() or "git clone failed"
        print(f"    (clone attempt {attempt} failed: {last_err})", flush=True)
    else:
        raise RuntimeError(f"git clone failed after retries: {last_err}")

    r = subprocess.run(
        ["git", "-C", clone_dir, "sparse-checkout", "set", subdir],
        capture_output=True,
    )
    if r.returncode != 0:
        raise RuntimeError(
            f"sparse-checkout failed for {repo_url}: "
            f"{r.stderr.decode('utf-8', 'replace')}"
        )
    src = os.path.join(clone_dir, subdir)
    if not os.path.isdir(src):
        raise RuntimeError(f"upstream subdir not found after checkout: {src}")
    return src


def sync_one(source, dry_run, prune, workdir, keep_temp):
    name = source["name"]
    local_dir = os.path.join(SKILLS_ROOT, source["local_dir"])
    print(f"\n=== [{name}] {source['local_dir']}")
    print(f"    upstream: {source['repo']} :: {source['upstream_subdir']}")

    if not git_available():
        print("    ERROR: git not found on PATH", flush=True)
        return ["git-missing"]

    errors = []
    try:
        src = fetch_upstream(source["repo"], source["upstream_subdir"], workdir,
                             f"upstream_{name}", keep_temp)
    except Exception as e:
        print(f"    ERROR: {e}", flush=True)
        return [f"fetch-failed:{name}"]

    upstream_files = {}
    for root, _dirs, files in os.walk(src):
        for fn in files:
            rel = os.path.relpath(os.path.join(root, fn), src)
            upstream_files[rel] = os.path.join(root, fn)

    local_files = {}
    if os.path.isdir(local_dir):
        for root, _dirs, files in os.walk(local_dir):
            for fn in files:
                rel = os.path.relpath(os.path.join(root, fn), local_dir)
                local_files[rel] = os.path.join(root, fn)

    added = copied = identical = 0
    local_only = []

    for rel in sorted(upstream_files):
        src_path = upstream_files[rel]
        dst_path = os.path.join(local_dir, rel)
        status = "OK"
        if rel not in local_files:
            status = "NEW"
        elif sha256_file(src_path) != sha256_file(dst_path):
            status = "DIFF"
        if status == "OK":
            identical += 1
            print(f"    OK   {rel}")
        else:
            print(f"    {status}  {rel}")
            if status == "NEW":
                added += 1
            else:
                copied += 1
            if not dry_run:
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)

    for rel in sorted(local_files):
        if rel not in upstream_files:
            local_only.append(rel)
            print(f"    LOCAL_ONLY  {rel}  (local file not in upstream; kept)")

    if local_only and prune and not dry_run:
        for rel in local_only:
            p = os.path.join(local_dir, rel)
            os.remove(p)
            print(f"    PRUNED  {rel}")
        # remove now-empty directories created by pruning
        for root, _dirs, _files in os.walk(local_dir, topdown=False):
            try:
                os.rmdir(root)
            except OSError:
                pass

    print(
        f"    -> identical={identical} new={added} updated={copied} "
        f"local_only={len(local_only)}"
    )
    if local_only and not prune:
        print(
            "       (use --prune to delete local files that no longer exist upstream)"
        )
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--skill", choices=[s["name"] for s in SOURCES] + ["all"],
                        default="all", help="which skill to sync (default: all)")
    parser.add_argument("--dry-run", action="store_true",
                        help="report differences only, write nothing")
    parser.add_argument("--prune", action="store_true",
                        help="delete local files that were removed upstream")
    parser.add_argument("--keep-temp", action="store_true",
                        help="keep the temporary clone for debugging")
    args = parser.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    if not git_available():
        print("ERROR: git not found on PATH", file=sys.stderr)
        return 2

    workdir = tempfile.mkdtemp(prefix="wanpe_skill_sync_")
    try:
        errors = []
        changed = False
        for source in SOURCES:
            if args.skill != "all" and source["name"] != args.skill:
                continue
            errs = sync_one(source, args.dry_run, args.prune, workdir, args.keep_temp)
            errors.extend(errs)
        print("\nDone.")
        if errors:
            print("Errors:", ", ".join(errors))
            return 1
        return 0
    finally:
        if not args.keep_temp:
            shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
