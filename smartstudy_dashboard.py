```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from transformers import MarianMTModel, MarianTokenizer
from langdetect import detect

# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="SmartStudy AI",
    page_icon="📚",
    layout="wide"
)

# -------------------------------
# LOAD TRANSLATION MODEL
# -------------------------------

@st.cache_resource
def load_model():

    model_name = "Helsinki-NLP/opus-mt-en-mul"

    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    return tokenizer, model


tokenizer, model = load_model()

# -------------------------------
# TRANSLATION FUNCTION
# -------------------------------

def translate(text, lang):

    if lang == "English":
        return text

    inputs = tokenizer(text, return_tensors="pt", padding=True)

    translated = model.generate(**inputs)

    result = tokenizer.decode(translated[0], skip_special_tokens=True)

    return result


# -------------------------------
# LANGUAGE DETECTION
# -------------------------------

def detect_language(text):

    try:
        return detect(text)
    except:
        return "en"


# -------------------------------
# LANGUAGE SELECTOR
# -------------------------------

LANG = st.sidebar.selectbox(
    "🌐 Select Language",
    ["English", "Tamil", "Hindi"]
)

# -------------------------------
# TRANSLATION DICTIONARY
# -------------------------------

TRANSLATIONS = {

    "English": {
        "overview": "Overview",
        "weak_topics": "Weak Topics",
        "tasks": "Study Tasks",
        "revision": "Revision",
        "progress": "Progress",
        "coach": "AI Coach"
    },

    "Tamil": {
        "overview": "மேலோட்டம்",
        "weak_topics": "பலவீனமான தலைப்புகள்",
        "tasks": "படிப்பு பணிகள்",
        "revision": "மீளாய்வு",
        "progress": "முன்னேற்றம்",
        "coach": "AI பயிற்சியாளர்"
    },

    "Hindi": {
        "overview": "सारांश",
        "weak_topics": "कमज़ोर विषय",
        "tasks": "अध्ययन कार्य",
        "revision": "पुनरावृत्ति",
        "progress": "प्रगति",
        "coach": "AI शिक्षक"
    }

}

def tr(key):
    return TRANSLATIONS.get(LANG, {}).get(key, key)


# -------------------------------
# MOCK DATA
# -------------------------------

STUDENT = {
    "name": "Arjun",
    "score": 74,
    "streak": 14
}

SUBJECTS = {

    "Mathematics": 54,
    "Physics": 71,
    "Programming": 88,
    "Chemistry": 43,
    "English": 76

}

WEAK_TOPICS = [

    {"topic": "Organic Reactions", "subject": "Chemistry", "score": 28},
    {"topic": "Differential Calculus", "subject": "Mathematics", "score": 41},
    {"topic": "Matrix Algebra", "subject": "Mathematics", "score": 48}

]


AI_RESPONSES = {

    "What should I study today?":
    "Focus on Organic Reactions for 45 minutes. Then practice Differential Calculus and take a short Matrix Algebra quiz.",

    "Why is chemistry weak?":
    "Your quiz accuracy in Organic Reactions is only 24 percent. You need more concept revision.",

    "Show my progress":
    "Your overall score increased to 74 percent this week. Programming is your strongest subject."

}

# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.title("SmartStudy AI")

page = st.sidebar.radio(

    "Navigation",

    [
        f"📊 {tr('overview')}",
        f"⚠️ {tr('weak_topics')}",
        f"✅ {tr('tasks')}",
        f"↺ {tr('revision')}",
        f"📈 {tr('progress')}",
        f"🤖 {tr('coach')}"
    ]

)

# -------------------------------
# HEADER
# -------------------------------

st.title("📚 SmartStudy AI Dashboard")

st.write(f"Welcome {STUDENT['name']}")

# -------------------------------
# OVERVIEW PAGE
# -------------------------------

if "Overview" in page or "மேலோட்டம்" in page or "सारांश" in page:

    col1, col2, col3 = st.columns(3)

    col1.metric("AI Score", STUDENT["score"])
    col2.metric("Study Streak", STUDENT["streak"])
    col3.metric("Subjects", len(SUBJECTS))

    st.subheader("Subject Mastery")

    fig = go.Figure()

    fig.add_bar(

        x=list(SUBJECTS.keys()),
        y=list(SUBJECTS.values())

    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# WEAK TOPICS
# -------------------------------

elif "Weak" in page or "பலவீனமான" in page or "कमज़ोर" in page:

    st.subheader("Weak Topics")

    for topic in WEAK_TOPICS:

        st.write(

            topic["topic"],
            "-",
            topic["subject"],
            "-",
            topic["score"],
            "%"

        )

# -------------------------------
# STUDY TASKS
# -------------------------------

elif "Study" in page or "படிப்பு" in page or "अध्ययन" in page:

    st.subheader("Today's Tasks")

    tasks = [

        "Study Organic Reactions",
        "Practice Calculus",
        "Revise Newton Laws"

    ]

    for t in tasks:

        st.checkbox(t)

# -------------------------------
# REVISION
# -------------------------------

elif "Revision" in page or "மீளாய்வு" in page or "पुनरावृत्ति" in page:

    st.subheader("Revision Queue")

    revisions = [

        "Quadratic Equations",
        "Python Functions",
        "Integration"

    ]

    for r in revisions:

        st.write("📌", r)

# -------------------------------
# PROGRESS PAGE
# -------------------------------

elif "Progress" in page or "முன்னேற்றம்" in page or "प्रगति" in page:

    st.subheader("Progress Report")

    progress_data = pd.DataFrame({

        "Week": ["W1", "W2", "W3", "W4"],
        "Score": [66, 69, 71, 74]

    })

    fig = go.Figure()

    fig.add_scatter(

        x=progress_data["Week"],
        y=progress_data["Score"],
        mode="lines+markers"

    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# AI COACH
# -------------------------------

elif "Coach" in page or "பயிற்சியாளர்" in page or "शिक्षक" in page:

    st.subheader("AI Study Coach")

    user_input = st.text_input("Ask the AI coach")

    if user_input:

        reply = AI_RESPONSES.get(

            user_input,

            "Chemistry needs more attention this week."

        )

        translated = translate(reply, LANG)

        st.write("AI:", translated)
```
