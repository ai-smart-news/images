import os
import random
import json
from datetime import datetime
from g4f.client import Client as Client_g4f
from gradio_client import Client as Client_gradio
from PIL import Image


subjects = [
    "ancient robotess", "cosmic whale queen", "masked enchantress", "crystal giantess", "mechanical songbird",
    "floating empress castle", "orbital matron", "hooded wanderess", "fire spirit maiden", "mirror siren",
    "lone samurai girl", "cybernetic nun", "glass dragoness", "forest guardianess", "energy blade dancer",
    "skyborne city queen", "golem priestess", "sunken relic maiden", "arcane knightess", "drifting starship pilot",
    "tree nymph", "neon dancer girl", "cathedral ship mistress", "blood sorceress", "space jellyfish queen",
    "clockwork seraph", "mutant doe", "shadow assassiness", "lava serpentess", "cloud leviathan",
    "frozen sentinel maiden", "desert banshee queen", "ghost aviatrix", "core priestess", "female time traveler",
    "dream diveress", "obsidian she-beast", "wind oracle maiden", "gravity witch", "cursed doll",
    "twilight huntress", "moon priestess", "data muse", "plasma valkyrie", "memory weaver",
    "alien mystic nun", "flame queen", "junkyard colossina", "solar lioness", "marble sphinx queen",
    "crystal seeress", "android seraphina", "storm chaser girl", "orb mistress", "space cowgirl",
    "withered statue maiden", "sky serpentess", "magnetic ghost lady", "veil danceress", "starborn maiden",
    "mirrored ronin girl", "tide witch", "panther automa", "ice prophetess", "temporal crow lady",
    "bone golemess", "dream vulpine", "obsidian hind", "tech valkyrie", "vortex mage girl",
    "circuit priestess", "skyforged lioness", "living relic maiden", "cyber dragon queen", "glass phoenix maiden",
    "acidic slug queen", "neon brute diva", "memory maiden", "lunar she-wolf", "spectral architectress",
    "cloud shepherdess", "signal huntress", "dust alchemista", "flesh automata", "silicon banshee",
    "spore druidess", "nebula crab queen", "hollow echo maiden", "plague oracle lady", "ether she-golem",
    "sonic knightess", "wire lich witch", "snow crow matron", "sun archangel", "machine monkess",
    "gravity sage maiden", "radiant thief girl", "moss giantess", "storm sentinel queen", "titanic jelly siren"
]


styles = [
    "fantasy", "cyberpunk", "surrealism", "baroque", "low-poly", "oil painting",
    "vaporwave", "realism", "gothic", "neon noir", "dieselpunk", "abstract expressionism",
    "steampunk", "futurism", "impressionism", "grunge", "synthwave", "chiaroscuro",
    "expressionist", "vintage poster", "dark academia", "minimalism", "sci-fi horror",
    "pixel art", "flat design", "brutalism", "watercolor", "ink sketch", "charcoal drawing",
    "concept art", "art nouveau", "pop art", "tribal art", "monochrome", "mythological",
    "cubism", "digital painting", "cinematic realism", "symbolist", "ethereal realism",
    "graffiti", "dark fantasy", "high fantasy", "contemporary surreal", "noir",
    "hyperrealism", "whimsical", "vintage anime", "cel shading", "magic realism",
    "industrial", "spiritual art", "mystic abstraction", "mechanical futurism",
    "biopunk", "afrofuturism", "arcane punk", "romanticism", "post-apocalyptic",
    "science illustration", "dreamcore", "datamosh", "cutout collage", "ornate gothic",
    "tech noir", "new wave", "low-fi", "retro pop", "hard-edge abstraction",
    "kinetic sculpture", "comic book style", "sacred geometry", "eastern ink style",
    "photorealism", "fluid art", "subrealism", "macabre", "organic minimalism",
    "pointillism", "pixel noise", "experimental glitch", "drip painting",
    "liquid chrome", "bizarre surreal", "mythic horror", "generative fractal",
    "sacral surrealism", "dark psychedelia", "deco futurism", "anime realism",
    "voidcore", "ornamental futurism", "retro arcade", "quantum surreal",
    "sacred sci-fi", "twisted baroque", "digital horror", "punk romantic"
]

lighting_moods = [
    "misty dawn", "harsh spotlight", "soft moonlight", "blood-red sunset", "dim cavern glow",
    "neon reflections", "fire-lit shadows", "radiant storm", "eerie twilight", "pulsing strobe",
    "backlit fog", "deep underwater glow", "arcade ambiance", "studio contrast", "luminous eclipse",
    "volcanic haze", "alien atmosphere", "solar flare", "rain-soaked streetlight", "flickering candlelight",
    "cracked crystal light", "overcast gloom", "colorful aurora", "stormy clouds", "burning skyline",
    "golden dusk", "silver dawn", "low-angle lanterns", "cyber shimmer", "moon halo",
    "shadow tunnel", "ray of hope", "drifting dust light", "monochrome tension", "glow from below",
    "lens-distorted light", "hallucinated sun", "radiating ice", "chaotic sparks", "cold steel glint",
    "halo blaze", "ambient void", "spotlight slice", "melting neon", "diffused projector light",
    "reflective surface glow", "laser pulse", "torchlit ruins", "oil-lamp mist", "shimmering void",
    "orbital station light", "sunken ruin haze", "signal glow", "dusk field fireflies", "swamp light",
    "ritual circle fire", "mist lanterns", "inverted sun", "hidden campfire", "colored smog",
    "light spirals", "aurora haze", "cold temple light", "chromatic clouds", "desert mirage shine",
    "ethereal brightness", "crescent glow", "reflected sparks", "moonbeam fracture", "blade glimmer",
    "wireless flicker", "hollow flicker", "bio-electric pulse", "timeless haze", "drone beam",
    "under-sky luminance", "cryptic eclipse", "sacred torchlight", "ancient glow", "floating prism light",
    "crystal cave glow", "engine sparks", "infrared shimmer", "plasma arcs", "dim reactor core",
    "tunnel flickers", "ceremonial embers", "vortex light", "lava field haze", "storm-lit sky",
    "dreamlight", "chaos bloom", "twilight shimmer", "cosmic pulse", "digital starlight"
]

color_palettes = [
    "monochrome blue", "gold and obsidian", "neon pink and teal", "rust and emerald",
    "crimson and fog white", "sepia tones", "electric violet and sky cyan", "pastel gradients",
    "sunset orange and navy", "silver and turquoise", "fire glow and shadow black", "lunar lavender and dusk",
    "jade and brass", "storm gray and royal purple", "mint and ash", "night indigo and bronze",
    "plasma green and carbon", "burnt sienna and glacier", "cherry red and void", "dusty rose and cream",
    "flame and steel", "forest and frost", "arctic ice and shadow", "pearl and graphite",
    "amber and onyx", "cloud and blood", "laser red and smoke", "deep plum and sand",
    "gold and navy", "holographic chrome", "emerald and obsidian", "sky gold and fog",
    "aquamarine and coal", "peach and oxide", "blood orange and ink", "silver fire",
    "dim cyan and brown", "star white and abyss blue", "purple dusk and haze",
    "light coral and void black", "neon rust and cobalt", "seafoam and mercury",
    "flamingo pink and steel blue", "violet haze and gold sparks", "lava and smoke",
    "frost green and granite", "pearl white and scarlet", "cerulean and bone",
    "ghost blue and dusk", "slate and sunrise", "turquoise and shadow brown",
    "storm cloud and moss", "ochre and grey steel", "platinum and maroon",
    "ink blue and signal red", "dream violet and fog green", "bronze and blush",
    "cream gold and pale cyan", "sky rose and ember", "petrol blue and chrome",
    "twilight and coal red", "mist gray and glowing orange", "lavender silver and wine",
    "cosmic cyan and carbon black", "ice pink and moss green", "opal and deep tan",
    "wine red and smoke white", "cactus green and pale gold", "dim violet and brass",
    "sunflower and twilight gray", "lava red and feather white", "electric blue and rust",
    "nude bronze and forest ink", "algae green and cold iron", "sun gold and haze gray",
    "sapphire and sulfur", "dust beige and ocean steel", "chrome blue and velvet red",
    "crimson haze and gold", "pine green and pearl silver", "black opal and rose",
    "mulberry and storm white", "deep jade and volcanic gray", "pewter and petrol green",
    "graphite and glacier blue", "moon silver and crimson bloom", "coral dusk and tech gray",
    "moonstone and pale wine", "digital mint and shadow bronze", "storm plum and electric smoke",
    "rose ivory and blue ash", "candy red and toxic green", "silk ivory and concrete",
    "ghost gray and neon leaf", "obsidian and champagne", "blood gold and cloud silver"
]

perspectives = [
    "low-angle view", "bird's eye view", "first-person view", "over-the-shoulder shot",
    "extreme close-up", "wide-angle scene", "side profile", "silhouette framing", "reflection angle",
    "distant shot", "worm’s eye view", "top-down cutaway", "isometric cut", "overhead abstract",
    "drone-style pan", "frontal symmetrical", "corner peek view", "mirrored environment shot",
    "rotated tilt shot", "fish-eye distortion", "dynamic zoom blur", "panoramic scope",
    "vertical split-frame", "underwater perspective", "edge-cliff framing",
    "dim corridor point-of-view", "light source behind subject", "sky-down vortex",
    "spiral angle", "motion blur capture", "lens compression frame", "sun-behind glare",
    "fog window focus", "flying camera arc", "abstract focus depth", "minimal tilt-frame",
    "side cut-out with depth", "backlight zoom", "twilight tunnel view",
    "from-reflection shot", "vortex eye focus", "heroic center-focus", "ghost-following angle",
    "upward eclipse shot", "shattered glass framing", "angled stairwell frame",
    "folded plane illusion", "rippling perspective", "curved hallway illusion",
    "sky-and-ground dual-view", "multiple mirror echo view", "descent view from above",
    "flat plane head-on", "lightburst focus", "lateral corridor", "top-left diagonal",
    "tunnel vision scope", "low glow from reflection", "dim-light corner peek",
    "symmetrical collapse perspective", "fractured lens perspective", "fog-lit corridor side shot",
    "wall trace focus", "inverted corridor scope", "organic tunnel split-view",
    "mist-obscured view", "angled room projection", "magnetic focus whirl",
    "portal through tree roots", "from-object reflection", "internal subject POV",
    "reverse tracking shot", "drift-through lens", "time-folded view",
    "oblique glass sliver", "rotated flatfield perspective", "trapped bubble lens",
    "reverse eclipse view", "veiled curtain glimpse", "infinite depth corridor",
    "fractured sky angle", "orbital floating perspective", "dust trail follow view",
    "gazing from below", "door-framed character focus", "flooded field angle",
    "back-focus silhouette", "light-through-hand perspective", "pulsing doorway effect",
    "inversion prism view", "iris tunnel framing", "water reflection top shot",
    "glitch-wrapped perspective", "cross-section hall cut"
]

details = [
    "cracked glass texture", "floating debris", "ethereal glow", "arcane symbols hovering",
    "water droplets in motion", "particles of ash", "mechanical joints", "overgrown roots",
    "levitating stones", "fog trails", "lens flare", "digital noise", "folded space-time",
    "glowing circuit veins", "neon tattoos", "vortex particles", "ancient carvings",
    "scrolls blowing in wind", "organic tentacles", "burning petals", "bubbling liquid",
    "torn cloth", "holographic interface", "rust flakes", "mirror fragments",
    "feather fall motion", "embers in air", "magnetic pulses", "starfield overlay",
    "quantum sparks", "cyber wings", "metallic moss", "liquid shimmer",
    "shadow flickers", "floating lanterns", "silicon smoke", "geometric patterns",
    "dripping light", "time fracture cracks", "glitching reflection", "flaming runes",
    "transparent filaments", "organic moss growth", "sound waves visualized",
    "tattered flags", "vines pulsing with energy", "dust vortex", "folding shadow",
    "motion ribbons", "dissolving skin", "electrostatic air", "star charts",
    "hovering stone rings", "infinite mirrors", "snow particles", "molten stone",
    "crystal webs", "nebula ink clouds", "fractured statue", "melting sculpture",
    "floating string lights", "bio-organic veins", "time-locked particles",
    "dripping neon wires", "telepathic symbol bloom", "hover glass shards",
    "folding cloth wave", "tinted aura circles", "blurred reflections", "creaking roots",
    "blinking eyes in fog", "vibrating crystal rings", "mechanical bones",
    "digital tears", "reverse smoke", "floating tattoos", "spore clouds",
    "floating raindrops", "dim holograms", "bleeding circuits", "suspended steam",
    "glowing scar lines", "pulse trails", "color inversion sparks", "mossy rubble",
    "scattered scripts", "ghost limbs", "metal petals", "shifting ink shapes",
    "smoke feather mix", "symbiotic filaments", "glass particle burst",
    "dimmed sun shafts", "hovering glyphs", "sonic distortion rings"
]

def pick_elements(category, n=2):
    return random.sample(category, n)

chosen = {
    "subject": pick_elements(subjects),
    "style": pick_elements(styles),
    "lighting": pick_elements(lighting_moods),
    "color": pick_elements(color_palettes),
    "perspective": pick_elements(perspectives),
    "details": pick_elements(details),
}

prompt_template = f"""
Please generate a single-sentence AI image prompt suitable for high-detail image generation models (like FLUX or Stable Diffusion).

Use the following creative inspiration:

- **Subject(s)**: {', '.join(chosen['subject'])}
- **Art Style(s)**: {', '.join(chosen['style'])}
- **Lighting / Mood**: {', '.join(chosen['lighting'])}
- **Color Palette**: {', '.join(chosen['color'])}
- **Perspective**: {', '.join(chosen['perspective'])}
- **Extra Details**: {', '.join(chosen['details'])}

Do not list the elements explicitly in the sentence. Instead, use these keywords to inform your creative description of a vivid, visually rich and immersive scene. The prompt should read like concept art narration, elegant and imaginative, with no camera tags or formatting.
Please describe more details of picture, image, and styles, realistic portrait, digital artwork, CGI pictures, at list 150 words.
Just return a **single descriptive sentence**.
"""

# === Step 1: 用 g4f GPT-4o 生成高品質繪圖 prompt ===
client = Client_g4f()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": (
                prompt_template
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
webp_path = result[0]

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
