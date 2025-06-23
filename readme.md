# 🎧 Voice AI Feedback Agent

An intelligent customer service call analyzer that automatically transcribes, analyzes, and provides actionable feedback on customer service interactions using advanced AI technologies.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [API Configuration](#api-configuration)
- [Sample Output](#sample-output)
- [Technical Details](#technical-details)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The Voice AI Feedback Agent is a comprehensive solution for automated customer service quality assurance. It combines multiple AI technologies to provide real-time analysis of customer calls, including sentiment analysis, intent detection, tone evaluation, and actionable improvement recommendations.

### Problem Solved
- **Manual QA Bottlenecks**: Eliminates time-intensive manual call reviews
- **Inconsistent Feedback**: Provides objective, data-driven evaluations
- **Reactive Problem Solving**: Enables proactive issue identification
- **Training Gaps**: Identifies specific areas for agent improvement
- **Escalation Delays**: Automatically flags concerning patterns

## ✨ Features

### 🎤 Audio Processing
- **Automatic Transcription**: Converts audio files to searchable text using faster-whisper
- **Multi-format Support**: Handles MP3 and WAV audio files
- **Optimized Performance**: Uses lightweight models for real-time processing

### 🧠 AI-Powered Analysis
- **Dual Sentiment Analysis**: Combines TextBlob and Transformers for accurate sentiment scoring
- **Intent Classification**: Automatically categorizes customer requests (Support, Complaint, Purchase, etc.)
- **Tone Analysis**: Evaluates both agent and customer communication styles
- **Key Phrase Extraction**: Identifies important topics and concerns

### 📊 Intelligent Insights
- **Performance Metrics**: Quantifiable scores for call quality assessment
- **Actionable Recommendations**: Specific suggestions for improvement
- **Pattern Recognition**: Identifies trends across multiple interactions
- **Escalation Alerts**: Automatic manager notifications for concerning patterns

### 🚨 Proactive Escalation
- **Smart Threshold Detection**: Monitors negative sentiment patterns
- **Automatic Alerts**: Triggers manager notifications after 3 consecutive negative calls
- **Historical Tracking**: Maintains call history for pattern analysis

## 🏗️ Architecture

```
Audio Input → Transcription → Parallel Analysis → Synthesis → Recommendations → Escalation Check
     ↓              ↓              ↓              ↓              ↓              ↓
   Upload    faster-whisper   Multi-modal NLP   AI Reasoning   Action Items   Manager Alert
```

### Core Components
1. **Audio Processing Pipeline**: faster-whisper for efficient transcription
2. **NLP Analysis Engine**: Multi-modal analysis using various AI models
3. **Reasoning System**: LLM-powered insight generation via Groq API
4. **Dashboard Interface**: Interactive Streamlit web application
5. **Data Management**: Session-based storage with historical tracking

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- 4GB+ RAM recommended
- Groq API key (free tier available)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Kanishk1764/Voice-ai-feedback-agent-Onelogica.git
cd Voice-ai-feedback-agent-Onelogica
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Additional Requirements
If `requirements.txt` is not available, install packages manually:
```bash
pip install streamlit groq faster-whisper textblob transformers pandas langdetect deep-translator
```

### Step 5: Download NLTK Data (Required for TextBlob)
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
```

## ⚙️ API Configuration

### Groq API Setup
1. Visit [Groq Console](https://console.groq.com/) and create a free account
2. Generate an API key
3. Replace the API key in `main.py`:
```python
client = Groq(api_key="your_api_key_here")
```

**⚠️ Security Note**: For production use, store API keys in environment variables:
```python
import os
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
```

## 🖥️ Usage

### Running the Application
```bash
streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`

### Using the Interface
1. **Upload Audio File**: Click "Upload call (MP3/WAV)" and select your audio file
2. **Automatic Processing**: The system will automatically:
   - Transcribe the audio
   - Analyze sentiment, tone, and intent
   - Extract key phrases
   - Generate recommendations
   - Check for escalation conditions
3. **View Results**: Explore the comprehensive analysis dashboard
4. **Review History**: Enable "View Call History" to see previous analyses

### Supported File Formats
- **Audio**: MP3, WAV
- **Max File Size**: Depends on available memory (recommended: <50MB)
- **Duration**: No strict limit, but processing time increases with length

## 📊 Sample Output

### Analysis Dashboard
```
📝 Transcript
Agent: "Thank you for calling customer service, how can I help you today?"
Customer: "I'm having issues with my recent order..."

📊 Sentiment Score: -0.2 (Slightly Negative)
🏷️ Label: NEGATIVE
🎯 Customer Intent: Support Request - Customer needs assistance with order issues

🎙️ Tone Analysis:
- Agent Tone: Professional, helpful, empathetic
- Customer Tone: Frustrated but cooperative
- Tone Match: Good alignment

🔑 Key Phrases:
• "Order issues"
• "Need assistance"
• "Product defect"
• "Refund request"

💡 Recommendations:
1. Communication: Use more empathetic language early in conversation
2. Intent Handling: Streamline order issue resolution process
3. Closing: "I've resolved your order issue and ensured this won't happen again..."
```

### Escalation Alert Example
```
🚨 MANAGER ALERT 🚨
Multiple negative calls detected!
Pattern: 3 consecutive calls with negative sentiment
Recommended Action: Immediate manager intervention required
```

## 🔧 Technical Details

### AI Models Used
- **Transcription**: faster-whisper (tiny model for speed)
- **Sentiment Analysis**: 
  - TextBlob (lexicon-based approach)
  - Transformers (BERT-based classification)
- **LLM Processing**: Groq API with Llama3-70B-8192
- **Language Detection**: langdetect library

### Performance Specifications
- **Transcription Speed**: ~2x real-time processing
- **Analysis Latency**: <5 seconds per call
- **Memory Usage**: ~2-4GB during processing
- **Supported Languages**: Primarily English (extensible)

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/AmazingFeature`
3. **Commit Changes**: `git commit -m 'Add AmazingFeature'`
4. **Push to Branch**: `git push origin feature/AmazingFeature`
5. **Open Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Include unit tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Groq**: For providing fast LLM inference API
- **OpenAI**: For Whisper model architecture
- **Hugging Face**: For Transformers library
- **Streamlit**: For the amazing web framework
- **Python Community**: For excellent open-source libraries

