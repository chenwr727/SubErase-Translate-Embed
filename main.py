import argparse
import os
import shutil

from modules.config import load_config
from modules.embed import embed_subtitles
from modules.erase import remove_subtitles
from modules.ocr import extract_subtitles
from modules.translate import translate_subtitles
from utils.logging_utils import update_status
from utils.video_utils import (
    create_video,
    detect_fps,
    extract_frames,
    get_temp_directory_path,
    get_temp_frame_paths,
)


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="SubErase-Translate-Embed: A tool for erasing, translating, and embedding subtitles."
    )
    parser.add_argument("--video", required=True, help="Path to the input video file.")
    parser.add_argument(
        "--language", required=True, help="Target language code for translation."
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Whether to delete the temporary directory after processing.",
    )
    args = parser.parse_args()

    # 开始处理
    update_status(f"Start! {args.video}")
    config = load_config()
    file_name, ext = os.path.splitext(args.video)
    fps = detect_fps(args.video)

    # 提取视频帧
    update_status(f"Source: extracting frames with {fps} FPS...")
    extract_frames(args.video, fps)
    temp_directory_path = get_temp_directory_path(args.video)
    frame_paths = get_temp_frame_paths(temp_directory_path)

    # 使用 OCR 提取字幕
    update_status("OCR: extracting subtitles...")
    srt_path = f"{file_name}_zh_ocr.srt"
    ocr_result, y_center = extract_subtitles(frame_paths, config, fps, srt_path)

    # 擦除原有字幕
    update_status("Erase: removing subtitles...")
    remove_subtitles(ocr_result, fps, len(frame_paths), config)
    output_path = f"{file_name}_output{ext}"
    create_video(args.video, output_path, fps)

    # 翻译字幕
    update_status("Translate: translating subtitles...")
    srt_lang_path = translate_subtitles(srt_path, args.language, config)

    # 将翻译后的字幕嵌入视频
    update_status("Embed: embedding subtitles...")
    output_file = f"{file_name}_{args.language}{ext}"
    embed_subtitles(output_path, srt_lang_path, y_center, output_file, args.language)

    if args.delete:
        if os.path.exists(file_name):
            shutil.rmtree(file_name)
            update_status("Temporary request directory {} deleted".format(file_name))
        update_status(f"Done! {args.video}")
    else:
        update_status(f"Failed! {args.video}")


if __name__ == "__main__":
    main()
