import sys
from typing import List

sys.path.insert(0, "./STTN")

import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from tqdm import tqdm

from STTN.core.utils import Stack, ToTorchFormatTensor
from STTN.model import sttn

_to_tensors = transforms.Compose([Stack(), ToTorchFormatTensor()])


def get_ref_index(neighbor_ids, length):
    """
    根据邻居ID列表和给定长度，获取参考索引列表。

    该函数的目的是在一系列ID中找出哪些ID未在邻居ID列表中出现，这些未出现的ID将被视为参考索引。
    这在某些应用场景中，比如网络节点选择、数据处理等，可能需要找出不在邻近范围内的节点作为参考或基准。

    参数:
    neighbor_ids: 邻居ID列表，包含已知邻居节点的ID。
    length: 给定的长度，代表ID的范围。

    返回:
    一个列表，包含根据指定规则选出的参考索引。
    """
    ref_length = 20
    ref_index = []
    for i in range(0, length, ref_length):
        if not i in neighbor_ids:
            ref_index.append(i)
    return ref_index


def build_sttn_model(ckpt_p: str, device="cuda"):
    """
    构建并加载预训练参数到STTN模型中。

    参数:
    ckpt_p: str - 模型检查点文件的路径。
    device: str - 模型推理所使用的设备，默认为"cuda"。

    返回:
    model - 加载了预训练参数的STTN模型实例。
    """
    model = sttn.InpaintGenerator().to(device)
    data = torch.load(ckpt_p, map_location=device)
    model.load_state_dict(data["netG"])
    model.eval()
    return model


@torch.no_grad()
def inpaint_video_with_builded_sttn(
    model,
    paths: List[str],
    frames: List[Image.Image],
    masks: List[Image.Image],
    neighbor_stride: int = 10,
    device="cuda",
) -> List[Image.Image]:
    """
    使用预训练的STTN模型对视频中的破损帧进行修复。

    参数:
    model: STTN模型实例，用于帧修复。
    paths: 每帧的文件路径列表。
    frames: 视频帧的图像列表。
    masks: 视频帧的遮罩列表，用于指示需要修复的区域。
    neighbor_stride: 修复时参考帧的间隔。
    device: 模型运行的设备，可以是'cuda'或'cpu'。

    返回:
    一个包含修复后帧的图像列表。
    """
    w, h = 432, 240
    video_length = len(frames)

    feats = [frame.resize((w, h)) for frame in frames]
    feats = _to_tensors(feats).unsqueeze(0) * 2 - 1
    _masks = [mask.resize((w, h), Image.NEAREST) for mask in masks]
    _masks = _to_tensors(_masks).unsqueeze(0)

    feats, _masks = feats.to(device), _masks.to(device)
    comp_frames = [None] * video_length

    feats = (feats * (1 - _masks).float()).view(video_length, 3, h, w)
    feats = model.encoder(feats)
    _, c, feat_h, feat_w = feats.size()
    feats = feats.view(1, video_length, c, feat_h, feat_w)

    # completing holes by spatial-temporal transformers
    for f in tqdm(
        range(0, video_length, neighbor_stride), desc="Inpaint Image", leave=False
    ):
        neighbor_ids = list(
            range(
                max(0, f - neighbor_stride), min(video_length, f + neighbor_stride + 1)
            )
        )
        ref_ids = get_ref_index(neighbor_ids, video_length)

        pred_feat = model.infer(
            feats[0, neighbor_ids + ref_ids, :, :, :],
            _masks[0, neighbor_ids + ref_ids, :, :, :],
        )
        pred_img = model.decoder(pred_feat[: len(neighbor_ids), :, :, :])
        pred_img = torch.tanh(pred_img)
        pred_img = (pred_img + 1) / 2
        pred_img = pred_img.permute(0, 2, 3, 1) * 255
        for i in range(len(neighbor_ids)):
            idx = neighbor_ids[i]
            b_mask = _masks.squeeze()[idx].unsqueeze(-1)
            b_mask = (b_mask != 0).int()
            frame = torch.from_numpy(np.array(frames[idx].resize((w, h))))
            frame = frame.to(device)
            img = pred_img[i] * b_mask + frame * (1 - b_mask)
            img = img.cpu().numpy()
            if comp_frames[idx] is None:
                comp_frames[idx] = img
            else:
                comp_frames[idx] = comp_frames[idx] * 0.5 + img * 0.5

    result = []
    ori_w, ori_h = frames[0].size
    for idx in tqdm(range(len(frames)), desc="Restore Image", leave=False):
        frame = np.array(frames[idx])
        b_mask = np.uint8(np.array(masks[idx])[..., np.newaxis] != 0)
        comp_frame = np.uint8(comp_frames[idx])
        comp_frame = Image.fromarray(comp_frame).resize((ori_w, ori_h))
        comp_frame = np.array(comp_frame)
        comp_frame = comp_frame * b_mask + frame * (1 - b_mask)
        result.append([paths[idx], comp_frame])
    return result
