#!/bin/bash

# 创建输出目录
PROCESSED_DIR="/nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/processed_data"
RGB_IMAGES_DIR="${PROCESSED_DIR}/rgb_images"
OUTPUT_TRAIN_JSONL="${PROCESSED_DIR}/samm_me_train_rgb.jsonl"
OUTPUT_TEST_JSONL="${PROCESSED_DIR}/samm_me_test_rgb.jsonl"

mkdir -p ${PROCESSED_DIR}
mkdir -p ${RGB_IMAGES_DIR}

# 处理训练数据
echo "处理训练数据..."
python convert_gray_to_rgb.py \
    --input-jsonl /nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/data_1img/samm_me_train.jsonl \
    --output-jsonl ${OUTPUT_TRAIN_JSONL} \
    --output-img-dir ${RGB_IMAGES_DIR}/train

# # 处理测试数据
# echo "处理测试数据..."
# python convert_gray_to_rgb.py \
#     --input-jsonl /nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/data_1img/samm_me_test.jsonl \
#     --output-jsonl ${OUTPUT_TEST_JSONL} \
#     --output-img-dir ${RGB_IMAGES_DIR}/test

# 更新训练脚本中的数据路径
echo "更新训练脚本..."
# 使用sed命令替换train_refine.sh文件中的数据集路径
# 将原始数据集路径替换为处理后的RGB图像数据集路径
# -i参数表示直接在原文件中进行修改
# s命令用于替换，g表示全局替换（替换所有匹配项）
# sed -i "s|--dataset /nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/data_1img/samm_me_train.jsonl|--dataset ${OUTPUT_TRAIN_JSONL}|g" train_refine.sh

echo "预处理完成! 现在可以运行 train_refine.sh 进行训练了。" 
