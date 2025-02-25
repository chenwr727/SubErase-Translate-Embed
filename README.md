简体中文 | [English](README_EN.md)

<div align="center">
    <h1>SubErase-Translate-Embed</h1>
    <p>🎬 一站式视频字幕处理解决方案</p>
    <p>
        <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
        <img src="https://img.shields.io/github/stars/chenwr727/SubErase-Translate-Embed" alt="stars">
        <img src="https://img.shields.io/github/forks/chenwr727/SubErase-Translate-Embed" alt="forks">
    </p>
</div>

## ✨ 项目亮点

SubErase-Translate-Embed 是一款强大的开源工具，让多语言视频内容制作变得简单高效。通过先进的 AI 技术，自动完成字幕识别、擦除、翻译与重新嵌入的全流程处理。

### 为什么选择 SubErase-Translate-Embed？

- 🚀 **全自动处理**：从字幕提取到重新嵌入，一键完成
- 🎯 **高精度识别**：基于 PaddleOCR 的准确字幕识别
- ✨ **完美擦除**：采用 STTN 技术，字幕擦除自然流畅
- 🌍 **多语言支持**：支持多种语言之间的互译
- 🛠️ **简单易用**：友好的命令行界面，轻松上手

## 🎥 效果展示

<div align="center">
    <img src="demo.webp" alt="Demo" width="80%">
    <p><em>左：原始视频 | 右：处理后的视频</em></p>
</div>

## 🚀 主要功能

- **智能字幕识别**：
  - 基于 PaddleOCR 的高精度文字识别
  - 支持多种字体和复杂背景
  - 自动检测字幕位置和时间戳

- **专业字幕擦除**：
  - 基于 STTN 的智能修复技术
  - 无痕擦除，画面自然
  - 支持复杂背景处理

- **高质量翻译**：
  - 接入 ChatGPT API，确保翻译准确性
  - 保持原文语境和表达方式
  - 支持多语言互译

- **精准字幕嵌入**：
  - 自定义字幕样式
  - 智能位置调整
  - 平滑过渡效果

## 🔧 安装指南

要使用 SubErase-Translate-Embed，请按照以下步骤操作：

1. **克隆项目代码**：
    ```bash
    git clone --recursive https://github.com/chenwr727/SubErase-Translate-Embed.git
    ```

2. **安装依赖包**：
    ```bash
    conda create -n ste python=3.10
    conda activate ste
    pip install paddlepaddle-gpu==2.6.1.post120 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html
    pip install -r requirements.txt
    ```

3. **下载模型**:
    - PaddleOCR
        - [det](https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_det_server_infer.tar)
        - [rec](https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_rec_server_infer.tar)
    - [STTN](https://drive.google.com/file/d/1ZAMV8547wmZylKRt5qR_tC5VlosXD4Wv/view?usp=sharing)
    
    将模型文件保存到 `./models` 目录下，结构如下：
    ```
    models
    ├── ch_PP-OCRv4_det_server_infer
    └── ch_PP-OCRv4_rec_server_infer
    └── sttn.pth
    ```

4. **配置文件**：
    ```bash
    cp config-template.yaml config.yaml
    ```

5. **应用安装**：
    ```bash
    sudo apt install imagemagick
    conda install -c conda-forge ffmpeg
    conda install -c conda-forge gcc=12.2.0
    ```

## 📖 使用方法

只需一行命令，即可完成视频字幕的全流程处理：

```bash
python main.py --video input_video.mp4 --language English
```

更多高级配置选项，请参考 `config.yaml`。

## 🤝 参与贡献

我们欢迎任何形式的贡献，无论是新功能、bug 修复还是文档改进。请查看我们的贡献指南了解详情。

## 📄 开源协议

本项目采用 MIT 协议开源，详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

感谢以下开源项目的贡献：

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [STTN](https://github.com/researchmm/STTN)
- [video-subtitle-remover](https://github.com/YaoFANGUK/video-subtitle-remover)
- [translation-agent](https://github.com/andrewyng/translation-agent.git)
