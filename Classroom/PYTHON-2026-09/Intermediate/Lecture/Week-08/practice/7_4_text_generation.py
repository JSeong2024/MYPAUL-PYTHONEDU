"""7.4 — 공개 소형 언어 모델(SmolLM2-135M-Instruct)을 이용한 텍스트 생성.

처음 실행할 때 Hugging Face에서 가중치를 다운로드하므로 인터넷이 필요합니다.
주로 영어로 학습된 소형 모델이므로 영어 프롬프트를 권장합니다.
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "HuggingFaceTB/SmolLM2-135M-Instruct"
PROMPT = "List three simple ways to save electricity at home. Keep each tip short."
MAX_NEW_TOKENS = 70

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Device:", device)
print("첫 실행 시 공개 모델을 다운로드합니다.")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID).to(device)
model.eval()

messages = [{"role": "user", "content": PROMPT}]
input_ids = tokenizer.apply_chat_template(
    messages, tokenize=True, add_generation_prompt=True,
    return_tensors="pt"
).to(device)

with torch.inference_mode():
    generated_ids = model.generate(
        input_ids,
        max_new_tokens=MAX_NEW_TOKENS,
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
    )

new_ids = generated_ids[0][input_ids.shape[-1]:]
answer = tokenizer.decode(new_ids, skip_special_tokens=True).strip()
print("Prompt:", PROMPT)
print("Generated text:\n", answer)
print("주의: 생성 결과는 사실 확인이 필요할 수 있습니다.")
