"""6.1 | 규칙 기반 메시지 분류. 머신러닝 학습을 수행하지 않습니다."""

def classify_message(message):
    keywords = ["무료", "당첨", "광고"]
    for word in keywords:
        if word in message:
            return "광고 의심"
    return "일반 메시지"

messages = [
    "오늘 수업 자료를 공유합니다.",
    "무료 쿠폰에 당첨되셨습니다.",
    "무료 공개 강의 안내입니다.",
]

for message in messages:
    print(message, "→", classify_message(message))

print("\n확인 활동: keywords에 '할인'을 추가하고 메시지를 다시 분류해 보세요.")
