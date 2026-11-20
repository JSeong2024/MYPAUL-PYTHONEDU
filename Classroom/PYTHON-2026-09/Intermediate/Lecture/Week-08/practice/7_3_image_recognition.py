"""7.3: ImageNet 사전 학습 MobileNetV3로 사진 분류.

처음 실행할 때 PyTorch Hub 예제 이미지/모델 가중치를 내려받으므로 인터넷 필요.
UPLOAD_OWN_IMAGE=True로 변경하면 Colab에서 직접 이미지를 업로드할 수 있음.
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
    from google.colab import files
    uploaded = files.upload()
    if not uploaded:
        raise ValueError("이미지 파일을 업로드해야 합니다.")
    img_path = Path(next(iter(uploaded)))
else:
    img_path = out_dir / "sample_dog.jpg"
    if not img_path.is_file():
        print("PyTorch Hub 공개 예제 이미지를 다운로드합니다.")
        urlretrieve(SAMPLE_IMAGE_URL, img_path)

image = Image.open(img_path).convert("RGB")
weights = MobileNet_V3_Small_Weights.DEFAULT
preprocess = weights.transforms()    # 모델에 맞춘 Resize, Crop, Normalize
model = mobilenet_v3_small(weights=weights)
model.eval()                          # 추론 모드

with torch.inference_mode():
    logits = model(preprocess(image).unsqueeze(0))
    probs = logits.softmax(dim=1)[0] # 1000개 클래스에 대한 점수 분포
    values, indices = torch.topk(probs, 5)

labels = weights.meta["categories"]
print("Top 5 predictions:")
for rank, (idx, value) in enumerate(zip(indices.tolist(), values.tolist()), 1):
    print(f"{rank}. {labels[idx]}: {value:.1%}")

fig, (ax_img, ax_bar) = plt.subplots(1, 2, figsize=(11.6, 4.4), dpi=150)
ax_img.imshow(image)
ax_img.set_title("Input Image")
ax_img.axis("off")
names = [labels[i] for i in indices.tolist()]
ax_bar.barh(names[::-1], [x * 100 for x in values.tolist()[::-1]])
ax_bar.set_xlabel("Softmax Score (%)")
ax_bar.set_title("Top 5 Predicted Classes")
ax_bar.set_xlim(0, 100)
fig.tight_layout()
fig.savefig(out_dir / "7_3_image_prediction.png", facecolor="white", dpi=160)
plt.show()
print("모델의 점수는 항상 현실의 정답 확률을 의미하지는 않습니다.")
