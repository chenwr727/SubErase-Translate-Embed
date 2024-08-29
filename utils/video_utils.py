import glob
import os
import subprocess
from typing import List

TEMP_VIDEO_FILE = "tmp.mp4"
TEMP_FRAME_FORMAT = "png"


def run_ffmpeg(args: List[str]) -> bool:
    """
    执行ffmpeg命令并检查其是否成功完成。

    参数:
        args (List[str]): 一个字符串列表，表示ffmpeg命令行工具的参数。

    返回:
        bool: 如果ffmpeg命令成功执行，则返回True，否则返回False。
    """
    commands = ["ffmpeg", "-hide_banner", "-loglevel", "error"]
    commands.extend(args)
    try:
        subprocess.check_output(commands, stderr=subprocess.STDOUT)
        return True
    except Exception as e:
        print(str(e))
        pass
    return False


def detect_fps(target_path: str) -> float:
    """
    检测视频文件的帧率（FPS）。

    该函数使用 ffprobe 工具查询视频的帧率。构造一个命令来启动 ffprobe，并指定日志级别、选择视频流以及请求帧率信息。
    执行该命令并解析输出以获取帧率。

    参数:
    target_path (str): 视频文件的路径。

    返回:
    float: 检测到的视频帧率。如果无法检测帧率则返回 30.0。
    """
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=r_frame_rate",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        target_path,
    ]
    output = subprocess.check_output(command).decode().strip().split("/")
    try:
        numerator, denominator = map(int, output)
        return numerator / denominator
    except Exception:
        pass
    return 30


def extract_frames(
    target_path: str, fps: float = 30, temp_frame_quality: int = 1
) -> bool:
    """
    从视频文件中提取帧并保存为临时图像序列。

    该函数使用FFmpeg工具从视频文件中提取帧，并将它们保存为指定质量的临时图像序列。
    主要用于视频处理或分析前的预处理阶段，以便于对单个帧进行操作或分析。

    参数:
    - target_path: str 视频文件的路径，用于提取帧的源视频。
    - fps: float 视频的帧率，默认为30帧每秒。用于设置提取帧的频率。
    - temp_frame_quality: int 图像的质量，用于控制输出图像的质量，值越小质量越高。

    返回:
    - bool 提取帧操作是否成功。
    """
    temp_directory_path = get_temp_directory_path(target_path)
    commands = [
        "-hwaccel",
        "auto",
        "-i",
        target_path,
        "-q:v",
        str(temp_frame_quality),
        "-pix_fmt",
        "rgb24",
        "-vf",
        "fps=" + str(fps),
        os.path.join(temp_directory_path, "%04d." + TEMP_FRAME_FORMAT),
    ]
    return run_ffmpeg(commands)


def create_video(
    target_path: str,
    output_path: str,
    fps: float = 30,
    output_video_quality: int = 35,
    output_video_encoder: str = "libx264",
) -> bool:
    """
    合成视频文件。

    该函数使用FFmpeg命令将临时目录中的帧与目标音频合并为最终的视频文件。

    参数:
    - target_path: 目标文件路径，用于获取临时目录路径。
    - output_path: 输出视频文件的路径。
    - fps: 视频的帧率，默认为30帧每秒。
    - output_video_quality: 输出视频的质量，0-51的整数，其中0是无损压缩，51是最大压缩。
    - output_video_encoder: 输出视频的编码器，默认使用libx264。

    返回:
    - bool: 表示FFmpeg命令执行是否成功的布尔值。
    """
    temp_directory_path = get_temp_directory_path(target_path)
    output_video_quality = (output_video_quality + 1) * 51 // 100

    commands = [
        "-hwaccel",
        "auto",
        "-r",
        str(fps),
        "-i",
        os.path.join(temp_directory_path, "%04d." + TEMP_FRAME_FORMAT),
        "-i",
        target_path,
        "-c:v",
        output_video_encoder,
        "-c:a",
        "aac",
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-pix_fmt",
        "yuv420p",
    ]

    if output_video_encoder in ["libx264", "libx265", "libvpx"]:
        commands.extend(["-crf", str(output_video_quality)])
    if output_video_encoder in ["h264_nvenc", "hevc_nvenc"]:
        commands.extend(["-cq", str(output_video_quality)])

    commands.extend(["-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2"])
    commands.extend(["-y", output_path])

    return run_ffmpeg(commands)


def get_temp_frame_paths(
    temp_directory_path: str, temp_frame_format: str = TEMP_FRAME_FORMAT
) -> List[str]:
    """
    获取临时文件夹中所有指定格式的临时帧文件路径。

    该函数通过遍历给定的临时目录，寻找所有符合指定格式的临时帧文件，并将它们的路径
    组成一个列表返回。路径列表按文件名排序，以便于后续处理时可以按顺序访问这些文件。

    参数:
    - temp_directory_path: str
      临时文件夹的路径，其中存放了所有待处理的临时帧文件。
    - temp_frame_format: str
      临时帧文件的格式，默认值为 TEMP_FRAME_FORMAT，这是一个全局变量，定义了
      系统默认的临时帧文件格式。

    返回值:
    - List[str]
      一个字符串列表，包含了所有找到的临时帧文件的完整路径。路径按文件名排序。
    """
    temp_frame_paths = glob.glob(
        (os.path.join(glob.escape(temp_directory_path), "*." + temp_frame_format))
    )
    temp_frame_paths.sort()
    return temp_frame_paths


def get_temp_directory_path(target_path: str) -> str:
    """
    根据给定的文件路径创建一个临时目录，并返回该目录的路径。

    参数:
    target_path (str): 目标文件的路径。

    返回:
    str: 创建的临时目录的路径。
    """
    target_name, _ = os.path.splitext(os.path.basename(target_path))
    target_directory_path = os.path.dirname(target_path)
    temp_directory_path = os.path.join(target_directory_path, target_name)
    os.makedirs(temp_directory_path, exist_ok=True)
    return temp_directory_path
