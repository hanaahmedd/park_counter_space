
import os
import tempfile

import cv2
import streamlit as st
from ultralytics import YOLO


# ==============================
# MODEL CONFIGURATION
# ==============================

MODEL_PATH = r"C:\HANA\NTI\OLD_parking counter\parking_counter.pt"


# ==============================
# PAGE CONFIGURATION
# ==============================

st.set_page_config(
    page_title="ParkVision | Smart Parking",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==============================
# CUSTOM CSS
# ==============================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(circle at 10% 0%, #172554 0%, transparent 35%),
        radial-gradient(circle at 90% 10%, #312e81 0%, transparent 30%),
        #080d19;
    font-family: 'Inter', sans-serif;
    color: #f8fafc;
}

/* Hide sidebar */

[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none;
}

/* Main spacing */

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Header */

.hero-card {
    background: linear-gradient(
        115deg,
        #172554,
        #312e81 55%,
        #6d28d9
    );
    border: 1px solid rgba(129, 140, 248, 0.35);
    border-radius: 22px;
    padding: 30px 35px;
    margin-bottom: 25px;
    box-shadow: 0 15px 45px rgba(37, 99, 235, 0.15);
}

.hero-card h1 {
    font-size: 2.3rem;
    font-weight: 800;
    color: white;
    margin: 0;
    letter-spacing: -1px;
}

.hero-card p {
    color: #c7d2fe;
    font-size: 1rem;
    margin-top: 8px;
}

.hero-tag {
    display: inline-block;
    background: rgba(34, 211, 238, 0.12);
    color: #67e8f9;
    border: 1px solid rgba(34, 211, 238, 0.3);
    border-radius: 30px;
    padding: 6px 13px;
    font-size: 0.75rem;
    font-weight: 700;
    margin-bottom: 12px;
    letter-spacing: 1px;
}

/* Section titles */

.section-title {
    color: #f1f5f9;
    font-size: 1.25rem;
    font-weight: 800;
    margin: 25px 0 15px 0;
}

/* Upload area */

[data-testid="stFileUploader"] {
    background: linear-gradient(135deg, #111c35, #171b36);
    border: 1px dashed #6366f1;
    border-radius: 18px;
    padding: 18px;
    transition: 0.3s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: #22d3ee;
    box-shadow: 0 0 20px rgba(34, 211, 238, 0.12);
}

[data-testid="stFileUploader"] label {
    color: #e0e7ff !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
}

/* Metrics */

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #172554, #111827);
    border: 1px solid rgba(129, 140, 248, 0.25);
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    transition: 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: #6366f1;
    box-shadow: 0 10px 30px rgba(99, 102, 241, 0.15);
}

[data-testid="stMetricLabel"] {
    color: #c7d2fe !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 800 !important;
}

/* Video labels */

.feed-label {
    background: #151f38;
    color: #a5f3fc;
    padding: 12px 16px;
    border-radius: 12px;
    border-left: 4px solid #22d3ee;
    font-weight: 700;
    margin-bottom: 12px;
}

/* Video images */

[data-testid="stImage"] img {
    border-radius: 16px;
    border: 1px solid rgba(129, 140, 248, 0.35);
    box-shadow: 0 12px 30px rgba(0,0,0,0.3);
}

/* Success message */

[data-testid="stAlert"] {
    border-radius: 14px;
}

/* Footer */

.footer {
    text-align: center;
    color: #64748b;
    font-size: 0.8rem;
    margin-top: 40px;
    padding: 20px;
    border-top: 1px solid #1e293b;
}

</style>

<div class="hero-card">
    <div class="hero-tag">✦ AI POWERED PARKING SYSTEM</div>
    <h1>🚘 ParkVision</h1>
    <p>
        Smart Parking Intelligence Dashboard
        <br>
        Detect. Monitor. Count. All in real time.
    </p>
</div>
""", unsafe_allow_html=True)


# ==============================
# VIDEO UPLOADER
# ==============================

st.markdown(
    '<div class="section-title">🎬 Upload Your Parking Video</div>',
    unsafe_allow_html=True
)

uploaded_video = st.file_uploader(
    "Choose a parking video to start detection",
    type=["mp4", "avi", "mov"],
)

model_path = MODEL_PATH


# ==============================
# VIDEO PROCESSING
# ==============================

if uploaded_video and model_path:

    temp_video = tempfile.NamedTemporaryFile(delete=False)
    temp_video.write(uploaded_video.read())
    temp_video.close()

    model = YOLO(model_path)

    cap = cv2.VideoCapture(temp_video.name)

    st.markdown(
        '<div class="section-title">📊 Parking Analytics</div>',
        unsafe_allow_html=True
    )

    # Metrics

    m_col1, m_col2, m_col3 = st.columns(3, gap="medium")

    free_metric = m_col1.empty()
    occupied_metric = m_col2.empty()
    total_metric = m_col3.empty()

    # Video section

    st.markdown(
        '<div class="section-title">📺 Live Detection Monitor</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            '<div class="feed-label">🎞️ ORIGINAL CAMERA FEED</div>',
            unsafe_allow_html=True
        )
        stframe_original = st.empty()

    with col2:
        st.markdown(
            '<div class="feed-label">🎯 AI DETECTION FEED</div>',
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

            # Original frame

            original_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            # YOLO detection

            results = model(
                frame,
                conf=0.25,
                verbose=False
            )

            annotated = results[0].plot()

            annotated = cv2.cvtColor(
                annotated,
                cv2.COLOR_BGR2RGB
            )

            # Count classes

            cls_ids = (
                results[0]
                .boxes.cls.cpu()
                .numpy()
                .astype(int)
            )

            free_space = (cls_ids == 0).sum()
            occupied = (cls_ids == 1).sum()

            # Overlay counts

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
                "📊 TOTAL DETECTED",
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