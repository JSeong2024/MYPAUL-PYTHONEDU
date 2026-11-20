"""Exercise 04 — 세 가지 Prompt와 토큰 제한에 따라 생성 결과를 비교하세요.

모델을 한 번만 로드한 뒤 여러 문장을 순차 생성합니다.
인터넷을 통해 공개 모델을 다운로드해야 하므로 Colab에서 실행하는 것을 권장합니다.
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "HuggingFaceTB/SmolLM2-135M-Instruct"
PROMPTS = [
    "Explain recycling in one short sentence.",
    "Explain recycling to an eight-year-old child in two short sentences.",
    "Give three examples of recycling at school. Use bullet points.",
]
TOKEN_LIMITS = [30, 70]

device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID).to(device)
model.eval()

for limit in TOKEN_LIMITS:
    print(f"\n======== MAX_NEW_TOKENS={limit} ========")
    for index, prompt in enumerate(PROMPTS, 1):
        input_ids = tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}],
            tokenize=True, add_generation_prompt=True,
            return_tensors="pt",
        ).to(device)
        with torch.inference_mode():
            generated_ids = model.generate(
                input_ids, max_new_tokens=limit, do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
        new_ids = generated_ids[0][input_ids.shape[-1]:]
        answer = tokenizer.decode(new_ids, skip_special_tokens=True).strip()
        print(f"\n[{index}] Prompt: {prompt}")
        print("Generated:", answer)
print("문장 길이·대상·형식 요구를 얼마나 충실하게 따랐는지 비교해 보세요.")
