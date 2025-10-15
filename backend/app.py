# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from sklearn.metrics.pairwise import cosine_similarity
from io import BytesIO
from PIL import Image
import requests
import json
import os

# =========================================
# 1️⃣ Initialize app
# =========================================
app = Flask(__name__)
# Allow requests specifically from your Netlify frontend
CORS(app, origins="https://visual-product-matcher3.netlify.app")

@app.route('/')
def home():
    return "Visual Product Matcher is running!"

# =========================================
# 2️⃣ Load model and embeddings
# =========================================
print("🔄 Loading model and data...")
model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')
embeddings = np.load("embeddings.npy")

with open("valid_products.json", "r") as f:
    products = json.load(f)

print(f"✅ Loaded {len(products)} products and embeddings: {embeddings.shape}")

# =========================================
# 3️⃣ Helper: extract features from uploaded image
# =========================================
def extract_features_from_pil(pil_img):
    pil_img = pil_img.resize((224, 224))
    x = image.img_to_array(pil_img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x, verbose=0)
    return features[0]

# =========================================
# 4️⃣ Helper: find top-k similar products
# =========================================
def find_similar_products(query_features, top_k=5):
    sims = cosine_similarity([query_features], embeddings)[0]
    idx = sims.argsort()[::-1][:top_k]
    results = []
    for i in idx:
        p = products[i]
        results.append({
            "id": p["id"],
            "name": p["name"],
            "category": p["category"],
            "image": p["image"],
            "similarity": round(float(sims[i]), 3)
        })
    return results

# =========================================
# 5️⃣ API route — POST /api/search
# =========================================
@app.route('/api/search', methods=['POST'])
def search():
    try:
        if 'file' in request.files:
            file = request.files['file']
            img = Image.open(file.stream).convert('RGB')
        
        elif request.json and 'image_url' in request.json:
            url = request.json['image_url']
            response = requests.get(url)
            img = Image.open(BytesIO(response.content)).convert('RGB')
        
        else:
            return jsonify({"error": "No image provided"}), 400

        q_feat = extract_features_from_pil(img)
        results = find_similar_products(q_feat, top_k=5)

        return jsonify({"results": results})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =========================================
# 6️⃣ Run app (Render-compatible)
# =========================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)