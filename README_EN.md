English | [简体中文](README.md)

# SubErase-Translate-Embed

## Project Overview

**SubErase-Translate-Embed** is an open-source tool designed to enhance the accessibility of multilingual video content. By integrating OCR technology, subtitle erasure, translation, and embedding functions, this tool automatically processes subtitles in short films, enabling users to easily experience short film content in different languages.

This project provides a one-stop solution for users who wish to translate videos into multiple languages and re-embed the subtitles. It is widely applicable in scenarios such as multilingual education, international film production, and global audience entertainment experiences.

![Demo](demo.webp)

## Key Features

- **Subtitle Recognition**: Uses OCR technology (based on PaddleOCR) to extract subtitles from videos.
- **Subtitle Erasure**: Automatically erases the original subtitles in the video using STTN (Spatio-Temporal Trajectory Network).
- **Subtitle Translation**: Utilizes OpenAI's ChatGPT API or other translation services to translate the extracted subtitles into the target language.
- **Subtitle Embedding**: Re-embeds the translated subtitles into the video, generating a new multilingual version.

## Installation Guide

To use SubErase-Translate-Embed, follow these steps:

1. **Clone the project code**:
    ```bash
    git clone --recursive https://github.com/chenwr727/SubErase-Translate-Embed.git
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Download models**:
    - [PaddleOCR](https://paddleocr.bj.bcebos.com/PP-OCRv4/chinese/ch_PP-OCRv4_det_server_infer.tar)
    - [STTN](https://drive.google.com/file/d/1ZAMV8547wmZylKRt5qR_tC5VlosXD4Wv/view?usp=sharing)

4. **Configuration**:
    ```bash
    cp config-template.yaml config.yaml
    ```

## Usage

Execute video processing with the following command, automatically recognizing, erasing, translating, and embedding subtitles:

```bash
python main.py --video input_video.mp4 --language English
```
Where `input_video.mp4` is the name of your video file, and `English` is the target translation language.

## Project Structure

- **main.py**: The main program entry point, responsible for managing the entire processing workflow.
- **modules/**: Contains various functional modules (OCR, subtitle erasure, translation, embedding).
- **utils/**: Contains general tools, such as logging and video processing utilities.
- **config.yaml**: Configuration file for setting language, video format, and other parameters.

## References

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [STTN](https://github.com/researchmm/STTN)
- [video-subtitle-remover](https://github.com/YaoFANGUK/video-subtitle-remover)
- [translation-agent](https://github.com/andrewyng/translation-agent.git)
