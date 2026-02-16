import google.generativeai as genai
from app.config import settings
from typing import List, Dict
import json

class LLMService:
    def __init__(self):
        # Configure Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.gemini_model = genai.GenerativeModel('gemini-pro')
    
    def generate_completion(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """Generate completion using Gemini"""
        # Combine system prompt and user prompt for Gemini
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        
        response = self.gemini_model.generate_content(
            full_prompt,
            generation_config=generation_config
        )
        return response.text
    
    def generate_quiz_questions(
        self,
        email_content: str,
        num_questions: int = 5
    ) -> List[Dict]:
        """Generate quiz questions from email content"""
        system_prompt = """You are an expert educational assessment designer specializing in non-profit and donor management topics. 
        Create challenging, thought-provoking questions that test deep understanding, not just recall.
        Always respond with valid JSON format."""
        
        prompt = f"""Based on the following donor email, generate {num_questions} multiple-choice questions that test understanding of:
        - Non-profit best practices
        - Donor relationships and stewardship
        - Fundraising strategies
        - Impact measurement
        - Ethical considerations in non-profit work

Email Content:
{email_content}

Generate questions in the following JSON format (MUST be valid JSON):
{{
    "questions": [
        {{
            "id": "q1",
            "question_text": "What is the primary focus of this donor communication?",
            "options": ["A) Financial reporting", "B) Program updates", "C) Event invitation", "D) Volunteer recruitment"],
            "correct_answer": "A",
            "explanation": "Detailed explanation of why this is correct and why others are wrong. Connect to non-profit best practices.",
            "difficulty": "medium"
        }}
    ]
}}

IMPORTANT:
1. Generate exactly {num_questions} questions
2. Each question must be contextually relevant to the email
3. Test comprehension and application, not just facts
4. Have clear, unambiguous correct answers (A, B, C, or D)
5. Include comprehensive explanations that teach
6. Mix difficulty levels (easy, medium, hard)
7. Return ONLY valid JSON, no markdown formatting
"""
        
        response = self.generate_completion(prompt, system_prompt, temperature=0.8, max_tokens=3000)
        
        # Parse JSON response
        try:
            # Clean the response
            response = response.strip()
            
            # Remove markdown code blocks if present
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            data = json.loads(response)
            questions = data.get("questions", [])
            
            # Validate questions
            if len(questions) != num_questions:
                print(f"Warning: Expected {num_questions} questions, got {len(questions)}")
            
            return questions
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(f"Response: {response}")
            return []
    
    def evaluate_answer(
        self,
        question: str,
        correct_answer: str,
        user_answer: str,
        base_explanation: str = "",
        context: str = ""
    ) -> str:
        """Generate detailed explanation for answer"""
        is_correct = correct_answer.strip().upper() == user_answer.strip().upper()
        
        prompt = f"""Question: {question}
Correct Answer: {correct_answer}
User's Answer: {user_answer}
Result: {"✓ Correct" if is_correct else "✗ Incorrect"}
Base Explanation: {base_explanation}
Context: {context}

Provide a detailed, educational explanation (2-3 paragraphs) that:
1. {"Reinforces why this answer is correct" if is_correct else "Explains why the user's answer is incorrect"}
2. Clarifies the reasoning behind the correct answer
3. Provides additional context and learning points about non-profit management
4. Connects to broader concepts in donor relations, fundraising, or non-profit operations
5. {"Acknowledges the user's knowledge" if is_correct else "Offers encouragement and learning resources"}

Keep the tone professional, encouraging, and educational. Focus on building understanding."""
        
        return self.generate_completion(prompt, temperature=0.7, max_tokens=800)
    
    def generate_quiz_summary(
        self,
        score: float,
        total: int,
        results: List[Dict],
        email_context: str = ""
    ) -> str:
        """Generate personalized quiz summary"""
        
        # Analyze performance
        correct_count = sum(1 for r in results if r['is_correct'])
        incorrect_topics = [r['question_text'][:50] + "..." for r in results if not r['is_correct']]
        
        prompt = f"""Generate a personalized learning summary for a user who completed a non-profit knowledge assessment.

Performance:
- Score: {score}% ({correct_count}/{total} correct)
- Questions answered: {total}

Quiz Context:
{email_context[:300]}...

Incorrect Questions:
{json.dumps(incorrect_topics, indent=2) if incorrect_topics else "None - Perfect score!"}

Provide a comprehensive summary that includes:

1. **Performance Overview** (1 paragraph)
   - Overall assessment of their understanding
   - Comparison to typical learner performance
   
2. **Strengths Identified** (2-3 bullet points)
   - Specific areas where they demonstrated strong knowledge
   - Skills they've mastered
   
3. **Growth Opportunities** (2-3 bullet points)
   - Specific concepts to review
   - Areas for deeper study
   
4. **Actionable Recommendations** (3-4 specific suggestions)
   - Resources to explore
   - Practical steps to improve
   - Topics to focus on
   
5. **Encouragement & Next Steps** (1 paragraph)
   - Motivational message
   - Suggested learning path

Keep it:
- Constructive and positive
- Specific and actionable
- Professional yet encouraging
- Focused on non-profit sector expertise

Format with clear sections using markdown."""
        
        return self.generate_completion(prompt, temperature=0.7, max_tokens=1500)

llm_service = LLMService()