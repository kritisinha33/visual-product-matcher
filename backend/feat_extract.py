# backend/feat_extract.py

import os
import json
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tqdm import tqdm

# ===============================
# 1️⃣ Load model
# ===============================
model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')

# ===============================
# 2️⃣ Helper: extract features from image
# ===============================
def extract_features(img_path):
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = model.predict(x, verbose=0)
        return features[0]
    except Exception as e:
        print(f"❌ Error processing {img_path}: {e}")
        return None

# ===============================
# 3️⃣ Load products list
# ===============================
with open("products.json", "r") as f:
    products = json.load(f)

# ===============================
# 4️⃣ Extract and save features
# ===============================
features = []
valid_products = []

for product in tqdm(products, desc="Extracting features"):
    img_path = product["image"]
    if not os.path.exists(img_path):
        print(f"⚠️ Skipping missing image: {img_path}")
        continue

    feat = extract_features(img_path)
    if feat is not None:
        features.append(feat)
        valid_products.append(product)

features = np.array(features)
print("✅ Feature extraction complete! Shape:", features.shape)

# ===============================
# 5️⃣ Save to disk
# ===============================
np.save("embeddings.npy", features)

with open("valid_products.json", "w") as f:
    json.dump(valid_products, f, indent=2)

print("✅ Saved embeddings.npy and valid_products.json successfully!")
