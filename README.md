简体中文 | [English](README_EN.md)

# SubErase-Translate-Embed

## 项目简介

**SubErase-Translate-Embed** 是一个开源工具，旨在提升多语言视频内容的可访问性。该工具通过集成 OCR 技术、字幕擦除、翻译与嵌入功能，实现对短剧视频中字幕的自动处理，使用户能够方便地体验不同语言版本的短剧内容。

本项目为希望将视频翻译成多种语言并重新嵌入字幕的用户提供了一站式解决方案，广泛应用于多语言教学、国际化影视制作、全球观众娱乐体验等场景。

![Demo](demo.webp)

## 主要功能

- **字幕识别**：使用 OCR 技术（基于 PaddleOCR）从视频中提取字幕。
- **字幕擦除**：借助 STTN（基于时空轨迹网络）技术，自动擦除原视频中的字幕。
- **字幕翻译**：利用 OpenAI 的 ChatGPT API 或其他翻译服务，将提取的字幕翻译为目标语言。
- **字幕嵌入**：将翻译后的字幕重新嵌入视频，生成新的多语言版本。

## 安装指南

要使用 SubErase-Translate-Embed，请按照以下步骤操作：

1. **克隆项目代码**：
    ```bash
    git clone https://github.com/chenwr727/SubErase-Translate-Embed.git
    ```

2. **安装依赖包**：
    ```bash
    pip install -r requirements.txt
    ```

3. **下载模型**:
    - [PaddleOCR](https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_det_server_infer.tar)
    - [STTN](https://drive.google.com/file/d/1ZAMV8547wmZylKRt5qR_tC5VlosXD4Wv/view?usp=sharing)

4. **配置文件**：
    ```bash
    cp config-template.yaml config.yaml
    ```

## 使用方法

通过以下命令执行视频处理，自动识别、擦除、翻译并嵌入字幕：

```bash
python main.py --video input_video.mp4 --language English
```
其中 `input_video.mp4` 是你的视频文件名，`English` 是目标翻译语言代码。

## 项目结构

- **main.py**：主程序入口，负责管理整个处理流程。
- **modules/**：包含各个功能模块（OCR、擦除字幕、翻译、嵌入字幕）。
- **utils/**：包含通用工具，如日志记录、视频处理工具等。
- **config.yaml**：配置文件，用于设置语言、视频格式等参数。

## 参考项目

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [STTN](https://github.com/researchmm/STTN)
- [video-subtitle-remover](https://github.com/YaoFANGUK/video-subtitle-remover)
- [translation-agent](https://github.com/andrewyng/translation-agent.git)
