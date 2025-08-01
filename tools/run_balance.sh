#!/bin/bash

# 设置输入和输出路径
INPUT_JSONL="/nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/samm_processed_data/samm_me_train_rgb.jsonl"
OUTPUT_DIR="/nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/samm_processed_data"
OUTPUT_JSONL="${OUTPUT_DIR}/samm_me_train_balanced.jsonl"

# 创建输出目录
mkdir -p ${OUTPUT_DIR}

echo "开始平衡宏表情和微表情数量..."

# 使用默认比例1.5（即宏表情数量为微表情的1.5倍）
python balance_macro_micro.py \
    --input-jsonl ${INPUT_JSONL} \
    --output-jsonl ${OUTPUT_JSONL} \
    --target-ratio 1.5

# 如果需要自定义比例，可以取消下面的注释并修改比例值
# python balance_macro_micro.py \
#     --input-jsonl ${INPUT_JSONL} \
#     --output-jsonl ${OUTPUT_JSONL} \
#     --target-ratio 1.2

echo "处理完成! 平衡后的数据保存在: ${OUTPUT_JSONL}" 
