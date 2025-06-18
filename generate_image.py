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
                """Please create a single-sentence AI art prompt, written in English, in the same style as the following example. The goal is to describe a rich, vivid, and cinematic digital artwork, suitable for use with an AI image generator like Midjourney, DALL·E, or Stable Diffusion.

Example prompt (DO NOT repeat it, just follow its level of detail and style):
"This digital artwork, created in a realistic, semi-realistic style, portrays a futuristic, cybernetic female warrior standing confidently in the center of the frame..."

Now, generate a similar prompt — same level of descriptive detail, same structure, but completely different concept. It should describe:
- A different subject or character (not the same warrior)
- A new setting or background
- A clear artistic style (e.g., cyberpunk, fantasy, horror, surreal, etc.)
- Visual atmosphere (fog, light, energy, emotion)
- Clothing, accessories, or weapons (if any)
- Specific colors and lighting

Make sure it's elegant, vivid, and usable directly as an AI image generation prompt."""
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

# 產生 markdown 圖片區塊，每 10 張換一行
readme_lines = ["# Generated Images", ""]
row = []

for i, image_file in enumerate(image_files, 1):
    row.append(f'<img src="{image_file}" width="100"/>')
    if i % 10 == 0:
        readme_lines.append(" ".join(row))
        row = []

# 加上最後一行（不足 10 張也要顯示）
if row:
    readme_lines.append(" ".join(row))

# 寫入 README.md
with open(readme_path, "w") as f:
    f.write("\n\n".join(readme_lines))

print(f"📄 README.md 已更新：{readme_path}")
