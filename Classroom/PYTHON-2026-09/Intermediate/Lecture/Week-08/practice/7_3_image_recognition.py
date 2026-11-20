"""7.3 — MobileNetV3-Small 사전 학습 모델을 이용한 이미지 분류.

첫 실행 시 공개 샘플 사진과 pretrained 가중치를 내려받으므로 인터넷 연결이 필요합니다.
UPLOAD_OWN_IMAGE=True로 바꾸면 Colab에서 직접 이미지 파일을 선택할 수 있습니다.
"""
from pathlib import Path
from urllib.request import urlretrieve

import matplotlib.pyplot as plt
import torch
from PIL import Image
from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small

UPLOAD_OWN_IMAGE = False
SAMPLE_IMAGE_URL = "https://raw.githubusercontent.com/pytorch/hub/master/images/dog.jpg"

out_dir = (Path(__file__).resolve().parents[1] / "assets") if "__file__" in globals() else Path("assets")
out_dir.mkdir(parents=True, exist_ok=True)

if UPLOAD_OWN_IMAGE:
    try:
        from google.colab import files
    except ImportError as exc:
        raise RuntimeError("사진 업로드는 Google Colab에서 실행하거나 코드를 로컬 경로로 수정하세요.") from exc
    uploaded = files.upload()
    if not uploaded:
        raise ValueError("분류할 이미지를 업로드하세요.")
    img_path = Path(next(iter(uploaded)))
else:
    img_path = out_dir / "sample_dog.jpg"
    if not img_path.is_file():
        print("공개 예제 사진 다운로드 중...")
        urlretrieve(SAMPLE_IMAGE_URL, img_path)

image = Image.open(img_path).convert("RGB")
weights = MobileNet_V3_Small_Weights.DEFAULT
model = mobilenet_v3_small(weights=weights)
model.eval()

input_tensor = weights.transforms()(image).unsqueeze(0)
with torch.inference_mode():
    logits = model(input_tensor)
    scores = logits.softmax(dim=1)[0]
    top_scores, top_ids = torch.topk(scores, k=5)

classes = weights.meta["categories"]
names = [classes[i] for i in top_ids.tolist()]
values = top_scores.tolist()

print("ImageNet Top-5 Prediction")
for rank, (name, score) in enumerate(zip(names, values), 1):
    print(f"{rank}. {name}: {score:.1%}")

fig, (ax_image, ax_score) = plt.subplots(1, 2, figsize=(12.2, 5), dpi=170,
                                        gridspec_kw={"width_ratios": [1, 1.3]})
ax_image.imshow(image)
ax_image.set_title("Input Image")
ax_image.axis("off")
ax_score.barh(names[::-1], [v * 100 for v in values[::-1]])
ax_score.set_title("Top 5 Predictions")
ax_score.set_xlabel("Softmax Score (%)")
ax_score.set_xlim(0, 100)
ax_score.grid(axis="x", alpha=0.18)
ax_score.set_axisbelow(True)
fig.tight_layout()
result = out_dir / "7_3_image_prediction.png"
fig.savefig(result, facecolor="white", dpi=170, bbox_inches="tight")
plt.show()
print("그래프 저장:", result)
print("참고: Softmax 출력은 실제 정답일 확률을 보장하지 않습니다.")
