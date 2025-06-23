import streamlit as st
import re
from groq import Groq
from datetime import datetime
import pandas as pd
from textblob import TextBlob
from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator
from faster_whisper import WhisperModel  # Replaced whisper with faster-whisper
from transformers import pipeline

# Initialize Groq client
client = Groq(api_key="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")

# Initialize faster-whisper model (tiny for speed, small for balance)
whisper_model = WhisperModel("tiny", device="cpu", compute_type="int8")

# Initialize sentiment analysis pipeline
sentiment_analyzer = pipeline("sentiment-analysis")

# Simulated database for call recordings and analysis
if "call_database" not in st.session_state:
    st.session_state.call_database = []

# Model class for LLM integration using Groq
class GroqModel:
    def __init__(self):
        self.client = client
    
    def generate_response(self, messages):
        response = self.client.chat.completions.create(
            model="llama3-70b-8192",
            messages=messages
        )
        return response.choices[0].message.content

# Customer Feedback Analyzer class
class FeedbackAgent:
    def __init__(self):
        self.model = GroqModel()
        self.alert_threshold = 3
        self.whisper_model = WhisperModel("tiny", device="cpu")  # Lightweight model
    
    def transcribe_call(self, audio_file):
        """Transcribe audio using faster-whisper"""
        segments, _ = self.whisper_model.transcribe(audio_file)
        return " ".join(segment.text for segment in segments)
    
    def analyze_sentiment(self, text):
        """Analyze sentiment using both TextBlob and Transformers"""
        blob_score = TextBlob(text).sentiment.polarity
        transformer_result = sentiment_analyzer(text[:512])[0]  # Truncate if too long
        return {
            "textblob_score": blob_score,
            "transformer_label": transformer_result["label"],
            "transformer_score": transformer_result["score"]
        }
    
    def extract_key_phrases(self, text):
        prompt = f"""
        Extract 3-5 key phrases from this customer service call:
        {text}
        Return as bullet points.
        """
        return self.model.generate_response([{"role": "user", "content": prompt}])
    
    def analyze_tone(self, text):
        prompt = f"""
        Analyze tone in this conversation:
        {text}
        Format as:
        - Agent Tone: [description]
        - Customer Tone: [description]
        - Tone Match: [alignment]
        """
        return self.model.generate_response([{"role": "user", "content": prompt}])
    
    def detect_intent(self, text):
        prompt = f"""
        Classify customer intent:
        {text}
        Categories: Information, Complaint, Purchase, Support, Billing, Other
        Include 1-sentence explanation.
        """
        return self.model.generate_response([{"role": "user", "content": prompt}])
    
    def generate_recommendations(self, transcript, analysis):
        prompt = f"""
        Based on this analysis:
        - Sentiment: {analysis['sentiment']}
        - Key Phrases: {analysis['key_phrases']}
        - Tone: {analysis['tone']}
        - Intent: {analysis['intent']}
        
        Provide 3 improvement recommendations focusing on:
        1. Communication adjustments
        2. Handling this intent better
        3. Suggested closing line
        """
        return self.model.generate_response([{"role": "user", "content": prompt}])
    
    def process_call(self, audio_file):
        # Transcribe
        transcript = self.transcribe_call(audio_file)
        
        # Analyze
        analysis = {
            "sentiment": self.analyze_sentiment(transcript),
            "key_phrases": self.extract_key_phrases(transcript),
            "tone": self.analyze_tone(transcript),
            "intent": self.detect_intent(transcript)
        }
        
        # Generate recommendations
        analysis["recommendations"] = self.generate_recommendations(transcript, analysis)
        
        # Check escalation
        analysis["escalation"] = (
            analysis["sentiment"]["textblob_score"] < 0 and
            len([c for c in st.session_state.call_database[-self.alert_threshold:] 
                if c["sentiment"]["textblob_score"] < 0]) >= self.alert_threshold - 1
        )
        
        # Store results
        call_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "transcript": transcript,
            **analysis
        }
        st.session_state.call_database.append(call_data)
        return call_data

# Streamlit UI
def main():
    st.set_page_config(page_title="Voice AI Feedback Agent", page_icon="🎧")
    st.title("Customer Call Analyzer")
    st.write("Upload call recordings for automated feedback")

    agent = FeedbackAgent()
    uploaded_file = st.file_uploader("Upload call (MP3/WAV)", type=["wav", "mp3"])

    if uploaded_file:
        with st.spinner("Analyzing..."):
            # Save temp file for faster-whisper
            with open("temp_audio.wav", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            analysis = agent.process_call("temp_audio.wav")

        # Display results
        st.subheader("Analysis Results")
        
        with st.expander("📝 Transcript"):
            st.write(analysis["transcript"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Sentiment", f"{analysis['sentiment']['textblob_score']:.2f}")
            st.write(f"Label: {analysis['sentiment']['transformer_label']}")
            
            st.subheader("🎯 Customer Intent")
            st.write(analysis["intent"])
        
        with col2:
            st.subheader("🎙️ Tone Analysis")
            st.write(analysis["tone"])
            
            st.subheader("🔑 Key Phrases")
            st.write(analysis["key_phrases"])
        
        st.subheader("💡 Recommendations")
        st.write(analysis["recommendations"])
        
        if analysis["escalation"]:
            st.error("🚨 Manager Alert: Multiple negative calls detected!")

    if st.checkbox("View Call History"):
        if st.session_state.call_database:
            df = pd.DataFrame(st.session_state.call_database)
            st.dataframe(df)
        else:
            st.warning("No calls analyzed yet")

if __name__ == "__main__":
    main()
