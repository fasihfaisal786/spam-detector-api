import streamlit as st
import requests

st.set_page_config(page_title="Spam Detector AI", page_icon="🛡️", layout="wide")

# ---------- CUSTOM CSS ----------
st.markdown("""
    <style>
    .main-title {
        font-size: 46px;
        font-weight: 800;
        color: #1a1a2e;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 16px;
        color: #6c757d;
        margin-bottom: 25px;
    }
    .result-spam {
        background-color: #ffe5e5;
        border-left: 6px solid #e63946;
        padding: 20px;
        border-radius: 10px;
        font-size: 20px;
        font-weight: 600;
        color: #e63946;
    }
    .result-ham {
        background-color: #e5f9ee;
        border-left: 6px solid #2a9d8f;
        padding: 20px;
        border-radius: 10px;
        font-size: 20px;
        font-weight: 600;
        color: #2a9d8f;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- SESSION STATE (history store karne ke liye) ----------
if "history" not in st.session_state:
    st.session_state.history = []
if "spam_count" not in st.session_state:
    st.session_state.spam_count = 0
if "ham_count" not in st.session_state:
    st.session_state.ham_count = 0

# ---------- HEADER ----------
st.markdown('<div class="main-title">🛡️ Spam Detector AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Machine Learning powered SMS/Message spam classifier — built with FastAPI, Scikit-learn & Streamlit</div>', unsafe_allow_html=True)

# ---------- STATS ROW ----------
col1, col2, col3 = st.columns(3)
col1.metric("Total Checked", len(st.session_state.history))
col2.metric("🚫 Spam Found", st.session_state.spam_count)
col3.metric("✅ Normal Messages", st.session_state.ham_count)

st.divider()

# ---------- TABS ----------
tab1, tab2 = st.tabs(["🔎 Checker", "ℹ️ About Project"])

with tab1:
    left, right = st.columns([2, 1])

    with left:
        st.subheader("Message Check Karo")
        message = st.text_area("Message likho ya paste karo:", height=140, placeholder="e.g. Congratulations! You won a free prize...")

        check = st.button("🔎 Analyze Message", use_container_width=True, type="primary")

        if check:
            if message.strip() == "":
                st.warning("⚠️ Pehle koi message likho!")
            else:
                with st.spinner("AI analyzing message..."):
                    try:
                        response = requests.post(
    "https://spam-detector-api-production-308d.up.railway.app/predict",
    json={"message": message}
)   
                        result = response.json()
                        prediction = result["prediction"]
                        confidence = result["confidence"]

                        # History mein add karo
                        st.session_state.history.insert(0, {
                            "message": message,
                            "prediction": prediction,
                            "confidence": confidence
                        })
                        if prediction == "spam":
                            st.session_state.spam_count += 1
                        else:
                            st.session_state.ham_count += 1

                    except Exception as e:
                        st.error(f"Backend se connect nahi ho paya. Kya FastAPI server chal raha hai? Error: {e}")
                        st.stop()

                st.markdown("### Result:")
                if prediction == "spam":
                    st.markdown(f'<div class="result-spam">🚫 SPAM Detected — {confidence}% confidence</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="result-ham">✅ Normal Message (Ham) — {confidence}% confidence</div>', unsafe_allow_html=True)

                st.progress(int(confidence))

    with right:
        st.subheader("💡 Try These")
        examples = [
            "Congratulations! You won a free iPhone, click now!",
            "Hey, what time works for you tomorrow?",
            "URGENT: Verify your account within 24 hours",
            "I'll pick up groceries on my way home"
        ]
        for ex in examples:
            if st.button(ex, use_container_width=True):
                st.session_state.example_selected = ex

    # ---------- HISTORY ----------
    if st.session_state.history:
        st.divider()
        st.subheader("📜 Recent Checks")
        for item in st.session_state.history[:5]:
            icon = "🚫" if item["prediction"] == "spam" else "✅"
            st.write(f"{icon} **{item['prediction'].upper()}** ({item['confidence']}%) — _{item['message'][:60]}..._")

with tab2:
    st.subheader("About This Project")
    st.write("""
    Yeh ek **Machine Learning powered Spam Detector** hai jo SMS/text messages ko 
    automatically classify karta hai — Spam ya Normal (Ham).
    """)
    st.write("**Tech Stack:**")
    st.write("- 🧠 Model: Logistic Regression")
    st.write("- 📊 Feature Extraction: TF-IDF Vectorization")
    st.write("- ⚡ Backend: FastAPI")
    st.write("- 🎨 Frontend: Streamlit")
    st.write("- 📈 Accuracy: ~96%")
    st.caption("Built by Fasih | AI Engineer in Progress")