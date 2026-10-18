# Qwen-Image 2.1 Prompt Enhancer — Skill Asset

本目录与参考仓库保持同步（原样复制，未做改写）：

- Source: https://github.com/iamyoki/qwen-image-2.1-skill — skill `qwen-image-2-1-prompter`
- License: Apache-2.0（iamyoki/qwen-image-2.1-skill，官方 Alibaba Qwen-Image-2.1
  Prompt Rewriting System Specification 的社区封装）
- 文件（与参考仓库目录原样一致）：
  - `SKILL.md` — 参考仓库原版（含 frontmatter，未修改）
  - `references/t2i_rules.md` — 原版（文生图 8 步规则）
  - `references/edit_rules.md` — 原版（图编辑/多图合成规则）
  - `references/cheat_sheet.md` — 原版（词汇与参数速查）
  - `scripts/validate_prompt.py` — 原版（离线校验工具，仅开发者测试用，正常使用不执行）

## 同步方式

上游更新时，直接覆盖本目录下的 `SKILL.md` 和 `references/` 下文件即可生效
（节点每次执行都会重新读取文件，无需重启 ComfyUI、无需改代码）。

也可以运行插件自带的同步脚本一键拉取官方原样（sparse-checkout + 字节校验，
保留本目录下的 SOURCE.md 等本地文件）：

```powershell
python scripts\sync_official_skills.py --skill qwen --dry-run   # 先看差异
python scripts\sync_official_skills.py --skill qwen             # 实际同步
```

## 加载机制

插件加载器检测到 `references/` 子目录后，自动将 `SKILL.md` 与 references 下所有
文件拼接为完整系统提示词（带 `# Reference: <fn> (inlined from ...)` 分区标记），
满足 SKILL.md 中 "Read references/t2i_rules.md" / "edit_rules.md" /
"cheat_sheet.md" 的指令。
