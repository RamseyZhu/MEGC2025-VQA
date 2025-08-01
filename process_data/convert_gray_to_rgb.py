#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
将灰度图像转换为RGB图像的预处理脚本
"""

import os
import json
import argparse
from PIL import Image
from tqdm import tqdm
import shutil
import logging
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def convert_grayscale_to_rgb(input_path, output_path):
    """
    将灰度图像转换为RGB图像
    
    Args:
        input_path: 输入图像路径
        output_path: 输出图像路径
    """
    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 打开并转换图像
        with Image.open(input_path) as img:
            if img.mode != 'RGB':
                # 转换为RGB
                img_rgb = img.convert('RGB')
                # 保存转换后的图像
                img_rgb.save(output_path)
                logger.debug(f"转换图像: {input_path} -> {output_path}")
            else:
                # 已经是RGB，直接复制
                shutil.copy(input_path, output_path)
                logger.debug(f"复制RGB图像: {input_path} -> {output_path}")
        return True
    except Exception as e:
        logger.error(f"处理图像 {input_path} 时出错: {str(e)}")
        return False

def process_jsonl(input_jsonl, output_jsonl, output_img_dir):
    """
    处理jsonl文件，更新图像路径并转换图像
    
    Args:
        input_jsonl: 输入的jsonl文件路径
        output_jsonl: 输出的jsonl文件路径
        output_img_dir: 输出图像目录
    """
    # 确保输出目录存在
    os.makedirs(output_img_dir, exist_ok=True)
    os.makedirs(os.path.dirname(output_jsonl), exist_ok=True)
    
    # 读取原始jsonl文件
    data = []
    with open(input_jsonl, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    
    processed_count = 0
    total_count = len(data)
    logger.info(f"开始处理 {total_count} 条数据...")
    
    # 处理每一条数据
    new_data = []
    for item in tqdm(data, desc="转换图像"):
        new_item = item.copy()
        
        # 处理图像列表
        if "images" in new_item:
            new_images = []
            for img_path in new_item["images"]:
                # 构建新的图像路径
                rel_path = os.path.relpath(img_path, "/nthfs/ustc/zhuls24/code/MM-MEGC-2025")
                new_img_path = os.path.join(output_img_dir, os.path.basename(rel_path))
                
                # 转换图像
                if convert_grayscale_to_rgb(img_path, new_img_path):
                    new_images.append(new_img_path)
                else:
                    new_images.append(img_path)  # 如果转换失败，使用原始路径
            
            new_item["images"] = new_images
        
        new_data.append(new_item)
        processed_count += 1
    
    # 写入新的jsonl文件
    with open(output_jsonl, 'w', encoding='utf-8') as f:
        for item in new_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    logger.info(f"处理完成! 处理了 {processed_count} 条数据，保存到 {output_jsonl}")
    return new_data

def main():
    parser = argparse.ArgumentParser(description="灰度图像转RGB预处理工具")
    parser.add_argument("--input-jsonl", type=str, required=True, help="输入的jsonl文件路径")
    parser.add_argument("--output-jsonl", type=str, required=True, help="输出的jsonl文件路径")
    parser.add_argument("--output-img-dir", type=str, required=True, help="输出图像目录")
    args = parser.parse_args()
    
    process_jsonl(args.input_jsonl, args.output_jsonl, args.output_img_dir)

if __name__ == "__main__":
    main() 
