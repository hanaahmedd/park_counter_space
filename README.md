<div align="center">

# 🅿️ ParkVision

### AI-Powered Smart Parking Space Counter

**Detect. Monitor. Count. Free vs. occupied parking spaces, in real time.**

</div>

---

## 🎬 Demo

https://github.com/user-attachments/assets/113aa250-6f1b-476b-8b96-5abbdfa2df28

---

## 📖 About

**ParkVision** is a computer-vision dashboard that counts how many parking spaces are **free** and how many are **occupied**, from an uploaded parking-lot **image** or **video**.

A custom-trained **YOLO** model detects each parking space and classifies its status. The results are shown in a modern **Streamlit** dashboard with live counters and a side-by-side view of the original footage and the AI detections.

## ✨ Features

- 🟢 **Free space counter**: counts empty parking spots.
- 🔴 **Occupied space counter**: counts spots taken by vehicles.
- 🅿️ **Total spaces**: free + occupied in the current frame.
- 🎥 **Video support**: `mp4`, `avi`, `mov`, processed frame by frame with live-updating metrics.
- 📷 **Image support**: `jpg`, `jpeg`, `png`, `webp`, `bmp`.
- 🖥️ **Side-by-side monitor**: original camera feed next to the AI detection feed.
- 🎨 **Parking-themed UI**: asphalt background, color-coded status boards, CCTV-style labels.
- ⚡ **Optimized**: the model is cached with `st.cache_resource` and every 2nd video frame is processed for smoother playback.

## 🧠 How It Works

1. The user uploads a parking image or video.
2. The YOLO model runs on each frame.
3. Detections are split by class:

   | Class ID | Meaning |
   |:--------:|---------|
   | `0` | 🟢 Free space |
   | `1` | 🔴 Occupied space |

4. Counts are drawn on the frame and displayed in the dashboard metrics.

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) | Object detection model |
| [Streamlit](https://streamlit.io/) | Web dashboard |
| [OpenCV](https://opencv.org/) | Image / video processing |
| [NumPy](https://numpy.org/) | Array operations |

## 📁 Project Structure

```
ParkVision/
├── parkvision_app.py        # Streamlit application
├── parking_counter.pt       # Trained YOLO model weights
├── requirements.txt         # Python dependencies
├── assets/                  # Screenshots / demo 
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/hanaahmedd/park_counter_space.git
cd YOUR_REPO
```

### 2. (Recommended) Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

`requirements.txt`:

```txt
streamlit
ultralytics
opencv-python
numpy
```

### 4. Set the model path

Open `app.py` and edit `MODEL_PATH` so it points to your weights file:

```python
# Original (absolute Windows path)
MODEL_PATH = r"YOUR PATH/parking_counter.pt"

# Recommended when the .pt file sits next to the script
MODEL_PATH = "parking_counter.pt"
```

### 5. Run the app

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal (usually `http://localhost:8501`).

## 🖱️ Usage

1. Launch the app.
2. Upload a **parking video** (left) or a **parking image** (right).
3. Watch the **Parking Lot Status Board** update with free, occupied and total spaces.
4. Compare the **Original Camera Feed** with the **AI Space Detection** feed.

## 📸 Screenshots

#Dashboard of Demo

<img width="1531" height="625" alt="dashboard of demo" src="https://github.com/user-attachments/assets/7e0ff38c-5e7b-4654-b237-04944d3aade7" />

#Test Image

<img width="1337" height="725" alt="demo_image" src="https://github.com/user-attachments/assets/ec1ec03b-6e5d-4ffb-a730-706eb607f36c" />


## 👤 Author

**Your Name**
- GitHub: [@hanaahmedd](https://github.com/hanaahmedd)
- LinkedIn: [Hana Ahmed](https://www.linkedin.com/in/hana-ahmed1/)

---

<div align="center">

⭐ If you like this project, give it a star!

</div>
