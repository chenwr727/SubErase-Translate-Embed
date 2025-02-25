[简体中文](README.md) | English

<div align="center">
    <h1>SubErase-Translate-Embed</h1>
    <p>🎬 All-in-One Video Subtitle Processing Solution</p>
    <p>
        <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
        <img src="https://img.shields.io/github/stars/chenwr727/SubErase-Translate-Embed" alt="stars">
        <img src="https://img.shields.io/github/forks/chenwr727/SubErase-Translate-Embed" alt="forks">
    </p>
</div>

## ✨ Overview

SubErase-Translate-Embed is a powerful open-source tool that simplifies multilingual video content creation. Using advanced AI technology, it automates the entire process of subtitle detection, removal, translation, and embedding.

### Why Choose SubErase-Translate-Embed?

- 🚀 **Fully Automated**: One-click solution from subtitle extraction to embedding
- 🎯 **High Accuracy**: Precise subtitle recognition powered by PaddleOCR
- ✨ **Perfect Removal**: Natural subtitle removal using STTN technology
- 🌍 **Multilingual**: Support for multiple language translations
- 🛠️ **User-Friendly**: Easy-to-use command-line interface

## 🎥 Demo

<div align="center">
    <img src="demo.webp" alt="Demo" width="80%">
    <p><em>Left: Original Video | Right: Processed Video</em></p>
</div>

## 🚀 Key Features

- **Intelligent Subtitle Recognition**:
  - High-precision text recognition with PaddleOCR
  - Support for various fonts and complex backgrounds
  - Automatic subtitle position and timestamp detection

- **Professional Subtitle Removal**:
  - Smart restoration using STTN technology
  - Seamless removal with natural results
  - Complex background handling

- **High-Quality Translation**:
  - Integration with ChatGPT API for accurate translations
  - Preservation of original context and expression
  - Support for multiple language pairs

- **Precise Subtitle Embedding**:
  - Customizable subtitle styles
  - Intelligent position adjustment
  - Smooth transition effects

## 🔧 Installation

Follow these steps to set up SubErase-Translate-Embed:

1. **Clone the Repository**:
    ```bash
    git clone --recursive https://github.com/chenwr727/SubErase-Translate-Embed.git
    ```

2. **Install Dependencies**:
    ```bash
    conda create -n ste python=3.10
    conda activate ste
    pip install paddlepaddle-gpu==2.6.1.post120 -f https://www.paddlepaddle.org.cn/whl/linux/mkl/avx/stable.html
    pip install -r requirements.txt
    ```

3. **Download Models**:
    - PaddleOCR
        - [det](https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_det_server_infer.tar)
        - [rec](https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_rec_server_infer.tar)
    - [STTN](https://drive.google.com/file/d/1ZAMV8547wmZylKRt5qR_tC5VlosXD4Wv/view?usp=sharing)
    
    Save the model files in the `./models` directory with the following structure:
    ```
    models
    ├── ch_PP-OCRv4_det_server_infer
    └── ch_PP-OCRv4_rec_server_infer
    └── sttn.pth
    ```

4. **Configuration**:
    ```bash
    cp config-template.yaml config.yaml
    ```

5. **Install Applications**:
    ```bash
    sudo apt install imagemagick
    conda install -c conda-forge ffmpeg
    conda install -c conda-forge gcc=12.2.0
    ```

## 📖 Usage

Process your video with a single command:

```bash
python main.py --video input_video.mp4 --language English
```

For advanced configuration options, refer to `config.yaml`.

## 🤝 Contributing

We welcome all forms of contributions, whether it's new features, bug fixes, or documentation improvements. Please check our contribution guidelines for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Thanks to these amazing projects:

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [STTN](https://github.com/researchmm/STTN)
- [video-subtitle-remover](https://github.com/YaoFANGUK/video-subtitle-remover)
- [translation-agent](https://github.com/andrewyng/translation-agent.git)
