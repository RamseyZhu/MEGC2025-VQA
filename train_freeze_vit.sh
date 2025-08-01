# MAX_PIXELS=1003520 \
MASTER_PORT=29501 \
CUDA_VISIBLE_DEVICES=8,9 \
NPROC_PER_NODE=2 \
swift sft \
    --model /nthfs/ustc/zhuls24/open_ckpt/Qwen/Qwen2.5-VL-7B-Instruct \
    --dataset /nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/samm_processed_data/samm_me_train_balanced.jsonl \
    --train_type lora \
    --torch_dtype bfloat16 \
    --num_train_epochs 3 \
    --per_device_train_batch_size 8 \
    --per_device_eval_batch_size 2 \
    --learning_rate 1e-5 \
    --lora_rank 8 \
    --lora_alpha 32 \
    --target_modules all-linear \
    --freeze_vit true \
    --init_weights true \
    --eval_steps 100 \
    --save_steps 100 \
    --save_total_limit 5 \
    --logging_steps 5 \
    --max_length 2048 \
    --output_dir /nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/output_qwen25vl_7b/freeze_vit \
    --warmup_ratio 0.05 \
    --dataloader_num_workers 8 \
    --gradient_checkpointing_kwargs '{"use_reentrant": false}' \
