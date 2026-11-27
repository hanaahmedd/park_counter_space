import os
import tempfile
import cv2
import numpy as np
import streamlit as st
from ultralytics import YOLO

# ==============================
# MODEL CONFIGURATION
# ==============================
MODEL_PATH = r"parking_counter.pt"

# ==============================
# PAGE CONFIGURATION
# ==============================
st.set_page_config(
    page_title="ParkVision | Smart Parking",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==============================
# CUSTOM CSS  (STYLE ONLY)
# ==============================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;600;700&family=Inter:wght@400;500;600;700;800&family=Orbitron:wght@600;800;900&display=swap');

:root {
    --asphalt: #0b0f14;
    --asphalt-2: #121821;
    --line-yellow: #facc15;
    --free: #22c55e;
    --free-glow: rgba(34, 197, 94, 0.35);
    --occ: #ef4444;
    --occ-glow: rgba(239, 68, 68, 0.35);
    --total: #38bdf8;
    --total-glow: rgba(56, 189, 248, 0.35);
    --text: #e5e7eb;
}

/* ---------- App background: asphalt + faint parking bay lines ---------- */
.stApp {
    background:
        repeating-linear-gradient(
            90deg,
            transparent 0px,
            transparent 118px,
            rgba(250, 204, 21, 0.045) 118px,
            rgba(250, 204, 21, 0.045) 120px
        ),
        radial-gradient(circle at 15% 0%, rgba(56, 189, 248, 0.12) 0%, transparent 35%),
        radial-gradient(circle at 90% 5%, rgba(34, 197, 94, 0.10) 0%, transparent 30%),
        linear-gradient(180deg, #0b0f14 0%, #0e131b 100%);
    font-family: 'Inter', sans-serif;
    color: var(--text);
}

/* Hide sidebar */
[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* ---------- Hero: parking entrance sign ---------- */
.hero-card {
    position: relative;
    display: flex;
    align-items: center;
    gap: 28px;
    background:
        linear-gradient(135deg, #0f1722 0%, #131c2b 60%, #0f1a1a 100%);
    border: 1px solid rgba(250, 204, 21, 0.25);
    border-radius: 22px;
    padding: 28px 35px;
    margin-bottom: 18px;
    overflow: hidden;
    box-shadow:
        0 15px 45px rgba(0, 0, 0, 0.45),
        inset 0 0 0 1px rgba(255, 255, 255, 0.03);
}

/* hazard stripe along the top, like a barrier gate */
.hero-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 8px;
    background: repeating-linear-gradient(
        -45deg,
        #facc15 0px, #facc15 16px,
        #111827 16px, #111827 32px
    );
}

.p-badge {
    flex-shrink: 0;
    width: 92px;
    height: 92px;
    border-radius: 18px;
    background: linear-gradient(145deg, #2563eb, #1d4ed8);
    border: 4px solid #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: 3.4rem;
    color: #ffffff;
    box-shadow: 0 0 0 4px #1d4ed8, 0 10px 30px rgba(37, 99, 235, 0.45);
    margin-top: 8px;
}

.hero-text { flex: 1; margin-top: 8px; }

.hero-tag {
    display: inline-block;
    background: rgba(34, 197, 94, 0.12);
    color: #4ade80;
    border: 1px solid rgba(34, 197, 94, 0.4);
    border-radius: 30px;
    padding: 5px 14px;
    font-size: 0.72rem;
    font-weight: 700;
    margin-bottom: 10px;
    letter-spacing: 2px;
}

.hero-tag .dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: #22c55e;
    border-radius: 50%;
    margin-right: 8px;
    animation: pulse-green 1.6s infinite;
}

.hero-card h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.4rem;
    font-weight: 900;
    color: #ffffff;
    margin: 0;
    letter-spacing: 2px;
}

.hero-card h1 span { color: var(--line-yellow); }

.hero-card p {
    font-family: 'Rajdhani', sans-serif;
    color: #9ca3af;
    font-size: 1.15rem;
    margin-top: 8px;
    letter-spacing: 1px;
}

.hero-cars {
    font-size: 1.6rem;
    letter-spacing: 6px;
    opacity: 0.9;
    white-space: nowrap;
}

/* ---------- Lane divider (painted road line) ---------- */
.lane-divider {
    height: 4px;
    margin: 6px 0 4px 0;
    border-radius: 4px;
    background: repeating-linear-gradient(
        90deg,
        #facc15 0px, #facc15 40px,
        transparent 40px, transparent 70px
    );
    opacity: 0.55;
}

/* ---------- Section titles: parking-sign style ---------- */
.section-title {
    font-family: 'Rajdhani', sans-serif;
    color: #f9fafb;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin: 28px 0 15px 0;
    padding-left: 14px;
    border-left: 6px solid var(--line-yellow);
}

/* ---------- Upload area: looks like a parking bay ---------- */
[data-testid="stFileUploader"] {
    background:
        linear-gradient(135deg, #111823, #0f151e);
    border: 2px dashed #facc15;
    border-radius: 14px;
    padding: 18px;
    transition: 0.3s ease;
    position: relative;
}

[data-testid="stFileUploader"]:hover {
    border-color: #22c55e;
    box-shadow: 0 0 25px rgba(34, 197, 94, 0.18);
}

[data-testid="stFileUploader"] label {
    color: #f3f4f6 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.5px;
}

[data-testid="stFileUploader"] section {
    background: rgba(255, 255, 255, 0.03);
    border-radius: 10px;
}

[data-testid="stFileUploader"] button {
    border-radius: 8px;
    border: 1px solid #facc15;
    color: #facc15;
    background: transparent;
    font-weight: 600;
}

[data-testid="stFileUploader"] button:hover {
    background: #facc15;
    color: #111827;
    border-color: #facc15;
}

/* ---------- Metrics: color-coded status boards ---------- */
[data-testid="stMetric"] {
    position: relative;
    background: linear-gradient(145deg, #121a25, #0d131b);
    border-radius: 16px;
    padding: 22px 24px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.35);
    transition: 0.3s ease;
    overflow: hidden;
}

[data-testid="stMetric"]::before {
    content: "";
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 6px;
    background: var(--total);
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
}

[data-testid="stMetricLabel"] {
    color: #cbd5e1 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 2px;
}

[data-testid="stMetricLabel"] p {
    font-size: 1.05rem !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 800 !important;
    font-size: 2.8rem !important;
    color: #ffffff !important;
}

/* 1st metric = FREE (green) */
[data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"]::before,
[data-testid="column"]:nth-child(1) [data-testid="stMetric"]::before {
    background: var(--free);
    box-shadow: 0 0 18px var(--free);
}
[data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"]:hover,
[data-testid="column"]:nth-child(1) [data-testid="stMetric"]:hover {
    border-color: var(--free);
    box-shadow: 0 10px 30px var(--free-glow);
}
[data-testid="stColumn"]:nth-child(1) [data-testid="stMetricValue"],
[data-testid="column"]:nth-child(1) [data-testid="stMetricValue"] {
    color: #4ade80 !important;
    text-shadow: 0 0 18px var(--free-glow);
}

/* 2nd metric = OCCUPIED (red) */
[data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"]::before,
[data-testid="column"]:nth-child(2) [data-testid="stMetric"]::before {
    background: var(--occ);
    box-shadow: 0 0 18px var(--occ);
}
[data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"]:hover,
[data-testid="column"]:nth-child(2) [data-testid="stMetric"]:hover {
    border-color: var(--occ);
    box-shadow: 0 10px 30px var(--occ-glow);
}
[data-testid="stColumn"]:nth-child(2) [data-testid="stMetricValue"],
[data-testid="column"]:nth-child(2) [data-testid="stMetricValue"] {
    color: #f87171 !important;
    text-shadow: 0 0 18px var(--occ-glow);
}

/* 3rd metric = TOTAL (blue) */
[data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"]::before,
[data-testid="column"]:nth-child(3) [data-testid="stMetric"]::before {
    background: var(--total);
    box-shadow: 0 0 18px var(--total);
}
[data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"]:hover,
[data-testid="column"]:nth-child(3) [data-testid="stMetric"]:hover {
    border-color: var(--total);
    box-shadow: 0 10px 30px var(--total-glow);
}
[data-testid="stColumn"]:nth-child(3) [data-testid="stMetricValue"],
[data-testid="column"]:nth-child(3) [data-testid="stMetricValue"] {
    color: #7dd3fc !important;
    text-shadow: 0 0 18px var(--total-glow);
}

/* ---------- Feed labels: CCTV style ---------- */
.feed-label {
    display: flex;
    align-items: center;
    gap: 10px;
    background: #0d131b;
    color: #e5e7eb;
    padding: 12px 16px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-left: 5px solid #facc15;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.feed-label .rec {
    display: inline-block;
    width: 10px; height: 10px;
    border-radius: 50%;
    background: #ef4444;
    animation: blink 1.2s infinite;
}

.feed-label.ai { border-left-color: #22c55e; }
.feed-label.ai .rec { background: #22c55e; animation: pulse-green 1.6s infinite; }

/* ---------- Video / image frames: monitor look ---------- */
[data-testid="stImage"] img {
    border-radius: 12px;
    border: 3px solid #1f2937;
    outline: 1px solid rgba(250, 204, 21, 0.35);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.55);
}

[data-testid="stImage"] [data-testid="stImageCaption"],
[data-testid="stCaptionContainer"] {
    color: #6b7280;
    font-family: 'Rajdhani', sans-serif;
    letter-spacing: 1px;
}

/* ---------- Alerts ---------- */
[data-testid="stAlert"] {
    border-radius: 12px;
    border-left: 5px solid #22c55e;
    background: rgba(34, 197, 94, 0.08);
}

/* ---------- Footer ---------- */
.footer {
    text-align: center;
    color: #6b7280;
    font-family: 'Rajdhani', sans-serif;
    letter-spacing: 1.5px;
    font-size: 0.95rem;
    margin-top: 40px;
    padding: 20px;
    border-top: 3px dashed rgba(250, 204, 21, 0.3);
}

/* ---------- Animations ---------- */
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.15; }
}

@keyframes pulse-green {
    0%   { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
    70%  { box-shadow: 0 0 0 9px rgba(34, 197, 94, 0); }
    100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
}

@media (max-width: 900px) {
    .hero-card { flex-direction: column; text-align: center; }
    .hero-cars { display: none; }
}

</style>

<div class="hero-card">
    <div class="p-badge">P</div>
    <div class="hero-text">
        <div class="hero-tag"><span class="dot"></span>AI POWERED PARKING SYSTEM</div>
        <h1>PARK<span>VISION</span></h1>
        <p>
            SMART PARKING SPACE COUNTER &nbsp;•&nbsp; FREE &nbsp;•&nbsp; OCCUPIED &nbsp;•&nbsp; REAL TIME
        </p>
    </div>
    <div class="hero-cars">🚗 🚙 🅿️ 🚕</div>
</div>
<div class="lane-divider"></div>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model(path: str) -> YOLO:
    return YOLO(path)

def process_frame(model: YOLO, frame: np.ndarray):
    original_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = model(
        frame,
        conf=0.25,
        verbose=False,
    )

    annotated = results[0].plot()

    cls_ids = (
        results[0]
        .boxes.cls.cpu()
        .numpy()
        .astype(int)
    )

    free_space = int((cls_ids == 0).sum())
    occupied = int((cls_ids == 1).sum())

    cv2.putText(
        annotated,
        f"Free: {free_space}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    cv2.putText(
        annotated,
        f"Occupied: {occupied}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
    )

    annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
    return original_rgb, annotated_rgb, free_space, occupied

# ==============================
# MEDIA UPLOADERS (VIDEO & IMAGE)
# ==============================
st.markdown(
    '<div class="section-title">🅿️ Upload Parking Lot Video or Image</div>',
    unsafe_allow_html=True
)

up_col1, up_col2 = st.columns(2, gap="large")

with up_col1:
    uploaded_video = st.file_uploader(
        "🎥 Choose a parking video to start detection",
        type=["mp4", "avi", "mov"],
    )

with up_col2:
    uploaded_image = st.file_uploader(
        "📷 Choose a parking image to start detection",
        type=["jpg", "jpeg", "png", "webp", "bmp"],
    )

model_path = MODEL_PATH

# ==============================
# IMAGE PROCESSING
# ==============================
if uploaded_image and model_path:
    model = load_model(model_path)
    file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
    image_frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image_frame is not None:
        st.markdown(
            '<div class="section-title">📊 Parking Lot Status Board</div>',
            unsafe_allow_html=True
        )

        m_col1, m_col2, m_col3 = st.columns(3, gap="medium")
        free_metric = m_col1.empty()
        occupied_metric = m_col2.empty()
        total_metric = m_col3.empty()

        st.markdown(
            '<div class="section-title">📺 Surveillance Monitor</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown(
                '<div class="feed-label"><span class="rec"></span>ORIGINAL CAMERA FEED</div>',
                unsafe_allow_html=True
            )
            stframe_original = st.empty()

        with col2:
            st.markdown(
                '<div class="feed-label ai"><span class="rec"></span>AI SPACE DETECTION</div>',
                unsafe_allow_html=True
            )
            stframe_labeled = st.empty()

        original_rgb, annotated_rgb, free_space, occupied = process_frame(
            model,
            image_frame,
        )

        free_metric.metric(
            "🟢 FREE SPACES",
            free_space
        )

        occupied_metric.metric(
            "🔴 OCCUPIED SPACES",
            occupied
        )

        total_metric.metric(
            "🅿️ TOTAL SPACES",
            free_space + occupied
        )

        stframe_original.image(
            original_rgb,
            channels="RGB",
            caption="Original Image"
        )

        stframe_labeled.image(
            annotated_rgb,
            channels="RGB",
            caption="AI Detection Results"
        )

        st.success("🎉 Parking image processing completed successfully!")
        st.balloons()
    else:
        st.error("❌ Could not decode the uploaded image. Please try another file.")

# ==============================
# VIDEO PROCESSING
# ==============================
if uploaded_video and model_path:
    temp_video = tempfile.NamedTemporaryFile(delete=False)
    temp_video.write(uploaded_video.read())
    temp_video.close()

    model = load_model(model_path)

    cap = cv2.VideoCapture(temp_video.name)

    st.markdown(
        '<div class="section-title">📊 Parking Lot Status Board</div>',
        unsafe_allow_html=True
    )

    # Metrics
    m_col1, m_col2, m_col3 = st.columns(3, gap="medium")
    free_metric = m_col1.empty()
    occupied_metric = m_col2.empty()
    total_metric = m_col3.empty()

    # Video section
    st.markdown(
        '<div class="section-title">📺 Surveillance Monitor</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            '<div class="feed-label"><span class="rec"></span>ORIGINAL CAMERA FEED</div>',
            unsafe_allow_html=True
        )
        stframe_original = st.empty()

    with col2:
        st.markdown(
            '<div class="feed-label ai"><span class="rec"></span>AI SPACE DETECTION</div>',
            unsafe_allow_html=True
        )
        stframe_labeled = st.empty()

    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frame_idx = 0

    try:
        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            frame_idx += 1

            # Process every 2nd frame
            if frame_idx % 2 != 0:
                continue

            original_frame, annotated, free_space, occupied = process_frame(
                model,
                frame,
            )

            # Update metrics
            free_metric.metric(
                "🟢 FREE SPACES",
                int(free_space)
            )

            occupied_metric.metric(
                "🔴 OCCUPIED SPACES",
                int(occupied)
            )

            total_metric.metric(
                "🅿️ TOTAL SPACES",
                int(free_space + occupied)
            )

            # Display videos
            stframe_original.image(
                original_frame,
                channels="RGB",
                caption="Original Video"
            )

            stframe_labeled.image(
                annotated,
                channels="RGB",
                caption="AI Detection Results"
            )

    finally:
        cap.release()
        if os.path.exists(temp_video.name):
            os.remove(temp_video.name)
    st.success("🎉 Parking video processing completed successfully!")
    st.balloons()

# ==============================
# FOOTER
# ==============================
st.markdown(
    '<div class="footer">🅿️ PARKVISION &nbsp;•&nbsp; SMART PARKING SPACE COUNTER &nbsp;•&nbsp; Made By Hana🥰</div>',
    unsafe_allow_html=True
)
