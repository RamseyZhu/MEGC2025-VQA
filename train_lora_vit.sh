# export NCCL_P2P_LEVEL=NVL \
# MAX_NUM=12 \
# CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
# NPROC_PER_NODE=4 \
# CUDA_LAUNCH_BLOCKING=1 \
# CUDA_VISIBLE_DEVICES=8,9 \
CUDA_VISIBLE_DEVICES=1,3 \
NPROC_PER_NODE=2 \
swift sft \
    --model /nthfs/ustc/zhuls24/open_ckpt/Qwen/Qwen2.5-VL-7B-Instruct \
    --dataset /nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/samm_processed_data/samm_me_train_balanced.jsonl \
    --train_type lora \
    --torch_dtype bfloat16 \
    --num_train_epochs 3 \
    --per_device_train_batch_size 4 \
    --per_device_eval_batch_size 1 \
    --output_dir /nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/output_qwen25vl_7b/lora_vit_balence \
    --save_steps 100 \
    --attn_impl sdpa \
    --eval_steps 100 \
    --save_total_limit 5 \
    --logging_steps 10 \
    --seed 42 \
    --learning_rate 1e-4 \
    --init_weights true \
    --lora_rank 16 \
    --lora_alpha 32 \
    --target_modules all-linear \
    --freeze_vit false \
    --freeze_aligner false \
    --eval_steps 100 \
    --save_steps 100 \
    --save_total_limit 5 \
    --logging_steps 5 \
    --warmup_ratio 0.05 \
    --dataloader_num_workers 8 \
    --gradient_checkpointing_kwargs '{"use_reentrant": false}'
