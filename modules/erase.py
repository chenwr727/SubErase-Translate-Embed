import concurrent.futures
import os
from typing import List

import cv2
import numpy as np
import torch
from PIL import Image
from tqdm import tqdm

from modules.sttn import build_sttn_model, inpaint_video_with_builded_sttn
from utils.image_utils import load_img


@torch.no_grad()
def inpaint_video(
    paths_list: List[str],
    frames_list: List[Image.Image],
    masks_list: List[Image.Image],
    neighbor_stride: int,
    ckpt_p="./sttn/checkpoints/sttn.pth",
):
    """
    对视频帧进行修复。

    使用预训练的 STTN 模型对视频帧进行修复。根据设备情况选择在 CUDA 或 CPU 上执行修复过程。此函数处理每个视频的帧序列，尝试恢复帧中的缺失部分。

    参数:
    - paths_list: 视频帧路径列表。
    - frames_list: 视频帧图像列表。
    - masks_list: 帧掩码图像列表。
    - neighbor_stride: 邻居帧之间的步长。
    - ckpt_p: STTN 模型检查点文件路径。

    返回:
    - 修复后的视频帧图像路径列表。
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # build sttn model
    model = build_sttn_model(ckpt_p, device)

    results = []

    for paths, frames, masks in tqdm(
        zip(paths_list, frames_list, masks_list),
        desc="Inpaint job",
        total=len(paths_list),
    ):
        # inference
        result = inpaint_video_with_builded_sttn(
            model, paths, frames, masks, neighbor_stride, device
        )
        results.extend(result)

    return results


def inpaint_imag(mask_result: List[tuple]):
    """
    对掩码处理后的图像进行修复。

    使用多线程并行处理的方法，对每个掩码帧进行处理并保存图像。
    这里使用了tqdm来显示处理进度，使程序在执行时能给出进度反馈。

    参数:
    mask_result: 掩码处理后的结果，是一个包含多个帧的可迭代对象。

    返回:
    None
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        list(
            tqdm(
                executor.map(process_frame, mask_result),
                total=len(mask_result),
                desc="Save Image",
            )
        )
    return None


def process_frame(value: tuple):
    """
    处理并保存单个视频帧。

    参数:
    value: 一个元组，第一个元素是帧的文件路径，第二个元素是帧的图像数据（以计算生成的方式获得）。

    返回值:
    无返回值，但该函数会直接在文件系统中生成视频帧图像文件。
    """
    frame_path, comp_frame = value
    Image.fromarray(np.uint8(comp_frame)).save(frame_path)


def extract_mask(
    mask_result: dict,
    fps: int,
    frame_len: int,
    max_frame_length: int,
    min_frame_length: int,
    mask_expand: int = 20,
):
    """
    根据掩膜结果提取连续帧的路径、图像和掩膜信息。

    :param mask_result: 包含每帧文件路径和其对应掩膜信息的字典。
    :param fps: 视频的帧率。
    :param frame_len: 视频的帧长度。
    :param max_frame_length: 最大帧长度。
    :param min_frame_length: 最小帧长度。
    :param mask_expand: 掩膜外扩的像素数。
    :return: 一个包含三个列表的元组，分别包含每组连续帧的路径、图像和掩膜信息。
    """

    def add_frames():
        end = frame_number
        if frame_number_pre == frame_number:
            end += min_frame_length
        for i in range(frame_number_pre + 1, end):
            if i > frame_len or i > frame_number_pre + min_frame_length:
                break
            frame_path_ = os.path.join(os.path.split(frame_path)[0], "%04d.png" % i)
            image_ = load_img(frame_path_)
            mask_ = Image.fromarray(np.zeros(image_.size[::-1], dtype="uint8"))
            paths.append(frame_path_)
            frames.append(image_)
            masks.append(mask_)

    paths_list = []
    frames_list = []
    masks_list = []
    paths = []
    frames = []
    masks = []
    frame_number_pre = 0
    for frame_path, value in tqdm(mask_result.items(), desc="Find Mask"):
        frame_number = int(os.path.splitext(os.path.basename(frame_path))[0])
        image = load_img(frame_path)
        width_ = image.size[0]
        mask = np.zeros(image.size[::-1], dtype="uint8")
        xmin, ymin, xmax, ymax = value["box"]
        xwidth = min(xmin, width_ - xmax)
        cv2.rectangle(
            mask,
            (max(0, xwidth - mask_expand), ymin - mask_expand),
            (min(width_ - xwidth + mask_expand, width_ - 1), ymax + mask_expand),
            (255, 255, 255),
            thickness=-1,
        )
        mask = Image.fromarray(mask)

        if frame_number - frame_number_pre < fps * 2 and len(paths) < max_frame_length:
            paths.append(frame_path)
            frames.append(image)
            masks.append(mask)
        else:
            if paths:
                add_frames()
                paths_list.append(paths)
                frames_list.append(frames)
                masks_list.append(masks)
            paths = [frame_path]
            frames = [image]
            masks = [mask]
        frame_number_pre = frame_number

    if paths:
        add_frames()
        paths_list.append(paths)
        frames_list.append(frames)
        masks_list.append(masks)

    if len(paths_list[-1]) < min_frame_length:
        paths = paths_list.pop()
        paths_list[-1].extend(paths)
        frames = frames_list.pop()
        frames_list[-1].extend(frames)
        masks = masks_list.pop()
        masks_list[-1].extend(masks)

    return paths_list, frames_list, masks_list


def remove_subtitles(ocr_result: dict, fps: float, frame_len: int, config: dict):
    """
    移除视频中的字幕。

    参数:
    - ocr_result: dict, OCR 识别的结果，包含需要移除的字幕信息。
    - fps: float, 视频的帧率，用于计算视频处理的速度。
    - frame_len: int, 帧的长度，用于调整视频处理的精度。
    - config: dict, 配置文件，包含视频处理的参数。

    返回值:
    无。
    """
    paths_list, frames_list, masks_list = extract_mask(
        ocr_result,
        fps,
        frame_len,
        config["erase"]["max_frame_length"],
        config["erase"]["min_frame_length"],
        config["erase"]["mask_expand"],
    )
    results = inpaint_video(
        paths_list,
        frames_list,
        masks_list,
        config["erase"]["neighbor_stride"],
        config["erase"]["ckpt_p"],
    )
    inpaint_imag(results)
