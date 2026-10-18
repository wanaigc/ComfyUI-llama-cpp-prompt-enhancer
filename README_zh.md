# ComfyUI-llama-cpp-prompt-enhancer
基于 llama.cpp 的 ComfyUI 本地提示词增强插件，原生运行 LLM 模型以润色与生成图像提示词。  
**[[📃English](./README.md)]**   

## 预览
![](./img/preview.png) 

## 新功能特性
- **本地提示词增强** — 基于 llama.cpp 的本地 LLM/VLM 模型润色、扩展图像提示词：完全离线，无需 API Key。
- **多种提示词风格** — 内置 Tags / Simple / Detailed / Extreme Detailed / Cinematic 预设，以及 Creative *Refine & Expand* 润色扩展模式。
- **模型专属提示词 Skill** — 内置 **Minimax H3**、**Krea 2**、**Moss Image**、**Qwen Image 2.1** 等模型的专属提示词增强 skill，为各模型量身定制提示词。
- **VLM 图像转提示词** — 加载带 `mmproj` 权重的视觉模型（含 Qwen 模式），直接从图像生成提示词。
- **预设系统** — 保存、管理、复用你自己的提示词预设（Preset Manager / Save Prompt Preset）。
- **结构化输出工具** — 解析模型返回的 JSON，转换为 BBoxes / SEGS / MASK 用于区域控制工作流，并可剥离 Markdown 代码块。
- **任意模型路径** — 可从任意绝对路径加载 `.gguf` 主模型与 `mmproj` 视觉投影（不限于 `ComfyUI/models/LLM`），并支持直接连接 Wanaigc File Finder。
- **模型管理节点** — Loader / Parameters / Unload Model / Clean States，以及 BETA 版 Text Encoder 节点，提供精细化控制。

## 安装步骤

#### 安装节点:
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/wanaigc/ComfyUI-llama-cpp-prompt-enhancer.git
python -m pip install -r ComfyUI-llama-cpp-prompt-enhancer/requirements.txt
#CUDA 13.1用户请执行:
#python -m pip install -r ComfyUI-llama-cpp-prompt-enhancer/requirements_cu131.txt
```

### 模型路径:
- **模型下载地址:** [Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-MTP-GGUF (HuggingFace)](https://huggingface.co/HauhauCS/Qwen3.8-27B-Uncensored-HauhauCS-Aggressive-MTP-GGUF) | [夸克网盘](https://pan.quark.cn/s/dd0ba0851a01)
- 请将下载的 `.gguf` 模型放置在 `ComfyUI/models/LLM` 目录中.  
- 支持任意 **GGUF 格式的 LLM 模型**（纯文本 LLM，或搭配对应 `mmproj` 权重的 VLM 模型）。

	> 在使用VLM模型进行图像推理之前, 请确保已经下载并选择了主模型对应的`mmproj`权重文件.

## 致谢
- [ComfyUI-llama-cpp](https://github.com/lihaoyun6/ComfyUI-llama-cpp) @lihaoyun6  
- [llama-cpp-python](https://github.com/JamePeng/llama-cpp-python) @JamePeng  
- [ComfyUI-llama-cpp](https://github.com/kijai/ComfyUI-llama-cpp) @kijai
- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) @comfyanonymous
