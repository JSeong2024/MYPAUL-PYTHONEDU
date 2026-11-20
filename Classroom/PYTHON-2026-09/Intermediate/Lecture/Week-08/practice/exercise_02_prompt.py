"""Exercise 02 — 텍스트 생성 프롬프트 분석.

7_4_text_generation.py의 PROMPT와 MAX_NEW_TOKENS를 변경하고 결과를 비교함.
"""
prompts = [
    "Explain recycling in one short sentence.",
    "Explain recycling to an eight-year-old child in two short sentences.",
    "Give three examples of recycling at school. Use bullet points.",
]
for number, prompt in enumerate(prompts, 1):
    print(f"{number}. {prompt}")
print("세 프롬프트를 7_4_text_generation.py에 각각 입력하여 생성 결과를 비교하세요.")
