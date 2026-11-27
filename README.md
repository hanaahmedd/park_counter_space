<div align="center">

# 🅿️ ParkVision

### AI-Powered Smart Parking Space Counter

**Detect. Monitor. Count. Free vs. occupied parking spaces, in real time.**

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![YOLO](https://img.shields.io/badge/Model-YOLO-00FFFF)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?logo=opencv&logoColor=white)

</div>

---

## 🎬 Demo

> **Replace this section with your own video** (see [How to add a video](#-how-to-add-a-video-to-this-readme) below).

https://github.com/YOUR_USERNAME/YOUR_REPO/assets/REPLACE_WITH_YOUR_VIDEO_ID

<!-- Optional: a GIF preview that plays inline everywhere -->
<!-- ![ParkVision Demo](assets/demo.gif) -->

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
2. The YOLO model runs on each frame (confidence threshold `0.25`).
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
├── assets/                  # Screenshots / demo GIF (optional)
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
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

Open `parkvision_app.py` and edit `MODEL_PATH` so it points to your weights file:

```python
# Original (absolute Windows path)
MODEL_PATH = r"C:\HANA\NTI\OLD_parking counter\parking_counter.pt"

# Recommended when the .pt file sits next to the script
MODEL_PATH = "parking_counter.pt"
```

### 5. Run the app

```bash
streamlit run parkvision_app.py
```

Then open the local URL shown in the terminal (usually `http://localhost:8501`).

## 🖱️ Usage

1. Launch the app.
2. Upload a **parking video** (left) or a **parking image** (right).
3. Watch the **Parking Lot Status Board** update with free, occupied and total spaces.
4. Compare the **Original Camera Feed** with the **AI Space Detection** feed.

## 📸 Screenshots

| Dashboard | Detection Result |
|:---------:|:----------------:|
| ![Dashboard](assets/dashboard.png) | ![Detection](assets/detection.png) |

> Add your own screenshots to the `assets/` folder and update the file names above.

## 🎥 How to Add a Video to This README

GitHub READMEs can play videos, but **a relative path like `assets/demo.mp4` will not play inline**. Use one of these options:

**Option 1: Upload directly to GitHub (best)**
1. Open your repo on GitHub and click the ✏️ pencil icon to edit `README.md`.
2. **Drag and drop** your `.mp4` or `.mov` file (max 100 MB on a free account) into the editor.
3. GitHub inserts a link like `https://github.com/user/repo/assets/12345/abcd-...`.
4. Keep that link on its own line. It renders as a playable video. Commit the change.

**Option 2: Use a GIF (works everywhere)**
1. Convert your demo to a short GIF (for example with ScreenToGif, or `ffmpeg`).
2. Save it as `assets/demo.gif` and use:
   ```markdown
   ![ParkVision Demo](assets/demo.gif)
   ```

**Option 3: YouTube link with a thumbnail**
```markdown
[![Watch the demo](assets/thumbnail.png)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)
```

## ⚠️ Notes

- Model weight files can be large. GitHub blocks files over **100 MB**, so use [Git LFS](https://git-lfs.com/) or attach the `.pt` file to a **GitHub Release** if needed.
- A GPU is not required, but it makes video processing noticeably faster.
- Detection quality depends on camera angle, lighting, and how similar the footage is to the training data.

## 🔮 Future Improvements

- Live webcam / RTSP stream support
- Occupancy percentage and history charts
- Export of results to CSV
- Multi-lot dashboard

## 🤝 Contributing

Contributions, issues and feature requests are welcome. Feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

## 👤 Author

**Your Name**
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [Your Name](https://www.linkedin.com/in/YOUR_PROFILE)

---

<div align="center">

⭐ If you like this project, give it a star!

</div>
