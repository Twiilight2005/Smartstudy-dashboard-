import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from groq import Groq
from langdetect import detect
from deep_translator import GoogleTranslator

# -------------------------

# PAGE CONFIG

# -------------------------

st.set_page_config(
page_title="SmartStudy AI",
page_icon="📚",
layout="wide"
)

# -------------------------

# LOAD GROQ API

# -------------------------

api_key = st.secrets["GROQ_API_KEY"]

client = Groq(
api_key=api_key
)

# -------------------------

# TRANSLATION FUNCTION

# -------------------------

def translate_text(text, lang):

```
if lang == "English":
    return text

lang_map = {
    "Tamil": "ta",
    "Hindi": "hi"
}

target = lang_map.get(lang)

return GoogleTranslator(source="auto", target=target).translate(text)
```

# -------------------------

# LANGUAGE DETECTION

# -------------------------

def detect_language(text):
try:
return detect(text)
except:
return "en"

# -------------------------

# LANGUAGE SELECTOR

# -------------------------

LANG = st.sidebar.selectbox(
"🌐 Select Language",
["English","Tamil","Hindi"]
)

# -------------------------

# AI FUNCTION

# -------------------------

def ask_ai(prompt):

```
chat = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {"role":"system","content":"You are an AI tutor helping students study."},
        {"role":"user","content":prompt}
    ]
)

reply = chat.choices[0].message.content

translated = translate_text(reply, LANG)

return translated
```

# -------------------------

# MOCK DATA

# -------------------------

STUDENT = {
"name":"Arjun",
"score":74,
"streak":14
}

SUBJECTS = {
"Mathematics":54,
"Physics":71,
"Programming":88,
"Chemistry":43,
"English":76
}

WEAK_TOPICS = [
{"topic":"Organic Reactions","subject":"Chemistry","score":28},
{"topic":"Differential Calculus","subject":"Mathematics","score":41},
{"topic":"Matrix Algebra","subject":"Mathematics","score":48}
]

# -------------------------

# SIDEBAR

# -------------------------

st.sidebar.title("SmartStudy AI")

page = st.sidebar.radio(
"Navigation",
[
"📊 Overview",
"⚠ Weak Topics",
"✅ Study Tasks",
"📈 Progress",
"🤖 AI Coach"
]
)

# -------------------------

# HEADER

# -------------------------

st.title("📚 SmartStudy AI Dashboard")
st.write(f"Welcome {STUDENT['name']}")

# -------------------------

# OVERVIEW

# -------------------------

if page == "📊 Overview":

```
col1,col2,col3 = st.columns(3)

col1.metric("AI Score",STUDENT["score"])
col2.metric("Study Streak",STUDENT["streak"])
col3.metric("Subjects",len(SUBJECTS))

st.subheader("Subject Mastery")

fig = go.Figure()

fig.add_bar(
    x=list(SUBJECTS.keys()),
    y=list(SUBJECTS.values())
)

st.plotly_chart(fig,use_container_width=True)
```

# -------------------------

# WEAK TOPICS

# -------------------------

elif page == "⚠ Weak Topics":

```
st.subheader("Weak Topics")

for topic in WEAK_TOPICS:

    st.write(
        f"{topic['topic']} | {topic['subject']} | {topic['score']}%"
    )
```

# -------------------------

# TASKS

# -------------------------

elif page == "✅ Study Tasks":

```
st.subheader("Today's Study Plan")

tasks = [
    "Study Organic Reactions",
    "Practice Calculus",
    "Revise Newton Laws"
]

for t in tasks:
    st.checkbox(t)
```

# -------------------------

# PROGRESS

# -------------------------

elif page == "📈 Progress":

```
st.subheader("Weekly Progress")

df = pd.DataFrame({
    "Week":["W1","W2","W3","W4"],
    "Score":[66,69,71,74]
})

fig = go.Figure()

fig.add_scatter(
    x=df["Week"],
    y=df["Score"],
    mode="lines+markers"
)

st.plotly_chart(fig,use_container_width=True)
```

# -------------------------

# AI COACH

# -------------------------

elif page == "🤖 AI Coach":

```
st.subheader("AI Study Coach")

user_input = st.text_input("Ask anything about studying")

if user_input:

    with st.spinner("AI thinking..."):

        response = ask_ai(user_input)

    st.write("AI:",response)
```
