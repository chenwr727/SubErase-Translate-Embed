import pysrt
from moviepy.editor import CompositeVideoClip, TextClip, VideoFileClip
from pysrt.srtfile import SubRipFile, SubRipItem


def create_subclip(sub: SubRipItem, fontsize: int, y_center: int, font: str):
    """
    根据字幕项生成视频字幕片段。

    本函数接收一个字幕项（包括开始时间和结束时间以及文本内容），并根据指定的字体大小、
    字体类型等参数创建一个视频字幕片段。字幕片段将被定位在指定的垂直中心位置，并且持续时间
    为字幕项的开始时间和结束时间之差。

    参数:
    - sub: SubRipItem类型，包含字幕的开始时间、结束时间和文本内容。
    - fontsize: int类型，字幕的字体大小。
    - y_center: int类型，字幕在视频中的垂直中心位置（像素值）。
    - font: str类型，字幕所使用的字体。

    返回:
    - TextClip类型，生成的字幕片段对象。
    """
    start_time = sub.start.ordinal / 1000.0
    end_time = sub.end.ordinal / 1000.0
    txtclip = TextClip(
        sub.text,
        fontsize=fontsize,
        font=font,
        color="white",
        stroke_color="black",
        stroke_width=1,
    )
    txtclip = txtclip.set_pos(("center", y_center - txtclip.size[1] // 2))
    return txtclip.set_start(start_time).set_duration(end_time - start_time)


def estimate_font_size(target_subtitle_width: int):
    """
    根据目标字幕宽度估算合适的字体大小。

    该函数假定字幕的宽度与字体大小之间存在一个大致的比例关系，
    即字幕宽度是字体大小的15倍。通过这个估算，可以为不同大小的字幕
    自动选择合适的字体大小，以保持视觉上的一致性。

    参数:
    target_subtitle_width: int - 目标字幕的宽度，单位为像素。

    返回值:
    int - 估算的字体大小，单位为像素。
    """
    estimated_font_size = int(target_subtitle_width / 15)
    return estimated_font_size


def get_textclip_len(text: str, fontsize: int, font: str):
    """
    计算文本剪辑的宽度。

    该函数通过创建一个文本剪辑对象并获取其大小信息，返回文本剪辑的宽度。
    这在需要根据文本内容和样式动态调整布局或尺寸时非常有用。

    参数:
    text: str - 要显示的文本内容。
    fontsize: int - 文本的字体大小。
    font: str - 文本的字体名称。

    返回值:
    int - 文本剪辑的宽度。
    """
    txtclip = TextClip(text, fontsize=fontsize, font=font)
    return txtclip.size[0]


def wrap_subtitle_text(
    subs: SubRipFile, fontsize: int, target_subtitle_width: int, font: str
):
    """
    对字幕文本进行换行处理以适应指定宽度。

    参数:
    - subs: SubRipFile 类型的对象，包含需要处理的字幕数据。
    - fontsize: 整数类型，表示字幕文本的字体大小。
    - target_subtitle_width: 整数类型，表示字幕显示的目标宽度。
    - font: 字符串类型，表示字幕文本的字体。

    返回值:
    - SubRipFile 类型的对象，其中每个字幕的文本已根据指定宽度进行了换行处理。
    """
    for sub in subs:
        text = sub.text.strip()
        split_word = ""
        if " " in text:
            split_word = " "
            text = text.split()
        lines = []
        current_line = ""
        for word in text:
            text_ = current_line + split_word + word
            if get_textclip_len(text_, fontsize, font) > target_subtitle_width:
                lines.append(current_line)
                current_line = word
            else:
                if current_line:
                    current_line += split_word
                current_line += word
        lines.append(current_line)
        sub.text = "\n".join(lines)
    return subs


def get_font(language: str):
    """
    根据语言选择合适的字体文件路径。

    参数:
    language (str): 语言名称，用于确定要加载的字体。

    返回:
    str or None: 字体文件的路径，如果找不到匹配的语言，则返回None。
    """
    font = None
    if language == "English":
        font = "./fonts/arialbd.ttf"
    return font


def embed_subtitles(
    video_path: str,
    srt_path: str,
    y_center: int,
    output_file: str,
    language: str,
    target_subtitle_width_ratio: float = 0.8,
    target_size: int = 30,
):
    """
    向视频添加字幕。

    :param video_path: 视频文件的路径。
    :param srt_path: 字幕文件的路径，格式为SRT。
    :param y_center: 字幕垂直位置的Y坐标，表示字幕垂直居中位置的中心线。
    :param output_file: 输出带有字幕的视频文件的路径。
    :param language: 字幕的语言，用于选择合适的字体。
    :param target_subtitle_width_ratio: 字幕宽度与视频宽度的比例，默认为0.8。
    :param target_size: 输出文件的目标大小，默认为30M。
    """
    video_clip = VideoFileClip(video_path)
    video_width = video_clip.size[0]

    font = get_font(language)

    target_subtitle_width = int(video_width * target_subtitle_width_ratio)
    fontsize = estimate_font_size(target_subtitle_width)

    subs = pysrt.open(srt_path)
    subs = wrap_subtitle_text(subs, fontsize, target_subtitle_width, font)

    subclips = [create_subclip(sub, fontsize, y_center, font) for sub in subs]
    final_clip = CompositeVideoClip([video_clip] + subclips)

    target_bitrate = (target_size * 8 * 1024 * 1024) / video_clip.duration / 1024
    final_clip.write_videofile(
        output_file,
        codec="libx264",
        bitrate=f"{int(target_bitrate)}k",
    )
