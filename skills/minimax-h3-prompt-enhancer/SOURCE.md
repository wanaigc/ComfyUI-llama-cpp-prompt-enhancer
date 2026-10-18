# MiniMax H3 Prompt Enhancer — Skill Asset

本目录与官方仓库保持同步（原样复制，未做改写）：

- Source: https://github.com/MiniMax-AI/MiniMax-H3/tree/main/skills/h3-prompt-writing
- License: MiniMax H3 Community License（官方）
- 文件（与官方目录原样一致）：
  - `SKILL.md` — 官方原版（含 frontmatter，未修改）
  - `references/base-en.txt` — 官方原版（T2VA/I2VA/FL2VA/L2VA 基础模式指南）
  - `references/ref-en.txt` — 官方原版（Ref2VA 全参考模式指南）
  - `agents/openai.yaml` — 官方原版（ChatGPT/Codex UI 元数据，纯元数据不参与提示词）

## 同步方式

官方更新时，直接覆盖本目录下的 `SKILL.md` 和 `references/` 下文件即可生效
（节点每次执行都会重新读取文件，无需重启 ComfyUI、无需改代码）。

也可以运行插件自带的同步脚本一键拉取官方原样（sparse-checkout + 字节校验，
保留本目录下的 SOURCE.md 等本地文件）：

```powershell
python scripts\sync_official_skills.py --skill h3 --dry-run   # 先看差异
python scripts\sync_official_skills.py --skill h3             # 实际同步
```

## 加载机制

插件加载器检测到 `references/` 子目录后，自动将 `SKILL.md` 与 references 下所有
文件拼接为完整系统提示词（带 `# Reference: <fn> (inlined from ...)` 分区标记），
满足官方 SKILL.md 中 "read references/base-en.txt" / "read references/ref-en.txt"
的指令。

> 注：官方 SKILL.md 面向具备文件读取能力的 agent，拼接后的提示词文本中 base-en.txt
> 与 ref-en.txt 的完整规范均对 LLM 可见。
