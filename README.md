# 📚 AI Study Buddy

> An AI-powered learning assistant that transforms study materials into concise summaries, interactive quizzes, revision flashcards, and intelligent question-answering using **Google Gemini AI**.

---

## 🌟 Overview

AI Study Buddy is a Generative AI-powered web application developed to simplify the learning experience for students. Instead of manually creating notes or searching through lengthy PDFs, users can upload their study material and instantly generate:

- 📄 Smart Summaries
- ❓ Multiple Choice Questions (MCQs)
- 🃏 Revision Flashcards
- 💬 AI-powered Question Answering

The application converts static study resources into an interactive and personalized learning platform.

---

## 🚀 Features

- 📤 Upload study material in PDF format
- 📄 Generate concise AI-powered summaries
- ❓ Automatically create MCQs for self-assessment
- 🃏 Generate revision flashcards
- 💬 Ask questions directly from the uploaded document
- 🎨 Modern and responsive Streamlit interface
- 🔒 Secure API key management using environment variables

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| Streamlit | Interactive web application |
| Google Gemini AI | Generative AI for content generation |
| PyPDF2 | PDF text extraction |
| python-dotenv | Secure API key management |
| Git & GitHub | Version control |

---

## 🧠 Workflow

```text
                User Uploads PDF
                       │
                       ▼
          Extract Text using PyPDF2
                       │
                       ▼
             Google Gemini AI Model
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
   Generate        Generate      Generate
   Summary          MCQs        Flashcards
                       │
                       ▼
              Answer User Queries
                       │
                       ▼
              Display Results in
              Streamlit Interface
```

---

### 🏠 Home Page

> Upload study material through a clean and modern interface.

---

### 📄 AI Summary Generation

> Generate concise and easy-to-understand summaries from uploaded notes.

---

### ❓ MCQ Generation

> Automatically create multiple-choice questions for self-evaluation.

---

### 🃏 Flashcards

> Quickly revise important concepts using AI-generated flashcards.

---

### 💬 Ask Questions

> Ask questions from the uploaded PDF and receive context-aware answers.

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/parikramagargav/AI-Study-Buddy.git
```

### Navigate to the project

```bash
cd AI-Study-Buddy
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```env
GEMINI_API_KEY=YOUR_API_KEY
```

### Run the application

```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
AI-Study-Buddy/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env (not included)
```

---

## 🎯 Future Enhancements

- 🌍 Multi-language support
- 🎤 Voice-based interaction
- 📱 Mobile application
- 📊 Learning progress tracking
- 📥 Export summaries as PDF
- 🎯 Personalized study recommendations

---

## 🌐 Live Demo

**Live Application**

https://ai-study-buddyyyy.streamlit.app/

---

## 💻 GitHub Repository

https://github.com/parikramagargav/AI-Study-Buddy

---

## 👨‍💻 Developed By

**Parikrama Gargav**

B.Tech CSE Core  
VIT Bhopal University

---

## 📜 License

This project was developed as part of the **Edunet Foundation AI Internship Capstone Project** for educational and learning purposes.
