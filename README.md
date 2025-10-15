# Visual Product Matcher

**A Deep Learning-Powered Visual Search Engine for Fashion Products**  

This project is a content-based image retrieval (CBIR) system to find visually similar fashion products. Users upload an image, and the app returns a curated list of similar items from the product database using deep learning.

**Live Demo**  
- Frontend: [https://visual-product-matcher3.netlify.app/](https://visual-product-matcher3.netlify.app/)  
- Backend: [https://visual-product-matcher-yijy.onrender.com/](https://visual-product-matcher-yijy.onrender.com/)

---

## Key Functionality
- **Image-based Searching:** Upload images to discover products.  
- **Real-time Similarity Scoring:** Uses cosine similarity between query and catalog images.  
- **Dynamic Results Display:** Responsive grid with product name and category.  
- **Responsive UI:** Works on desktop and mobile devices.  

---

## Technology Stack

| Category           | Technology                                     |
|-------------------|-----------------------------------------------|
| Backend           | Flask, Gunicorn                               |
| Machine Learning  | TensorFlow (Keras), Scikit-learn, NumPy, Pillow |
| Frontend          | HTML5, CSS3, Vanilla JavaScript (Fetch API)  |
| Core Model        | MobileNetV2 (pre-trained on ImageNet)        |
| Deployment        | Render (API), Netlify (Client)               |

---

## System Architecture and Methodology

The system uses **content-based image retrieval** with two phases:

- **Offline Indexing:**  
  MobileNetV2 extracts 1280-dimensional embeddings from product images. Saved as `embeddings.npy` for fast lookup.

- **Online Retrieval:**  
  User-uploaded images are converted into embeddings. Cosine similarity finds top-K visually similar products.  

The pipeline runs inside a **Flask API**, returning JSON responses for search requests.

---

## Local Development Setup

```bash
# Clone the Repository
git clone https://github.com/kritisinha33/visual-product-matcher.git
cd visual-product-matcher

# Setup Backend Environment
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt

# Generate Product Image Embeddings
# Creates embeddings.npy & valid_products.json for searching
python feat_extract.py

# Start Backend Server
# Flask API available at http://127.0.0.1:5000
python app.py

# Start Frontend Application
cd ../frontend
# Open the app in browser at http://127.0.0.1:8000
python -m http.server 8000

# Screenshot of working Application
<img width="1920" height="939" alt="image" src="https://github.com/user-attachments/assets/86df4315-748a-4710-aded-92487ab0580f" />
<img width="1885" height="930" alt="image" src="https://github.com/user-attachments/assets/21a15e76-6c5e-4c70-9a04-583d149ae4f8" />


