import os
import time

import pysrt

from utils.translation_utils import translate_text


def chatgpt_translate(text: str, language: str):
    """
    使用ChatGPT模型翻译字幕文本。

    参数:
    - text: str，需要翻译的字幕文本。
    - language: str，目标翻译语言，如"English"。

    返回:
    - str，翻译后的字幕文本或错误信息。
    """
    content = ""
    try:
        content = translate_text(
            source_lang="Chinese", target_lang=language, source_text=text
        )
    except Exception as e:
        print(f"chatgpt translate error:" + str(e))
    return content


def check_timeline(srt, new_srt_text):
    """
    检查字幕时间线是否一致。

    本函数通过比较原始字幕对象和新的字幕文本中每个字幕片段的开始和结束时间，
    来验证两者的时间线是否完全一致。这用于确保字幕内容经过修改后（如翻译或格式调整），
    其时间戳未发生任何变化，这对于保持字幕与视频内容的同步至关重要。

    参数:
    - srt: pysrt.SubRipFile对象，代表原始的字幕数据。
    - new_srt_text: 字符串，表示经过修改但需要验证时间线的新字幕文本。

    返回:
    - 布尔值：如果所有字幕片段的开始和结束时间都相同，则返回True，表示时间线一致；
      否则，在发现不一致时立即返回False。
    """
    new_srt = pysrt.SubRipFile().from_string(new_srt_text)

    for s, new_s in zip(srt, new_srt):
        if s.start != new_s.start:
            return False
        if s.end != new_s.end:
            return False

    return True


def translate_subtitles(srt_path: str, target_language: str, try_times: int = 5):
    """
    将字幕翻译成目标语言并保存。

    该函数读取字幕文件，使用 chatgpt_translate 函数翻译内容，并将翻译后的字幕保存到新文件中。
    如果经过多次尝试后翻译的内容行数或时间格式与原始字幕不符，仍然会返回翻译后字幕文件的路径。

    :param srt_path: 字幕文件的路径。
    :param target_language: 目标语言代码，用于翻译。
    :param try_times: 重试次数，默认为 5 次。
    :return: 翻译后字幕文件的路径。
    """
    srt_path_english = srt_path.replace("_zh", f"_{target_language}")
    if os.path.exists(srt_path_english):
        return srt_path_english

    with open(srt_path, "r", encoding="utf-8") as f:
        subtitles = f.read().strip()
    srt = pysrt.open(srt_path)

    lines = len(subtitles.split("\n"))
    for i in range(try_times):
        translated_subtitles = chatgpt_translate(subtitles, target_language)
        if translated_subtitles:
            if len(translated_subtitles.strip().split("\n")) != lines:
                print(f"chatgpt translate lines not match, try again! {i + 1}")
            elif not check_timeline(srt, translated_subtitles):
                print(f"chatgpt translate timeline not match, try again! {i + 1}")
            else:
                with open(srt_path_english, "w") as f:
                    f.write(translated_subtitles)
                return srt_path_english
        time.sleep(1)

    return srt_path
