# Swift微调脚本，使用多模态大模型进行微调
CUDA_VISIBLE_DEVICES=0 MAX_PIXELS=1003520 swift sft \
    # 模型类型，使用Qwen2.5-VL大模型
    --model_type qwen2_5 \
    # 预训练模型的路径，指向Qwen2.5-VL-7B-Instruct模型
    --model /nthfs/ustc/zhuls24/open_ckpt/Qwen/Qwen2.5-VL-7B-Instruct \
    # 训练数据集的路径，包含图像和文本数据的jsonl文件
    --dataset /nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/data_1img/samm_me_train.jsonl \
    # 训练类型，使用LoRA参数高效微调技术
    --train_type lora \
    # 注意力实现方式，使用原生torch的SDPA注意力机制
    --attn_impl sdpa \
    # 是否冻结视觉编码器(Vision Transformer)部分，这里设置为不冻结
    --freeze_vit false \
    # 是否冻结视觉-语言对齐模块，这里设置为不冻结
    --freeze_aligner false \
    # 是否冻结大语言模型部分，这里设置为不冻结
    --freeze_llm false \
    # --freeze_parameters_ratio 0. \ # 冻结参数的比例，full训练模式下可以设置
    # 每个GPU上的训练批次大小
    --per_device_train_batch_size 1 \
    # 每个GPU上的评估批次大小
    --per_device_eval_batch_size 2 \
    # 数据集分割比例，10%用于评估
    --split_dataset_ratio 0.1 \
    # 模型输出保存目录
    --output_dir qwen2.5vl_samm_me \
    # 最大训练步数
    --max_steps 1500 \
    # 每训练多少步保存一次检查点
    --save_steps 100 \
    # 每训练多少步进行一次评估
    --eval_steps 100 \
    # 最多保存的检查点数量，超过会删除旧的
    --save_total_limit 2 \
    # 每多少步记录一次日志
    --logging_steps 10 \
    # 随机种子，确保实验可重复性
    --seed 42 \
    # 学习率设置
    --learning_rate 1e-4 \
    # 是否初始化权重，true表示使用初始化策略
    --init_weights true \
    # LoRA的秩，决定了可训练参数的数量，越大参数越多
    --lora_rank 8 \
    # LoRA的缩放参数，控制LoRA更新的影响程度
    --lora_alpha 32 \
    # Adam优化器的beta1参数
    --adam_beta1 0.9 \
    # Adam优化器的beta2参数
    --adam_beta2 0.95 \
    # Adam优化器的epsilon值，防止除零错误
    --adam_epsilon 1e-08 \
    # 权重衰减系数，用于L2正则化防止过拟合
    --weight_decay 0.1 \
    # 梯度累积步数，相当于增大批次大小，节省显存
    --gradient_accumulation_steps 8 \
    # 梯度裁剪阈值，防止梯度爆炸
    --max_grad_norm 1 \
    # 学习率调度器类型，使用余弦退火策略
    --lr_scheduler_type cosine \
    # 学习率预热阶段占总训练步数的比例
    --warmup_ratio 0.05 \
    # 学习率预热步数，与warmup_ratio二选一，这里设为0表示使用比例
    --warmup_steps 0 \
    # 是否使用梯度检查点技术来节省显存，代价是计算时间增加
    --gradient_checkpointing false
