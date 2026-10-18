# MOSS-Image Prompt Enhancer — Skill Asset

本目录与官方仓库保持同步（原样复制，未做改写）：

- Source: https://github.com/OpenMOSS/MOSS-Image/tree/main/skills/moss-image-prompt-enhancer
- License: Apache-2.0 (OpenMOSS/MOSS-Image)
- 文件：
  - `SKILL.md` — 官方原版（含 frontmatter，未修改）
  - `references/layout.md` — 官方原版（未修改）

## 同步方式

官方更新时，直接覆盖本目录下的 `SKILL.md` 和 `references/layout.md` 即可生效
（节点每次执行都会重新读取文件，无需重启 ComfyUI、无需改代码）。

也可以运行插件自带的同步脚本一键拉取官方原样（sparse-checkout + 字节校验，
保留本目录下的 SOURCE.md 等本地文件）：

```powershell
python scripts\sync_official_skills.py --skill moss --dry-run   # 先看差异
python scripts\sync_official_skills.py --skill moss             # 实际同步
```

## 加载机制

插件加载器会检测 skill 目录下的 `references/` 子目录：
存在时，将 `SKILL.md` 与 `references/` 下所有文件拼接为完整的系统提示词
（这样官方 SKILL.md 中 "Read references/layout.md" 的指令对 LLM 可见）。

> 注：官方 SKILL.md 面向具备文件系统/脚本执行能力的 agent，包含运行
> `scripts/compile_prompt.py` 的说明。本插件场景下 LLM 仅获得提示词文本，
> 脚本调用部分不可执行，但保留原样以维持与官方同步；Layout 的 JSON 规则
> 完整可见，可直接按规范输出。
