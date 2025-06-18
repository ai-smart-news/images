import os
import random
import json
from datetime import datetime
from g4f.client import Client as Client_g4f
from gradio_client import Client as Client_gradio
from PIL import Image

# === Step 1: 用 g4f GPT-4o 生成高品質繪圖 prompt ===
client = Client_g4f()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": (
                """Please write a single-sentence AI image generation prompt that is rich in visual detail and structured like a cinematic description. This prompt will be used with a high-resolution, highly descriptive model such as FLUX, so the output should be exceptionally vivid and immersive.

The prompt should include:
- A clear subject or character
- The character’s appearance
- Artistic style or mood (realistic, sci-fi, mechanical, fantasy, surreal, etc.)
- Environment or setting details
- Specific lighting and color schemes
- Clothing, accessories, or technology
- Motion, atmosphere, or effects

Structure it as a single long sentence. No camera tags. Make it imaginative and visual.
"""
            )
        }
    ]
)

image_prompt = response.choices[0].message.content.strip()
print("🎨 Prompt:", image_prompt)

# === Step 2: 定義並選取圖片尺寸（所有尺寸皆 ≥ 1024） ===
image_sizes = [
    {"name": "portrait", "width": 1024, "height": 1536},
    {"name": "landscape", "width": 1280, "height": 1024},
    {"name": "square", "width": 1024, "height": 1024},
    {"name": "ultra-wide", "width": 1920, "height": 1024},
    {"name": "vertical-hd", "width": 1080, "height": 1920}
]

size_choice = random.choice(image_sizes)
width = size_choice["width"]
height = size_choice["height"]

# === Step 3: 調用 FLUX Space 模型產圖 ===
client = Client_gradio("black-forest-labs/FLUX.1-dev")

result = client.predict(
    prompt=image_prompt,
    seed=0,
    randomize_seed=True,
    width=width,
    height=height,
    guidance_scale=3.5,
    num_inference_steps=28,
    api_name="/infer"
)

# === Step 4: 建立日期資料夾與檔名 ===
today = datetime.now().strftime("%Y_%m_%d")
folder_path = os.path.join("images", today)
os.makedirs(folder_path, exist_ok=True)

existing_files = [f for f in os.listdir(folder_path) if f.endswith(".png")]
image_index = len(existing_files) + 1
filename = f"{today}_{image_index:02}.png"
output_path = os.path.join(folder_path, filename)

# === Step 5: 將 .webp 轉存為 .png ===
webp_path = result[0]["path"]

with Image.open(webp_path) as img:
    img.convert("RGB").save(output_path, "PNG")

print(f"✅ 圖片已儲存：{output_path}")

# === Step 6: 更新 data.json ===
json_path = os.path.join(folder_path, "data.json")
timestamp = datetime.utcnow().isoformat() + "Z"

new_entry = {
    "filename": filename,
    "prompt": image_prompt,
    "width": width,
    "height": height,
    "style": size_choice["name"],
    "timestamp": timestamp
}

if os.path.exists(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
else:
    data = {"date": today, "images": []}

data["images"].append(new_entry)

with open(json_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"📄 data.json 已更新：{json_path}")

# === Step 7: 更新 README.md 每行最多顯示 10 張圖片 ===
readme_path = os.path.join(folder_path, "README.md")
image_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".png")])

readme_lines = ["# Generated Images", ""]
row = []

for i, image_file in enumerate(image_files, 1):
    row.append(f'<img src="{image_file}" width="100"/>')
    if i % 10 == 0:
        readme_lines.append(" ".join(row))
        row = []

if row:
    readme_lines.append(" ".join(row))

with open(readme_path, "w") as f:
    f.write("\n\n".join(readme_lines))

print(f"📄 README.md 已更新：{readme_path}")
