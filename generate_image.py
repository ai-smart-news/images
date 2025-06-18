import os
from datetime import datetime
from g4f.client import Client as Client_g4f
from gradio_client import Client
import shutil
from PIL import Image

# === Step 1: 用 g4f GPT-4o 生成 Fantasy prompt ===
client = Client_g4f()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": (
                "請幫我生成一句適合 AI 繪圖的 fantasy prompt，英文，一句話即可，風格可以是魔法、精靈、史詩場景、奇幻生物或幻想藝術。"
            )
        }
    ]
)

image_prompt = response.choices[0].message.content.strip()
print("🎨 生成的 Prompt:", image_prompt)

# === Step 2: 用 HuggingFace 模型生成圖片 ===

client = Client("black-forest-labs/FLUX.1-dev")
result = client.predict(
        prompt=image_prompt,
        seed=0,
        randomize_seed=True,
        width=1080,
        height=1920,
        guidance_scale=3.5,
        num_inference_steps=28,
        api_name="/infer"
)

# === Step 3: 檔案命名與儲存路徑設定 ===
today = datetime.now().strftime("%Y_%m_%d")
folder_path = os.path.join("images", today)
os.makedirs(folder_path, exist_ok=True)

# 找出今天已經存在的圖片數量，確保檔名遞增
existing_files = [f for f in os.listdir(folder_path) if f.endswith(".png")]
image_index = len(existing_files) + 1

# 指定儲存檔名
filename = f"{today}_{image_index:02}.png"
output_path = os.path.join(folder_path, filename)

# 將 webp 轉成 PNG 存起來
with Image.open(result[0]) as img:
    img.convert("RGB").save(output_path, "PNG")

print(f"✅ 圖片已轉成 PNG 並儲存至：{output_path}")


# === Step 5: 更新 README.md 預覽圖片 ===
readme_path = os.path.join(folder_path, "README.md")

# 取得該資料夾內所有 PNG 圖片（排序確保順序）
image_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".png")])

# 產生 markdown 格式的圖片預覽
readme_lines = ["# Generated Images\n"]
for image_file in image_files:
    readme_lines.append(f'<img src="{image_file}" width="100"/>')

# 寫入 README.md
with open(readme_path, "w") as f:
    f.write("\n\n".join(readme_lines))

print(f"📄 README.md 已更新：{readme_path}")