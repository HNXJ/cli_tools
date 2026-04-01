from mlx_lm import load, generate
import os
import gc

def call_native_mlx_fallback(prompt, system_context):
    """
    Directly loads the 27B Qwen model from the Warehouse and generates a response.
    Explicitly flushes VRAM after generation.
    """
    # Enforce the strict Absolute Pathing rule for MLX models
    model_path = os.path.expanduser("~/workspace/Warehouse/mlx_models/Qwen3.5-27B-Opus-Reasoning-6bit/")

    print("\n[NETWORK LOST] Injecting 27B Qwen3.5 Opus-Reasoning Model into Unified Memory via MLX...")

    try:
        model, tokenizer = load(model_path)

        # Format for the Qwen conversational template
        messages = [
            {"role": "system", "content": system_context},
            {"role": "user", "content": prompt}
        ]

        if hasattr(tokenizer, "apply_chat_template") and tokenizer.chat_template is not None:
            formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        else:
            # Standard ChatML fallback
            formatted_prompt = f"<|im_start|>system\n{system_context}<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n"

        print("[MLX NATIVE FALLBACK] Generating response...\n")
        response = generate(model, tokenizer, prompt=formatted_prompt, max_tokens=2048, verbose=False)

        # Force garbage collection to free unified memory after generation
        del model
        del tokenizer
        gc.collect()

        return response

    except Exception as e:
        return f"MLX Fallback Error: {str(e)}"

if __name__ == "__main__":
    # Test script if called directly
    from Computational.cli_tools.memory_and_logic.context_compressor import compress_cli_context
    ctx = compress_cli_context()
    res = call_native_mlx_fallback("Tell me about the current project goals.", ctx)
    print(res)
