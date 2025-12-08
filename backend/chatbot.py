import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class LectureChatbot:
    def __init__(self):
        """Initialize the chatbot with Google Gemini"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')

        self.chat_history = []
        self.lecture_context = None
    
    def set_lecture_context(self, transcript_text):
        """
        Set the lecture transcript as context for the chatbot
        
        Args:
            transcript_text: The full lecture transcription
        """
        self.lecture_context = transcript_text
        self.chat_history = []
        print(f"✅ Lecture context set ({len(transcript_text)} characters)")
    
    def ask_question(self, question):
        """
        Ask a question about the lecture
        
        Args:
            question: User's question about the lecture
            
        Returns:
            dict: Contains answer and status
        """
        if not self.lecture_context:
            return {
                'status': 'error',
                'answer': '⚠️ No lecture has been transcribed yet. Please:\n\n1. Go to "Upload & Transcribe"\n2. Upload your audio file\n3. Click "Transcribe Now"\n4. Then come back here to chat!',
                'error': 'No context'
            }
        
        try:
            # Create a comprehensive prompt with context
            prompt = f"""
You are Gaku, a helpful AI tutor assisting a student with their lecture notes. Your goal is to help them understand the material better.

LECTURE CONTENT:
{self.lecture_context}

PREVIOUS CONVERSATION:
{self._format_chat_history()}

STUDENT'S QUESTION:
{question}

INSTRUCTIONS:
- **PRIMARY**: Always try to answer based on the lecture content first
- **If the question is directly about the lecture**: Use ONLY the lecture content
- **If asking for definitions/concepts mentioned but not fully explained in the lecture**: Provide the definition AND mention if it was covered in the lecture or not
- **If the question is a follow-up or asks for clarification**: You can use general knowledge to help them understand better, but always tie it back to the lecture when possible
- **If completely unrelated to the lecture**: Politely redirect them to ask about the lecture material

RESPONSE STYLE:
- Use **Markdown formatting** with **bold** for emphasis and key terms
- Use bullet points (-) for lists
- Be clear, helpful, and encouraging
- Keep answers concise but complete (2-4 paragraphs max)
- Use examples when helpful

EXAMPLE GOOD RESPONSES:
- "Based on the lecture, **virtualization** is... [from lecture]. Let me add some context: [general knowledge if helpful]"
- "The lecture covered **Type 2 hypervisors** which are... [from lecture]"
- "While the lecture didn't define **containerization** in detail, it's related to the virtualization concepts discussed. Let me explain: [definition]"

Your answer in Markdown:
"""
            
            print(f"💬 Processing question: {question[:50]}...")
            response = self.model.generate_content(prompt)
            answer = response.text
            
            # Add to chat history (keep only last 10 exchanges)
            self.chat_history.append({
                'question': question,
                'answer': answer
            })
            
            # Limit chat history to prevent memory issues
            if len(self.chat_history) > 10:
                self.chat_history = self.chat_history[-10:]
            
            print(f"✅ Answer generated ({len(answer)} characters)")
            
            return {
                'status': 'success',
                'answer': answer,
                'error': None
            }
            
        except Exception as e:
            print(f"❌ Error answering question: {str(e)}")
            return {
                'status': 'error',
                'answer': None,
                'error': str(e)
            }
    
    def _format_chat_history(self):
        """Format chat history for context"""
        if not self.chat_history:
            return "No previous questions."
        
        formatted = []
        for i, item in enumerate(self.chat_history[-5:], 1):  # Last 5 questions
            formatted.append(f"Q{i}: {item['question']}\nA{i}: {item['answer']}\n")
        
        return "\n".join(formatted)
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []
        print("🗑️ Chat history cleared")
    
    def get_quiz_questions(self, num_questions=5):
        """
        Generate quiz questions based on the lecture
        
        Args:
            num_questions: Number of quiz questions to generate
            
        Returns:
            dict: Contains questions and status
        """
        if not self.lecture_context:
            return {
                'status': 'error',
                'questions': None,
                'error': 'No lecture context set. Please transcribe a lecture first.'
            }
        
        try:
            prompt = f"""
Based on this lecture, create {num_questions} multiple-choice quiz questions to test understanding.

LECTURE CONTENT:
{self.lecture_context}

Format each question EXACTLY like this:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUESTION 1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Your question here]

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

✅ CORRECT ANSWER: [Letter]

💡 EXPLANATION: [Why this is correct and why others are wrong]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUESTION 2
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Your question here]

A) [Option A]
B) [Option B]
C) [Option C]
D) [Option D]

✅ CORRECT ANSWER: [Letter]

💡 EXPLANATION: [Why this is correct and why others are wrong]

...and so on.

GUIDELINES:
- Make questions that test understanding, not just memorization
- Include a mix of difficulty levels
- Ensure all options are plausible
- Base questions only on content from the lecture
- Provide clear, educational explanations

Create exactly {num_questions} questions following this format.
"""
            
            print(f"📝 Generating {num_questions} quiz questions...")
            response = self.model.generate_content(prompt)
            
            print(f"✅ Quiz generated successfully")
            
            return {
                'status': 'success',
                'questions': response.text,
                'error': None
            }
            
        except Exception as e:
            print(f"❌ Error generating quiz: {str(e)}")
            return {
                'status': 'error',
                'questions': None,
                'error': str(e)
            }
    
    def explain_concept(self, concept):
        """
        Get detailed explanation of a specific concept from the lecture
        
        Args:
            concept: The concept to explain
            
        Returns:
            dict: Contains explanation and status
        """
        if not self.lecture_context:
            return {
                'status': 'error',
                'explanation': None,
                'error': 'No lecture context set. Please transcribe a lecture first.'
            }
        
        try:
            prompt = f"""
From this lecture, provide a detailed explanation of: "{concept}" using MARKDOWN formatting.

LECTURE CONTENT:
{self.lecture_context}

Structure your explanation using PROPER MARKDOWN:

---

# 🎯 CONCEPT: {concept}

---

## 📖 Simple Definition

[Explain it in 2-3 sentences using simple, clear language that anyone can understand. Avoid jargon unless necessary.]

---

## 📚 Context from Lecture

[Explain how this concept was presented in the lecture. Include:]

- The main points discussed
- Specific examples or details mentioned
- How it relates to the overall topic

---

## 💡 Key Examples

**Example 1**: [Concrete example, either from the lecture or a practical one]

**Example 2**: [Another example to illustrate the concept clearly]

[Add more examples if helpful]

---

## 🔗 Related Concepts

- **Related Concept 1**: Brief explanation of how they connect
- **Related Concept 2**: Brief explanation of how they connect
- **Related Concept 3**: Brief explanation of how they connect

---

## ✅ Why It Matters

[Explain in 2-3 sentences:]
- The practical importance or application
- Why students should understand this
- Real-world relevance if applicable

---

**FORMATTING RULES**:
- Use # for main heading, ## for subheadings
- Use **bold** for emphasis and key terms
- Use - for bullet lists
- Use --- for horizontal dividers
- NO ASCII boxes or special Unicode characters
- Use proper Markdown syntax only

**IMPORTANT NOTE**: If the concept "{concept}" wasn't directly covered in the lecture, politely explain this and suggest related topics from the lecture that might be helpful instead.
"""
            
            print(f"💡 Explaining concept: {concept}")
            response = self.model.generate_content(prompt)
            
            print(f"✅ Explanation generated")
            
            return {
                'status': 'success',
                'explanation': response.text,
                'error': None
            }
            
        except Exception as e:
            print(f"❌ Error explaining concept: {str(e)}")
            return {
                'status': 'error',
                'explanation': None,
                'error': str(e)
            }