# 📚 Gaku - AI-Powered Lecture Summarizer

> **Gaku** (学) means "study" in Japanese

Transform your lecture recordings into comprehensive study materials with AI! Gaku transcribes audio lectures, generates beautifully formatted summaries, creates study tools, and provides an intelligent chatbot tutor.

[![Demo Video](https://img.shields.io/badge/▶️-Watch%20Demo-red?style=for-the-badge&logo=youtube)](https://drive.google.com/file/d/1pnvwGGCMAwcKgMnGfQ6DHixSJ4F0aAA7/view?usp=sharing)

---

## ✨ Features

### 🎤 **Audio Transcription**
- Upload lecture recordings (MP3, WAV, M4A, WEBM)
- Automatic transcription using AssemblyAI
- Supports files up to 200MB
- High-quality, punctuated transcripts
- Download transcripts as text files

### 📝 **Smart Summaries**
- AI-generated comprehensive study notes with beautiful Markdown formatting
- Organized sections:
  - 📚 Lecture Overview
  - 🎯 Key Concepts
  - 💡 Important Details
  - 📖 Definitions & Terminology
  - ✅ Key Takeaways
  - ❓ Study Questions
- Download summaries as text files

### 💬 **Intelligent AI Tutor**
- Chat with Gaku about the lecture content
- Ask questions and get instant, context-aware answers
- Markdown-formatted responses with bold emphasis
- Provides additional explanations when needed
- Real-time typing indicators and timestamps

### 🎯 **Study Tools**
- **Quiz Generator**: Create customizable multiple-choice quizzes (1-20 questions)
- **Flashcards**: Generate study flashcards (1-30 cards)
- Adjustable difficulty with slider controls

### 💾 **Smart Features**
- **Auto-save**: Sessions persist for 24 hours in browser
- **Download**: Export transcripts and summaries
- **File Validation**: Client and server-side checks
- **Error Handling**: User-friendly error messages
- **Session Recovery**: Resume where you left off

---

## 🛠️ Tech Stack

**Frontend:**
- HTML5, CSS3, JavaScript (ES6+)
- Marked.js for Markdown rendering
- Custom responsive UI with playful design

**Backend:**
- Python 3.12+
- Flask (Web Framework)
- Flask-CORS

**AI/ML Services:**
- **Google Gemini 2.5 Flash**: AI-powered summarization and intelligent chat
- **AssemblyAI**: High-quality audio transcription

**Other:**
- python-dotenv for environment variables
- LocalStorage for session persistence

---

## 📦 Installation

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)
- API Keys:
  - [Google Gemini API Key](https://ai.google.dev/)
  - [AssemblyAI API Key](https://www.assemblyai.com/)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/gaku-lecture-summarizer.git
cd gaku-lecture-summarizer
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
```

5. **Run the application**
```bash
python backend/api.py
```

6. **Open in browser**
```
http://127.0.0.1:5000
```

---

## 📖 Usage

### 1. Upload & Transcribe
1. Click "Browse files" and select your lecture audio file
2. Click "Transcribe Now" and wait for processing
3. Review and download the transcript

### 2. Generate Summary
1. Navigate to "View Summary"
2. Click "Generate Summary"
3. Review beautifully formatted notes with emojis and structure
4. Download the summary for offline study

### 3. Chat with Gaku
1. Go to "Chat with AI"
2. Ask questions about the lecture content
3. Get instant, intelligent responses with context
4. Chat history maintained during session

### 4. Use Study Tools
1. Open "Study Tools"
2. Adjust slider for number of questions/cards
3. Generate Quiz (1-20 questions with explanations)
4. Create Flashcards (1-30 Q&A pairs)

---

## 📁 Project Structure
```
gaku-lecture-summarizer/
├── backend/
│   ├── __init__.py
│   ├── api.py              # Flask application & routes
│   ├── transcriber.py      # AssemblyAI integration
│   ├── summarizer.py       # Gemini summarization
│   └── chatbot.py          # AI chat functionality
├── frontend/
│   ├── static/
│   │   └── app.js          # Frontend JavaScript
│   ├── index.html          # Main HTML file
│   ├── gaku_logo.png       # Logo
│   └── gaku_background.png # Background image
├── .env                    # Environment variables (not in repo)
├── .gitignore
├── LICENSE.txt
├── requirements.txt        # Python dependencies
└── README.md
```

---

## 🔒 Security & Privacy

- API keys are stored in `.env` (never committed to Git)
- Temporary files are automatically deleted after transcription
- Local session data expires after 24 hours
- No permanent data storage on server
- All processing happens server-side

---

## 🚀 Future Enhancements

- [ ] Support for video files (extract audio)
- [ ] Multiple language support
- [ ] Export summaries as PDF
- [ ] Real-time collaboration
- [ ] Mobile app version
- [ ] Integration with note-taking apps (Notion, Evernote)
- [ ] Speaker diarization (identify different speakers)
- [ ] Timestamp-based navigation in audio
- [ ] Custom quiz difficulty levels
- [ ] Spaced repetition system for flashcards
- [ ] Dark mode

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

**Attribution Requirement**: Any forks, modifications, or derivative works must credit the original author: Jothika Pydi

---

## 👩‍💻 Author

**Jothika SaiPydi**
 
- LinkedIn:Jothika sai Pydi(https://linkedin.com/in/jothika-sai-pydi-1bba3328a)
- GitHub: [Jothika2506](https://github.com/Jothika2506)

---

## 🙏 Acknowledgments

- [Google Gemini](https://ai.google.dev/) for powerful AI capabilities
- [AssemblyAI](https://www.assemblyai.com/) for accurate transcription
- [Marked.js](https://marked.js.org/) for Markdown rendering
- Inspired by the need for better study tools for students worldwide

---

## ⭐ Support

If you found this project helpful, please consider giving it a ⭐ on GitHub!

---

<div align="center">
  <strong>Made with ❤️ for students everywhere</strong>
  <br>
  <sub>Turning hours of lectures into minutes of learning</sub>
</div>
