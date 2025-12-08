import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class Summarizer:
    def __init__(self):
        """Initialize the summarizer with Google Gemini"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    def generate_summary(self, transcript_text):
        """
        Generate a comprehensive summary of the lecture with enhanced formatting
        
        Args:
            transcript_text: The full lecture transcription
            
        Returns:
            dict: Contains summary, key points, and status
        """
        try:
            prompt = f"""
You are an expert educational note-taker. Create comprehensive, well-structured study notes from this lecture using PROPER MARKDOWN FORMATTING.

LECTURE TRANSCRIPT:
{transcript_text}

Create notes using MARKDOWN with this structure:

# 📚 LECTURE OVERVIEW

[Write 2-3 clear sentences summarizing the entire lecture - what was covered and why it matters. Make this engaging and easy to understand.]

---

# 🎯 KEY CONCEPTS

**1. CONCEPT NAME**  
→ Brief explanation in 1-2 sentences using simple language

**2. CONCEPT NAME**  
→ Brief explanation in 1-2 sentences using simple language

**3. CONCEPT NAME**  
→ Brief explanation in 1-2 sentences using simple language

[Continue for all main concepts...]

---

# 💡 IMPORTANT DETAILS

- **Detail Title**: Specific fact, data, or example with context
- **Detail Title**: Specific fact, data, or example with context
- **Detail Title**: Specific fact, data, or example with context

[Continue for all important details...]

---

# 📖 DEFINITIONS & TERMINOLOGY

**Term 1**: Clear, concise definition in simple words

**Term 2**: Clear, concise definition in simple words

**Term 3**: Clear, concise definition in simple words

[Continue for all important terms...]

---

# ✅ KEY TAKEAWAYS

1. **Main Takeaway**: Explain why this matters and what students should remember

2. **Main Takeaway**: Explain why this matters and what students should remember

3. **Main Takeaway**: Explain why this matters and what students should remember

[Continue for 3-5 takeaways...]

---

# ❓ STUDY QUESTIONS

1. [Thought-provoking question that tests understanding, not memorization]

2. [Thought-provoking question that tests understanding, not memorization]

3. [Thought-provoking question that tests understanding, not memorization]

[Continue for 3-5 questions...]

---

**CRITICAL FORMATTING RULES**:
- Use # for main headings
- Use **bold** for emphasis and sub-headings
- Use - for bullet lists
- Use 1. 2. 3. for numbered lists
- Use --- for horizontal dividers between sections
- Use → for arrows/explanations
- NO ASCII art boxes or special characters
- Keep language simple and clear
"""
            
            print("Generating enhanced summary with Gemini...")
            response = self.model.generate_content(prompt)
            
            return {
                'status': 'success',
                'summary': response.text,
                'error': None
            }
            
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return {
                'status': 'error',
                'summary': None,
                'error': str(e)
            }
    
    def generate_study_guide(self, transcript_text):
        """
        Generate a structured study guide
        
        Args:
            transcript_text: The full lecture transcription
            
        Returns:
            dict: Contains study guide and status
        """
        try:
            prompt = f"""
Create a comprehensive study guide from this lecture transcript. Include:

1. Main Topics Covered
2. Detailed explanations of each topic
3. Examples mentioned
4. Questions for self-assessment (5-10 questions)
5. Key takeaways

Lecture Transcript:
{transcript_text}

Make it well-structured and easy to study from.
"""
            
            print("Generating study guide...")
            response = self.model.generate_content(prompt)
            
            return {
                'status': 'success',
                'study_guide': response.text,
                'error': None
            }
            
        except Exception as e:
            print(f"Error generating study guide: {str(e)}")
            return {
                'status': 'error',
                'study_guide': None,
                'error': str(e)
            }
    
    def generate_flashcards(self, transcript_text, num_cards=10):
        """
        Generate flashcards for studying
        
        Args:
            transcript_text: The full lecture transcription
            num_cards: Number of flashcards to generate
            
        Returns:
            dict: Contains flashcards and status
        """
        try:
            prompt = f"""
Create {num_cards} flashcards from this lecture to help students study effectively using MARKDOWN formatting.

LECTURE TRANSCRIPT:
{transcript_text}

Format each flashcard using PROPER MARKDOWN:

---

## 🎴 CARD 1

### ❓ Question
[Write a clear, concise question that tests understanding]

### ✅ Answer
[Provide a comprehensive answer with key details. Use bullet points if needed:]
- Main point 1
- Main point 2
- Main point 3

---

## 🎴 CARD 2

### ❓ Question
[Write a clear, concise question that tests understanding]

### ✅ Answer
[Provide a comprehensive answer with key details. Use bullet points if needed:]
- Main point 1
- Main point 2
- Main point 3

---

[Continue this pattern for all {num_cards} cards...]

**FORMATTING RULES**:
- Use ## for card headers
- Use ### for Question/Answer subheaders
- Use - for bullet lists in answers
- Use --- for dividers between cards
- Use **bold** for emphasis
- NO ASCII boxes or special Unicode characters
- Use proper Markdown syntax only

**IMPORTANT GUIDELINES**:
- Questions should test **understanding**, not just memorization
- Cover **different topics** from the lecture
- Include both **conceptual** and **factual** questions
- Make answers **clear and complete** with key details
- Use **simple language** that's easy to understand
- Use **bullet points** in answers when listing multiple points
"""
            
            print(f"Generating {num_cards} flashcards...")
            response = self.model.generate_content(prompt)
            
            return {
                'status': 'success',
                'flashcards': response.text,
                'error': None
            }
            
        except Exception as e:
            print(f"Error generating flashcards: {str(e)}")
            return {
                'status': 'error',
                'flashcards': None,
                'error': str(e)
            }