#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
处理SAMM数据集，根据微表情标注生成训练数据
"""

import os
import json
import pandas as pd
from tqdm import tqdm
import random
import glob
import argparse

# 文件路径
EXCEL_PATH = '/nthfs/ustc/zhuls24/code/MM-MEGC-2025/data/SAMM/SAMM_LongVideos_V3_Release.xlsx'
VIDEO_DIR = '/nthfs/ustc/zhuls24/code/MM-MEGC-2025/data/SAMM/SAMM_longvideos'
OUTPUT_DIR = '/nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/data_1img'
OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'samm_me_train.jsonl')
TEST_OUTPUT_PATH = os.path.join(OUTPUT_DIR, 'samm_me_test.jsonl')

# 确保输出目录存在
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 用户提问的多样化模板
USER_PROMPTS = [
    "Is the expression shown in the figure a micro-expression or a macro-expression?",
    # "Is this a micro-expression or macro-expression?",
    # "Classify this facial expression as micro or macro.",
    # "What type of facial expression is this: micro or macro?",
    # "Is this facial expression categorized as micro or macro?",
    # "Determine if this is a micro-expression or a macro-expression.",
    # "Can you tell if this is a micro or macro facial expression?",
    # "Identify whether this facial expression is micro or macro.",
    # "Would you classify this as a micro or macro expression?",
    # "Does this represent a micro-expression or a macro-expression?",
    # "Is the facial movement shown here a micro or macro expression?"
]

def get_image_paths(subject, code, onset, offset):
    """
    获取给定subject、code以及onset到offset之间的所有图片路径
    
    参数：
    subject - 被试ID
    code - 诱导代码
    onset - 表情开始帧
    offset - 表情结束帧
    
    返回：
    包含所有图片路径的列表
    """
    # 格式化subject和code
    subject_str = f"{subject:03d}"
    folder_path = os.path.join(VIDEO_DIR, f"{subject_str}_{code}")
    
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"警告: 文件夹不存在 - {folder_path}")
        return []
    
    # 获取该文件夹中的所有图片
    image_pattern = os.path.join(folder_path, f"{subject_str}_{code}_*.jpg")
    all_images = glob.glob(image_pattern)
    
    # 筛选onset到offset之间的图片
    selected_images = []
    for img_path in all_images:
        try:
            # 从文件名中提取图片ID
            img_id = int(os.path.basename(img_path).split('_')[-1].split('.')[0])
            if onset <= img_id <= offset:
                selected_images.append(img_path)
        except ValueError:
            print(f"警告: 无法解析图片ID - {img_path}")
    
    # 排序图片路径
    selected_images.sort(key=lambda x: int(os.path.basename(x).split('_')[-1].split('.')[0]))
    return selected_images

def check_and_fix_paths(image_paths):
    """
    检查并修复图片路径
    
    参数：
    image_paths - 图片路径列表
    
    返回：
    修复后的图片路径列表
    """
    fixed_paths = []
    for path in image_paths:
        # 确保路径存在
        if os.path.exists(path):
            fixed_paths.append(path)
        else:
            # 尝试修复路径（例如检查常见的扩展名）
            alt_extensions = ['.jpg', '.jpeg', '.png']
            for ext in alt_extensions:
                alt_path = os.path.splitext(path)[0] + ext
                if os.path.exists(alt_path):
                    fixed_paths.append(alt_path)
                    print(f"已修复路径: {path} -> {alt_path}")
                    break
    
    return fixed_paths

def generate_data(sample_count=None, max_frames=5, min_frames=3):
    """
    生成训练和测试数据，每条数据仅包含一张图片
    
    参数：
    sample_count - 如果指定，则只处理指定数量的样本（用于测试）
    max_frames - 每个样本最多使用的帧数（此参数在单图片模式下不再使用）
    min_frames - 每个样本至少需要的帧数（此参数在单图片模式下不再使用）
    """
    # 读取Excel文件
    print(f"读取 {EXCEL_PATH}...")
    # 从第十行开始读取Excel文件，跳过前9行的标题或说明内容
    df = pd.read_excel(EXCEL_PATH, skiprows=9)
    
    # 准备数据列表
    all_data = []
    
    # 遍历每一行标注
    print("处理标注数据...")
    for _, row in tqdm(df.iterrows(), total=len(df)):
        try:
            # 提取信息
            subject = int(row['Subject'])
            code = row['Inducement Code']
            onset = int(row['Onset'])
            offset = int(row['Offset'])
            me_type = str(row['Type'])
            
            # 检查是否为微表情或宏表情
            if me_type not in ['Micro - 1/2', 'Macro']:
                continue
                
            # 获取图片路径
            image_paths = get_image_paths(subject, code, onset, offset)
            
            # 检查和修复图片路径
            image_paths = check_and_fix_paths(image_paths)
            
            if not image_paths:
                continue
            
            # 随机选择一个用户提示
            # user_prompt = random.choice(USER_PROMPTS)
            user_prompt = USER_PROMPTS[0]
            
            # 为每张图片创建一条数据
            for img_path in image_paths:
                data_item = {
                    "messages": [
                        {"role": "user", "content": "<image>" + user_prompt},
                        {"role": "assistant", "content": me_type}
                    ],
                    "images": [img_path],  # 每条数据只包含一张图片
                    # "metadata": {
                    #     "subject": subject,
                    #     "code": code,
                    #     "onset": onset,
                    #     "offset": offset,
                    #     "type": me_type,
                    #     "frame_id": int(os.path.basename(img_path).split('_')[-1].split('.')[0])
                    # }
                }
                
                all_data.append(data_item)
            
            # 如果已经收集了足够的样本，则停止
            if sample_count and len(all_data) >= sample_count:
                break
        
        except Exception as e:
            print(f"处理行时出错: {e}")
            print(f"行数据: {row}")
    
    print(f"共处理 {len(all_data)} 条数据")
    
    # 统计微表情/宏表情的分布
    micro_count = sum(1 for item in all_data if item['messages'][1]['content'] == 'Micro - 1/2')
    macro_count = sum(1 for item in all_data if item['messages'][1]['content'] == 'Macro')
    print(f"微表情(Micro - 1/2): {micro_count}, 宏表情(Macro): {macro_count}")
    
    # 不划分测试集，所有数据都作为训练集
    random.shuffle(all_data)
    train_data = all_data
    test_data = []  # 空测试集
    # 保存数据
    print(f"保存训练数据到 {OUTPUT_PATH}...")
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print(f"保存测试数据到 {TEST_OUTPUT_PATH}...")
    with open(TEST_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        for item in test_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    print("完成!")
    print(f"训练集大小: {len(train_data)}")
    print(f"测试集大小: {len(test_data)}")
    print(f"训练集中微表情: {sum(1 for item in train_data if item['messages'][1]['content'] == 'Micro - 1/2')}")
    print(f"训练集中宏表情: {sum(1 for item in train_data if item['messages'][1]['content'] == 'Macro')}")
    print(f"测试集中微表情: {sum(1 for item in test_data if item['messages'][1]['content'] == 'Micro - 1/2')}")
    print(f"测试集中宏表情: {sum(1 for item in test_data if item['messages'][1]['content'] == 'Macro')}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="处理SAMM数据集生成微表情/宏表情分类任务数据")
    parser.add_argument("--sample", type=int, help="仅处理指定数量的样本（用于测试）")
    parser.add_argument("--max-frames", type=int, default=5, help="每个样本最多使用的帧数")
    parser.add_argument("--min-frames", type=int, default=3, help="每个样本至少需要的帧数")
    args = parser.parse_args()
    
    generate_data(sample_count=args.sample, max_frames=args.max_frames, min_frames=args.min_frames)
