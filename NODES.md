# ComfyUI-llama-cpp-prompt-enhancer — 节点清单

> 生成日期：2026-10-18（基于当前 `nodes.py` 实际注册表）
> 仓库：https://github.com/wanaigc/ComfyUI-llama-cpp-prompt-enhancer
> 说明：本插件 fork 自 `lihaoyun6/ComfyUI-llama-cpp_vlm`，全部节点以 `wanaigc_` 前缀注册，
> 与同目录并存的原始 `ComfyUI-llama-cpp_vlm` 插件互不冲突；CATEGORY 统一为
> `wanaigc/llama-cpp-vlm`。保留原生 VLM 能力，并扩展了提示词增强体系。

---

## 一、节点总览（15 个）

| # | 注册 key | 显示名 | 主要输出 | 功能 |
|---|---|---|---|---|
| 1 | `wanaigc_llama_cpp_model_loader` | Wanaigc Llama-cpp Model Loader | `LLAMACPPMODEL` | 加载 GGUF 模型 + mmproj（VLM），支持自定义绝对路径 |
| 2 | `wanaigc_llama_cpp_instruct_adv` | Wanaigc Llama-cpp Instruct | `output` / `output_list` / `state_uid` | 核心推理节点（文本/VLM 多图/视频） |
| 3 | `wanaigc_llama_cpp_parameters` | Wanaigc Llama-cpp Parameters | `LLAMACPPARAMS` | 采样参数 |
| 4 | `wanaigc_llama_cpp_unload_model` | Wanaigc Llama-cpp Unload Model | `any` | 卸载模型释放显存 |
| 5 | `wanaigc_llama_cpp_clean_states` | Wanaigc Llama-cpp Clean States | `any` | 清理指定/全部对话状态 |
| 6 | `wanaigc_parse_json_node` | Wanaigc Parse JSON | `any/string/int/float/boolean` | 解析 LLM 输出的 JSON |
| 7 | `wanaigc_json_to_bbox` | Wanaigc JSON to BBoxes | `BBOX` / `IMAGE` | JSON → bbox 坐标（支持 Qwen3/2.5-VL 格式） |
| 8 | `wanaigc_bbox_to_segs` | Wanaigc BBoxes to SEGS | `SEGS` | bbox → SEGS（供 Impact Pack 等使用） |
| 9 | `wanaigc_bbox_to_mask` | Wanaigc BBoxes to MASK | `MASK` | bbox → 遮罩 |
| 10 | `wanaigc_bboxes_to_bbox` | Wanaigc BBoxes to BBox | `BBOX` | 按索引提取单组 bbox |
| 11 | `wanaigc_remove_code_block` | Wanaigc Unpack Code Block | `STRING` | 去除输出中的代码块围栏 |
| 12 | `wanaigc_PromptEnhancerPreset` | Wanaigc Prompt Enhancer Preset | `STRING` (system_prompt) | 提示词增强预设（内置 + skill 资产 + 用户预设） |
| 13 | `wanaigc_llama_cpp_save_preset` | Wanaigc Save Prompt Preset | `STRING` (status) | 把系统提示词保存为用户预设文件 |
| 14 | `wanaigc_preset_manager` | Wanaigc Preset Manager | `STRING` / `STRING` | 用户预设管理（load/save/delete/rename + md 编辑） |
| 15 | `wanaigc_llama_cpp_text_encoder` | Wanaigc Llama-cpp Text Encoder (BETA) | `CONDITIONING` | 文本编码（BETA） |

---

## 二、节点详细说明

### 1. Wanaigc Llama-cpp Model Loader（`wanaigc_llama_cpp_model_loader`）
- **输入**
  - `model`：下拉，扫描 `ComfyUI/models/LLM/` 下非 mmproj 的 `.gguf`
  - `mmproj`：下拉，`LLM/` 下含 `mmproj` 的文件（默认 `None`，即纯文本模式）
  - `chat_handler`：VLM 对话处理器下拉（默认 `None`）
  - `n_ctx`：INT，默认 8192（1024–327680）
  - `vram_limit`：INT，默认 -1（GB，-1 不限制）
  - `image_min_tokens` / `image_max_tokens`：INT，默认 0
  - `load_mtp`：BOOLEAN，默认 False
  - `custom_model_path`：STRING，**非空时用绝对路径覆盖 model 下拉**（可加载 `models/LLM/` 之外的任意 .gguf）
  - `custom_mmproj_path`：STRING，**非空时用绝对路径覆盖 mmproj 下拉**
- **输出**：`llama_model`（LLAMACPPMODEL）

### 2. Wanaigc Llama-cpp Instruct（`wanaigc_llama_cpp_instruct_adv`）
- **输入**
  - `llama_model`：来自 Loader
  - `preset_prompt`：内置预设下拉（带 `*` 的预设可用 `custom_prompt` 填充占位）
  - `custom_prompt`：STRING（multiline），覆盖或填充预设
  - `system_prompt`：STRING（multiline），可接 Preset 节点的输出
  - `inference_mode`：`one by one` / `images` / `video`
  - `max_frames`：INT，默认 24
- **输出**：`output`（STRING）、`output_list`（STRING）、`state_uid`（INT）

### 3. Wanaigc Llama-cpp Parameters（`wanaigc_llama_cpp_parameters`）
- **输入**：`max_tokens`(1024)、`top_k`(30)、`top_p`(0.9)、`min_p`(0.05)、`typical_p`(1.0)、
  `temperature`(0.8)、`repeat_penalty`(1.0)、`frequency_penalty`(0.0)、`present_penalty`(0.0)、
  `mirostat_mode`(0)、`mirostat_eta`(0.1) 等
- **输出**：`parameters`（LLAMACPPARAMS）

### 4. Wanaigc Llama-cpp Unload Model（`wanaigc_llama_cpp_unload_model`）
- **输入**：`any` → **输出**：`any`（透传；卸载全局模型）

### 5. Wanaigc Llama-cpp Clean States（`wanaigc_llama_cpp_clean_states`）
- **输入**：`any`、`state_uid`（INT，默认 -1；-1 = 清空全部）
- **输出**：`any`

### 6. Wanaigc Parse JSON（`wanaigc_parse_json_node`）
- **输入**：`input`（STRING，forceInput）、可选 `key`、`default`
- **输出**：`any` / `string` / `int` / `float` / `boolean`

### 7. Wanaigc JSON to BBoxes（`wanaigc_json_to_bbox`）
- **输入**：`json`（STRING）、`mode`（simple / Qwen3-VL / Qwen2.5-VL）、`label`（过滤）、可选 `image`
- **输出**：`bboxes`（BBOX）、`image_list`（IMAGE）

### 8. Wanaigc BBoxes to SEGS（`wanaigc_bbox_to_segs`）
- **输入**：`bboxes`、`image`、`dilation`(10)、`feather`(0)
- **输出**：`SEGS`

### 9. Wanaigc BBoxes to MASK（`wanaigc_bbox_to_mask`）
- **输入**：`bboxes`、`image`、`dilation`(10)、`feather`(0)
- **输出**：`mask`（MASK）

### 10. Wanaigc BBoxes to BBox（`wanaigc_bboxes_to_bbox`）
- **输入**：`bboxes`、`image_index`(0)、`bbox_index`(0；999 = 全部)
- **输出**：`bbox`（BBOX）

### 11. Wanaigc Unpack Code Block（`wanaigc_remove_code_block`）
- **输入**：`input`（STRING，forceInput）、可选 `label`
- **输出**：`output`（STRING）

### 12. Wanaigc Prompt Enhancer Preset（`wanaigc_PromptEnhancerPreset`）
- **输入**：`preset`（下拉，见下方「预设来源」）
- **输出**：`system_prompt`（STRING）

### 13. Wanaigc Save Prompt Preset（`wanaigc_llama_cpp_save_preset`）
- **输入**：`preset_name`（STRING，即 `.md` 文件名）、`system_prompt`（STRING，multiline）
- **输出**：`status`（STRING）；保存到 `presets/<preset_name>.md`

### 14. Wanaigc Preset Manager（`wanaigc_preset_manager`）
- **输入**：`preset_name`（用户预设下拉）、`action`（load / save / delete / rename）、
  `new_name`（rename 用）、`system_prompt`（md 编辑框）
- **输出**：`system_prompt`（STRING）、`status`（STRING）
- **说明**：完整管理用户预设，`system_prompt` 编辑框可直接编辑/保存 Markdown 内容

### 15. Wanaigc Llama-cpp Text Encoder (BETA)（`wanaigc_llama_cpp_text_encoder`）
- **输出**：`conditioning`（CONDITIONING）

---

## 三、Prompt Enhancer Preset 下拉来源

下拉 = 18 内置 + 4 skill 资产 + 用户预设（动态合并）：

**内置 18 个**：Qwen-Image [EN]、Qwen-Image [ZH]、Qwen-Image 2512 [EN]、Qwen-Image 2512 [ZH]、
Qwen-Image-Edit、Qwen-Image-Edit 2509、Qwen-Image-Edit 2511、Z-Image Turbo、Flux.2 T2I、
Flux.2 I2I、Wan T2V [EN]、Wan T2V [ZH]、Wan I2V [EN]、Wan I2V [ZH]、Wan I2V Full-Auto [EN]、
Wan I2V Full-Auto [ZH]、Wan FLF2V [EN]、Wan FLF2V [ZH]

**Skill 资产 4 个**（`skills/<skill>/SKILL.md` 文件即资产，官方原样同步，加载时自动拼接 references/）：
- MOSS-Image Prompt Enhancer [官方]（`skills/moss-image-prompt-enhancer/`，OpenMOSS，Apache-2.0）
- MiniMax H3 Prompt Enhancer [官方]（`skills/minimax-h3-prompt-enhancer/`，MiniMax，Community License）
- Qwen-Image 2.1 Prompt Enhancer（`skills/qwen-image-2.1-prompt-enhancer/`，iamyoki 封装，Apache-2.0）
- Krea 2 Prompt Enhancer（`skills/krea2-prompt-enhancer/`，社区版，无官方 skill）

**用户预设**：`presets/<名称>.md`（文件即资产，Preset Manager / Save 节点管理，旧的
`presets/user_presets.json` 已自动一次性迁移、旧文件保留）

---

## 四、关联文件结构

```
ComfyUI-llama-cpp-prompt-enhancer/
├── nodes.py                                # 节点实现（本清单唯一权威来源）
├── support/prompt_enhancer_preset.py       # 内置预设常量（已还原为原版，不含硬编码 skill）
├── skills/<skill>/                         # skill 文件资产（SKILL.md + references/ + SOURCE.md）
├── presets/<name>.md                       # 用户预设（文件资产）
└── scripts/sync_official_skills.py         # 官方 skill 一键同步脚本
```

## 五、独立插件节点（不在本插件内）

| 注册 key | 显示名 | CATEGORY | 位置 | 功能 |
|---|---|---|---|---|
| `wanaigc_file_finder` | WanAIGC File Finder | `WanAIGC/IO` | `custom_nodes/wanaigc/nodes/file_finder.py` | 浏览电脑任意目录：directory 下拉 + custom_directory 绝对路径覆盖 + filter 通配 + recursive，输出 file_paths / file_names / count |
