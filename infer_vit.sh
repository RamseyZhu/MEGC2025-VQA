MASTER_PORT=29502 \
CUDA_VISIBLE_DEVICES=3 \
NPROC_PER_NODE=1 MAX_PIXELS=1003520 swift infer \
    --ckpt_dir /nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/output_qwen25vl_7b/lora_vit_balence/v0-20250619-214808/checkpoint-1300-merged \
    --max_new_tokens 512 \
    --temperature 0 \
    --val_dataset /nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/test_data/str_test.jsonl \
    --result_path /nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/output_infer/lora_vit_balence_output_1300.jsonl \
    --max_batch_size 1 \
    --infer_backend vllm \
    --max_model_len 2048 \
    --gpu_memory_utilization 0.7 \

# MASTER_PORT=29503 \
# CUDA_VISIBLE_DEVICES=1 \
# NPROC_PER_NODE=1 MAX_PIXELS=1003520 swift infer \
#     --ckpt_dir /nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/output_qwen25vl_7b/freeze_vit/v2-20250619-220612/checkpoint-5475-merged \
#     --max_new_tokens 512 \
#     --temperature 0 \
#     --val_dataset /nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/test_data/str_test.jsonl \
#     --result_path /nthfs/ustc/zhuls24/code/MM-MEGC-2025/code/STR_swift/output_infer/freeze_vit_output_5475.jsonl \
#     --max_batch_size 1 \
#     --infer_backend vllm \
#     --max_model_len 2048 \
#     --gpu_memory_utilization 0.7 \
#     --enforce_eager true
    # --attn_impl flash_attn \
