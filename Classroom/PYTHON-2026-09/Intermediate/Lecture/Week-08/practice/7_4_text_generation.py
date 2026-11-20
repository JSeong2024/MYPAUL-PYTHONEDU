"""7.4: Hugging Face 공개 소형 언어 모델로 텍스트 생성.

모델: HuggingFaceTB/SmolLM2-135M-Instruct (주로 영어). 첫 실행 인터넷 필요.
작은 모델이므로 일반 상용 AI 수준의 정확도/품질을 기대하면 안 됨.
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "HuggingFaceTB/SmolLM2-135M-Instruct"
PROMPT = "List three simple ways to save electricity at home. Keep each tip short."
MAX_NEW_TOKENS = 70

device = "cuda" if torch.cuda.is_available() else "cpu"
print("Device:", device)
print("모델을 처음 실행하는 경우 가중치를 다운로드합니다.")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID).to(device)
model.eval()

messages = [{"role": "user", "content": PROMPT}]
# 역할 정보 등을 모델이 기대하는 입력 형식으로 변환
input_ids = tokenizer.apply_chat_template(
    messages, tokenize=True, add_generation_prompt=True,
    return_tensors="pt"
).to(device)
print("Input token count:", input_ids.shape[-1])

with torch.inference_mode():
    output_ids = model.generate(
        input_ids,
        max_new_tokens=MAX_NEW_TOKENS,
        do_sample=False,             # 재현하기 쉬운 탐욕적 생성
        pad_token_id=tokenizer.eos_token_id,
    )

# 입력 문장 제외, 새롭게 생성된 토큰만 디코딩
new_tokens = output_ids[0][input_ids.shape[-1]:]
answer = tokenizer.decode(new_tokens, skip_special_tokens=True)
print("\n[Prompt]", PROMPT)
print("\n[Generated Text]\n", answer.strip())
print("\n주의: 생성 결과는 검증되지 않은 문장일 수 있습니다.")
