import os
import re

from tqdm import tqdm

from utils.subtitle_utils import create_srt_entry


def remove_punctuation(text):
    # 定义一个正则表达式模式，匹配所有中文和英文标点符号
    punctuation_pattern = r"[^\w\s]"
    return re.sub(punctuation_pattern, "", text)


def get_subtitles(ocr_result: dict, config: dict, fps: float, file_name: str):
    """
    根据OCR结果生成字幕文件。

    本函数通过分析OCR识别结果，根据配置和视频帧率，生成符合SRT格式的字幕文本。
    主要逻辑是通过比较相邻帧的文本内容，来确定字幕的开始和结束帧。

    参数:
    - ocr_result: dict, 每一帧的OCR识别结果，包含文本信息。
    - config: dict, 视频处理的配置信息，包括视频最小持续时间等。
    - fps: float, 视频的帧率。
    - file_name: 文件名。

    返回:
    - None
    """
    frame_number_pre = 0
    text_pre = ""
    subtitles = []
    subtitle = {}
    frames = fps * config["video"]["min_duration"]
    for frame_path, value in tqdm(ocr_result.items(), desc="OCR subtitle"):
        frame_number = int(os.path.splitext(os.path.basename(frame_path))[0])
        text = value["text"]
        text_clean = remove_punctuation(text)
        text_pre_clean = remove_punctuation(text_pre)
        if text_clean == text_pre_clean and frame_number - frame_number_pre <= frames:
            subtitle["end"] = frame_number
        else:
            if subtitle:
                if subtitle["end"] - subtitle["start"] > frames:
                    subtitles.append(subtitle)
            subtitle = {
                "start": frame_number,
                "end": frame_number,
                "text": text,
            }
        frame_number_pre = frame_number
        text_pre = text

    if subtitle:
        if subtitle["end"] - subtitle["start"] > frames:
            subtitles.append(subtitle)

    subtitle_list = []
    if subtitles:
        subtitle_list = [subtitles[0]]
        for subtitle in subtitles[1:]:
            text_clean = remove_punctuation(subtitle["text"])
            text_pre_clean = remove_punctuation(subtitle_list[-1]["text"])
            if (
                text_clean == text_pre_clean
                and subtitle["start"] - subtitle_list[-1]["end"] <= frames
            ):
                subtitle_list[-1]["end"] = subtitle["end"]
            else:
                subtitle_list.append(subtitle)

    subtitle_text_list = []
    for index, subtitle in enumerate(subtitle_list):
        subtitle_text_list.append(create_srt_entry(subtitle, index + 1, fps))

    subtitle_text = "\n".join(subtitle_text_list)
    srt_path = f"{file_name}_zh_ocr.srt"
    with open(srt_path, "w") as file:
        file.write(subtitle_text)

    return srt_path
