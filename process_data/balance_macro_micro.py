#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
平衡数据集中的宏表情和微表情数量
对每个视频片段的宏表情进行采样，使宏表情总数与微表情数量接近
"""

import os
import json
import argparse
import random
import logging
from collections import defaultdict
from tqdm import tqdm

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def extract_video_id(image_path):
    """
    从图像路径中提取视频ID
    
    Args:
        image_path: 图像路径
        
    Returns:
        视频ID (例如 "011_7")
    """
    # 提取文件名
    filename = os.path.basename(image_path)
    # 假设文件名格式为 "{video_id}_{frame_number}.jpg"
    # 例如 "011_7_0866.jpg"
    parts = filename.split('_')
    if len(parts) >= 2:
        return f"{parts[0]}_{parts[1]}"
    return None

def balance_expressions(input_jsonl, output_jsonl, target_ratio=1.5):
    """
    平衡数据集中的宏表情和微表情数量
    
    Args:
        input_jsonl: 输入的jsonl文件路径
        output_jsonl: 输出的jsonl文件路径
        target_ratio: 宏表情与微表情的目标比率（宏表情数量/微表情数量）
    """
    # 读取原始jsonl文件
    logger.info(f"读取输入文件: {input_jsonl}")
    
    data = []
    with open(input_jsonl, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    
    # 分类宏表情和微表情
    macro_expressions = []
    micro_expressions = []
    
    for item in data:
        if "messages" in item and len(item["messages"]) >= 2:
            if "Macro" in item["messages"][1]["content"]:
                macro_expressions.append(item)
            elif "Micro" in item["messages"][1]["content"]:
                micro_expressions.append(item)
    
    logger.info(f"原始数据: {len(data)} 条")
    logger.info(f"宏表情: {len(macro_expressions)} 条")
    logger.info(f"微表情: {len(micro_expressions)} 条")
    
    # 计算每个视频片段的宏表情和微表情
    video_macros = defaultdict(list)
    video_micros = defaultdict(list)
    
    for item in macro_expressions:
        if "images" in item and item["images"]:
            video_id = extract_video_id(item["images"][0])
            if video_id:
                video_macros[video_id].append(item)
    
    for item in micro_expressions:
        if "images" in item and item["images"]:
            video_id = extract_video_id(item["images"][0])
            if video_id:
                video_micros[video_id].append(item)
    
    logger.info(f"视频片段总数: {len(set(video_macros.keys()) | set(video_micros.keys()))}")
    
    # 计算需要的宏表情总数
    target_macro_count = int(len(micro_expressions) * target_ratio)
    logger.info(f"目标宏表情数量: {target_macro_count}")
    
    # 为每个视频片段计算采样数量
    videos_with_macros = list(video_macros.keys())
    total_macros = sum(len(video_macros[vid]) for vid in videos_with_macros)
    
    # 确保每个视频至少保留一些宏表情
    sampled_macros = []
    remaining_videos = videos_with_macros.copy()
    
    # 首先，从每个视频中至少取一些样本
    min_samples_per_video = 5
    for video_id in videos_with_macros:
        # 如果视频的宏表情少于最小采样数，全部保留
        if len(video_macros[video_id]) <= min_samples_per_video:
            sampled_macros.extend(video_macros[video_id])
            remaining_videos.remove(video_id)
        else:
            # 否则，采样最小数量
            samples = random.sample(video_macros[video_id], min_samples_per_video)
            sampled_macros.extend(samples)
            # 从原始列表中移除已采样的项
            for item in samples:
                video_macros[video_id].remove(item)
    
    logger.info(f"初始采样后的宏表情: {len(sampled_macros)}")
    
    # 计算还需要多少宏表情
    remaining_needed = target_macro_count - len(sampled_macros)
    
    # 如果还需要更多宏表情
    if remaining_needed > 0 and remaining_videos:
        # 计算每个视频应该提供的样本数
        remaining_macros = {vid: len(video_macros[vid]) for vid in remaining_videos}
        total_remaining = sum(remaining_macros.values())
        
        if total_remaining > 0:
            for video_id in remaining_videos:
                if not video_macros[video_id]:  # 如果视频没有更多宏表情了
                    continue
                    
                # 根据该视频宏表情占总数的比例计算采样数
                sample_count = min(
                    len(video_macros[video_id]),
                    max(1, int(remaining_needed * len(video_macros[video_id]) / total_remaining))
                )
                
                samples = random.sample(video_macros[video_id], sample_count)
                sampled_macros.extend(samples)
    
    logger.info(f"最终采样的宏表情: {len(sampled_macros)}")
    
    # 合并微表情和采样后的宏表情
    balanced_data = micro_expressions + sampled_macros
    
    # 随机打乱数据
    random.shuffle(balanced_data)
    
    # 写入新的jsonl文件
    with open(output_jsonl, 'w', encoding='utf-8') as f:
        for item in balanced_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    logger.info(f"平衡后的数据集总数: {len(balanced_data)}")
    logger.info(f"其中微表情: {len(micro_expressions)} 条")
    logger.info(f"其中宏表情: {len(sampled_macros)} 条")
    logger.info(f"比例(宏:微): {len(sampled_macros)/len(micro_expressions):.2f}")
    logger.info(f"处理完成! 已保存到: {output_jsonl}")

def main():
    parser = argparse.ArgumentParser(description="平衡数据集中的宏表情和微表情数量")
    parser.add_argument("--input-jsonl", type=str, required=True, help="输入的jsonl文件路径")
    parser.add_argument("--output-jsonl", type=str, required=True, help="输出的jsonl文件路径")
    parser.add_argument("--target-ratio", type=float, default=1.5, help="宏表情与微表情的目标比率")
    args = parser.parse_args()
    
    balance_expressions(args.input_jsonl, args.output_jsonl, args.target_ratio)

if __name__ == "__main__":
    main() 
