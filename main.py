# call_analyzer_LASTTRY.py
# (if this breaks just use v2)

import streamlit as st
import os
from datetime import datetime
import pandas as pd

# --- Config stuff that never works right ---
WHISPER_MODEL = "tiny"  # small was too slow
GROQ_MODEL = "llama3-70b-8192"  # overkill probably
ALERT_AFTER = 3  # bad calls before complaining

# --- Global junk ---
all_calls = []  # yeah yeah globals are bad whatever

# ---- Transcription ----
def audio_to_text(audio_path):
    """Turns audio into text. Works... mostly?"""
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel(WHISPER_MODEL, device="cpu")
        segments, _ = model.transcribe(audio_path)
        return " ".join(seg.text for seg in segments)
    except Exception as e:
        return f"Failed: {str(e)}"

# ---- Mood Detection ----
def check_mood(text):
    """Sees if customer is happy/mad"""
    # Simple way first
    try:
        from textblob import TextBlob
        mood1 = TextBlob(text).sentiment.polarity
    except:
        mood1 = 0
        st.warning("TextBlob not working right")

    # Fancy way if possible
    mood2 = "N/A"
    try:
        from transformers import pipeline
        mood2 = pipeline("sentiment-analysis")(text[:1000])[0]
    except:
        pass

    return {
        "score": mood1,
        "ai_says": mood2 if isinstance(mood2, str) else mood2["label"],
        "confidence": 0 if isinstance(mood2, str) else mood2["score"]
    }

# ---- Groq Stuff ----
def ask_ai(question, context):
    """Asks the fancy AI thing"""
    try:
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_KEY"))
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{
                "role": "user",
                "content": f"{question}\n\n{context[:3000]}"
            }]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI failed: {str(e)}"

# ---- Main App ----
def main():
    st.title("Call Analyzer 🤷")
    st.write("Upload a call recording and hope for the best")

    uploaded = st.file_uploader("Pick file", type=['mp3','wav'])

    if uploaded:
        # Save because whisper hates streams
        temp_path = f"temp_{uploaded.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded.getbuffer())

        with st.spinner("Working... (this takes forever)"):
            # 1. Get text
            transcript = audio_to_text(temp_path)
            if "Failed" in transcript:
                st.error(transcript)
                return

            # 2. Check mood
            mood = check_mood(transcript)

            # 3. Ask AI stuff
            questions = [
                "What was this call about? (1 sentence)",
                "List 2 things the agent did well",
                "What could the agent improve?",
                "Suggest a better closing line"
            ]
            answers = [ask_ai(q, transcript) for q in questions]

            # 4. Check if we should panic
            recent_bad = [c for c in all_calls[-ALERT_AFTER:] 
                         if c["mood"]["score"] < 0]
            alert = mood["score"] < 0 and len(recent_bad) >= ALERT_AFTER-1

            # Save results
            call_data = {
                "when": datetime.now().strftime("%m/%d %H:%M"),
                "text": transcript,
                "mood": mood,
                "purpose": answers[0],
                "positives": answers[1],
                "improvements": answers[2],
                "closing": answers[3],
                "alert": alert
            }
            all_calls.append(call_data)

        # Show results
        st.subheader("Results")

        with st.expander("📝 Transcript"):
            st.text(transcript)

        col1, col2 = st.columns([1,2])

        with col1:
            st.metric("Mood", f"{mood['score']:.2f}")
            st.caption(f"AI says: {mood['ai_says']}")

            st.subheader("Purpose")
            st.write(call_data["purpose"])

        with col2:
            st.subheader("Good Stuff")
            st.write(call_data["positives"])

            st.subheader("Could Improve")
            st.write(call_data["improvements"])

        st.subheader("Better Closing")
        st.write(call_data["closing"])

        if alert:
            st.error("MANAGER ALERT! Too many angry calls!")

        # Cleanup
        try:
            os.remove(temp_path)
        except:
            st.warning("Couldn't delete temp file")

    # History view
    if st.checkbox("Show past calls"):
        if all_calls:
            df = pd.DataFrame(all_calls)
            st.dataframe(df[["when", "purpose", "mood"]])
        else:
            st.write("No calls yet")

if __name__ == "__main__":
    main()
    # TODO: Add error logging
    # TODO: Make less janky
