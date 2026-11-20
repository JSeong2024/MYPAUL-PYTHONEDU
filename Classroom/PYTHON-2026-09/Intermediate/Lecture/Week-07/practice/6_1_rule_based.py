"""6.1 | 규칙 기반 메시지 분류: 머신러닝이 아닌 비교 예제."""


def classify_message(message: str) -> str:
    keywords = ["무료", "당첨", "광고"]
    for word in keywords:
        if word in message:
            return "광고 의심"
    return "일반 메시지"


if __name__ == "__main__":
    messages = [
        "오늘 수업 자료를 공유합니다.",
        "무료 쿠폰에 당첨되셨습니다.",
        "무료 공개 강의 안내입니다.",
        "내일 오전 10시에 만나자!",
    ]
    for message in messages:
        print(f"{message} → {classify_message(message)}")
