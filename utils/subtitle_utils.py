def format_time(sec: float):
    """
    将给定的时间（以秒为单位）格式化为“小时:分钟:秒,毫秒”的格式。

    参数:
    sec (float): 需要格式化的时间，以秒为单位。

    返回:
    str: 格式化后的时间字符串，格式为“小时:分钟:秒,毫秒”。
    """
    ms = int(sec * 1000)
    sec, ms = divmod(ms, 1000)
    min, sec = divmod(sec, 60)
    hr, min = divmod(min, 60)
    return f"{hr:02}:{min:02}:{sec:02},{ms:03}"


def create_srt_entry(segment: dict, index: int, fps: int):
    """
    创建一个字幕条目。

    该函数根据视频的帧率和字幕片段信息生成字幕文件（SRT格式）的一行条目。

    参数:
    - segment: 字典类型，包含字幕的开始时间、结束时间和文本内容。
    - index: 整数类型，字幕的序号。
    - fps: 整数类型，视频的帧率。

    返回:
    字符串类型，表示一个字幕条目，按照SRT格式进行格式化。
    """
    start_time = format_time(segment["start"] / fps)
    end_time = format_time(segment["end"] / fps)
    text = segment["text"]
    return f"{index}\n{start_time} --> {end_time}\n{text}\n"
