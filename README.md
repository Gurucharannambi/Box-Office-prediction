# 🎬 Telugu Box Office Predictor — Streamlit App

A deep-learning style Telugu box office prediction dashboard with:
- **Hero / Director / Genre / Season / Budget / Screens** inputs
- **Live prediction** with confidence score
- **Training Loss Curve** (Plotly)
- **Confusion Matrix** (Plotly heatmap)
- **97.3% model accuracy** display

---

## 🚀 Run Locally

```bash
# 1. Install dependencies (no TensorFlow needed!)
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

App opens at: **http://localhost:8501**

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push this folder to a **GitHub repo** (public or private)
2. Go to → [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"**
4. Select your repo, branch, and set **Main file path** to `app.py`
5. Click **Deploy** — done in ~60 seconds!

> Streamlit Cloud auto-installs from `requirements.txt`.

---

## 📦 Dependencies

| Package     | Version  | Purpose                     |
|-------------|----------|-----------------------------|
| streamlit   | ≥1.32.0  | Web app framework            |
| plotly      | ≥5.18.0  | Training loss + confusion matrix charts |
| numpy       | ≥1.24.0  | Data generation for charts   |

**No TensorFlow, PyTorch, Keras, or heavy ML libraries required.**  
The prediction engine uses calibrated feature weights (simulating a trained deep learning model).

---

## 📁 File Structure

```
telugu_streamlit/
├── app.py            ← Main Streamlit app
├── requirements.txt  ← Lightweight dependencies
└── README.md         ← This file
```
