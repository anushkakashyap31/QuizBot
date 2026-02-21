from google import genai
from google.genai import types
from app.config import settings
from typing import List, Dict
import json
import time
import random
import re

class LLMService:
    def __init__(self):
        """Initialize Gemini AI service"""
        # Configure with new package
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        print("✓ Gemini AI service initialized with google.genai package")
    
    def generate_completion(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        retry_count: int = 3,
        backoff_factor: float = 2.0
    ) -> str:
        """Generate completion using Gemini with exponential backoff retry logic"""
        
        # Combine prompts
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        for attempt in range(retry_count):
            try:
                print(f"🤖 Generating completion (attempt {attempt + 1}/{retry_count})...")
                
                # Use new API
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=max_tokens,
                    )
                )
                
                # Extract text from response
                if response.text:
                    print(f"✓ Generation successful ({len(response.text)} chars)")
                    return response.text
                else:
                    print(f"⚠️ Empty response on attempt {attempt + 1}")
                    if attempt < retry_count - 1:
                        wait_time = backoff_factor ** attempt + random.uniform(0, 1)
                        print(f"⏳ Waiting {wait_time:.2f}s before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise Exception("Gemini returned empty response after all retries")
                        
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Attempt {attempt + 1} failed: {error_msg}")
                
                # Check for specific errors
                if "429" in error_msg or "quota" in error_msg.lower():
                    print("⚠️ Rate limit hit, using longer backoff...")
                    wait_time = (backoff_factor ** (attempt + 2)) + random.uniform(0, 2)
                elif "500" in error_msg or "503" in error_msg:
                    print("⚠️ Server error, retrying with backoff...")
                    wait_time = backoff_factor ** attempt + random.uniform(0, 1)
                else:
                    wait_time = backoff_factor ** attempt + random.uniform(0, 1)
                
                if attempt < retry_count - 1:
                    print(f"⏳ Waiting {wait_time:.2f}s before retry...")
                    time.sleep(wait_time)
                else:
                    print(f"❌ All {retry_count} attempts failed")
                    raise Exception(f"Failed after {retry_count} attempts: {error_msg}")
    
    def generate_quiz_questions(
        self,
        email_content: str,
        num_questions: int = 5
    ) -> List[Dict]:
        """Generate quiz questions from donor email content"""
        
        print(f"\n{'='*60}")
        print(f"📧 Generating {num_questions} quiz questions from email")
        print(f"{'='*60}\n")
        
        # Truncate email if too long
        original_length = len(email_content)
        if len(email_content) > 3000:
            email_content = email_content[:3000] + "..."
            print(f"📝 Email truncated from {original_length} to 3000 chars")
        
        system_prompt = """You are an expert educational assessment designer specializing in non-profit management, donor relations, and fundraising.

Your task is to create challenging, thought-provoking multiple-choice questions that test deep understanding, not just recall.

CRITICAL RULES:
1. Return ONLY valid JSON - no markdown, no code blocks, no explanations
2. Questions must be clear, specific, and challenging
3. Explanations must be detailed and educational
4. Focus on non-profit best practices and ethics
5. Use simple, direct language
6. Ensure all strings are properly closed"""
        
        prompt = f"""Based on this donor email, generate EXACTLY {num_questions} multiple-choice questions about non-profit management, donor relations, fundraising practices, and ethical considerations in valid JSON format.

=== EMAIL CONTENT ===
{email_content}
=== END EMAIL ===

Return ONLY a JSON object in this EXACT format (no markdown, no backticks, no other text):

{{
    "questions": [
        {{
            "id": "q1",
            "question_text": "Based on the email, what is the primary purpose of the donation acknowledgment letter?",
            "options": [
                "A) To provide tax documentation for the donor",
                "B) To request additional donations",
                "C) To promote upcoming events",
                "D) To advertise the organization's programs"
            ],
            "correct_answer": "A",
            "explanation": "Detailed explanation of why A is correct and why other options are incorrect. Should be 2-3 sentences focusing on non-profit best practices.",
            "difficulty": "medium"
        }}
    ]
}}

REQUIREMENTS:
- Generate EXACTLY {num_questions} questions
- Each question must relate to the email content
- Correct answer must be ONLY the letter: A, B, C, or D
- Each option must start with the letter, close paren, and space (e.g., "A) ")
- Difficulty can be: "easy", "medium", or "hard"
- Explanations must be substantive (2-3 sentences minimum)
- Questions should test understanding, not just recall
- Focus on practical non-profit management concepts
- Return ONLY the JSON object, nothing else"""
        
        try:
            # Generate with retry logic
            response = self.generate_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=5000,
                retry_count=5,
                backoff_factor=2.0
            )
            
            # Clean the response
            response = response.strip()
            print(f"📄 Raw response length: {len(response)} chars")
            
            # Remove markdown code blocks if present
            if "```json" in response:
                print("🔧 Removing ```json markdown...")
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                print("🔧 Removing ``` markdown...")
                response = response.split("```")[1].split("```")[0].strip()
            
            # Additional cleaning
            response = response.replace('\n', ' ').replace('\r', '')
            
            # Try to fix common JSON issues
            # Add closing brace if missing
            open_braces = response.count('{')
            close_braces = response.count('}')
            if open_braces > close_braces:
                response += '}' * (open_braces - close_braces)
            
            # Parse JSON
            print("🔍 Parsing JSON response...")
            try:
                data = json.loads(response)
            except json.JSONDecodeError as e:
                # If parsing fails, try to extract just the questions array
                print(f"⚠️ Initial parse failed, trying to extract questions array...")
                match = re.search(r'"questions"\s*:\s*\[(.*)\]', response, re.DOTALL)
                if match:
                    questions_str = '[' + match.group(1) + ']'
                    try:
                        questions_list = json.loads(questions_str)
                        data = {'questions': questions_list}
                    except:
                        # Final fallback - return default quiz
                        print("⚠️ Failed to parse, using fallback quiz...")
                        return self._get_fallback_quiz(num_questions)
                else:
                    # Can't extract - use fallback
                    print("⚠️ Could not extract questions, using fallback quiz...")
                    return self._get_fallback_quiz(num_questions)

            questions = data.get("questions", [])
            
            print(f"✓ Successfully generated {len(questions)} questions")
            
            if len(questions) == 0:
                print("⚠️ No questions in response, using fallback quiz...")
                return self._get_fallback_quiz(num_questions)
            
            # Validate each question has required fields
            required_fields = ['id', 'question_text', 'options', 'correct_answer', 'explanation', 'difficulty']
            valid_questions = []
            for i, q in enumerate(questions):
                missing = [f for f in required_fields if f not in q]
                if missing:
                    print(f"⚠️ Question {i+1} missing fields: {', '.join(missing)}, skipping...")
                    continue
                
                # Validate options format
                if len(q['options']) != 4:
                    print(f"⚠️ Question {i+1} doesn't have 4 options, skipping...")
                    continue

                # Validate correct answer
                if q['correct_answer'] not in ['A', 'B', 'C', 'D']:
                    print(f"⚠️ Question {i+1} has invalid answer, fixing to 'A'...")
                    q['correct_answer'] = 'A'
                
                valid_questions.append(q)            
            
            if len(valid_questions) == 0:
                print("⚠️ No valid questions, using fallback quiz...")
                return self._get_fallback_quiz(num_questions)
            
            print(f"\n{'='*60}")
            print(f"✅ Quiz generation complete! {len(valid_questions)} valid questions")
            print(f"{'='*60}\n")
            
            return valid_questions[:num_questions]
            
        except Exception as e:
            print(f"❌ Error generating questions: {str(e)}")
            print("⚠️ Using fallback quiz...")
            return self._get_fallback_quiz(num_questions)
    
    def _get_fallback_quiz(self, num_questions: int) -> List[Dict]:
        """Generate a fallback quiz when AI generation fails"""
        fallback_questions = [
            {
                "id": "q1",
                "question_text": "What is the primary purpose of acknowledging donations in non-profit organizations?",
                "options": [
                    "A) To provide tax documentation",
                    "B) To request more donations",
                    "C) To advertise programs",
                    "D) To recruit volunteers"
                ],
                "correct_answer": "A",
                "explanation": "Acknowledgment letters provide donors with necessary tax documentation for their charitable contributions.",
                "difficulty": "medium"
            },
            {
                "id": "q2",
                "question_text": "What does 501(c)(3) status signify for a non-profit organization?",
                "options": [
                    "A) Tax-exempt status allowing tax-deductible donations",
                    "B) Permission to conduct political campaigns",
                    "C) Authorization to sell products",
                    "D) Requirement to pay corporate taxes"
                ],
                "correct_answer": "A",
                "explanation": "501(c)(3) status means the organization is tax-exempt and donations to it are tax-deductible.",
                "difficulty": "easy"
            },
            {
                "id": "q3",
                "question_text": "Why is donor stewardship important in non-profit management?",
                "options": [
                    "A) It builds long-term relationships and encourages future giving",
                    "B) It is legally required by the IRS",
                    "C) It replaces the need for fundraising",
                    "D) It eliminates the need for program evaluation"
                ],
                "correct_answer": "A",
                "explanation": "Donor stewardship helps maintain relationships with supporters and encourages continued support.",
                "difficulty": "medium"
            },
            {
                "id": "q4",
                "question_text": "What information should a donation receipt include?",
                "options": [
                    "A) Donation amount, date, and organization's tax ID",
                    "B) Only the donor's name",
                    "C) Staff salaries",
                    "D) Future fundraising goals"
                ],
                "correct_answer": "A",
                "explanation": "Proper receipts must include the amount, date, and tax identification for IRS purposes.",
                "difficulty": "easy"
            },
            {
                "id": "q5",
                "question_text": "How soon should a non-profit acknowledge a donation?",
                "options": [
                    "A) Within 48-72 hours for best practice",
                    "B) Within 6 months",
                    "C) Only at year-end",
                    "D) Acknowledgment is optional"
                ],
                "correct_answer": "A",
                "explanation": "Timely acknowledgment (within 2-3 days) shows respect and professionalism.",
                "difficulty": "medium"
            }
        ]
        
        return fallback_questions[:num_questions]
    
    def evaluate_answer(
        self,
        question: str,
        correct_answer: str,
        user_answer: str,
        base_explanation: str = "",
        context: str = ""
    ) -> str:
        """Generate detailed explanation for user's answer with retry logic"""
        is_correct = correct_answer.strip().upper() == user_answer.strip().upper()
        
        prompt = f"""Provide a detailed explanation for this quiz question answer.

Question: {question}
Correct Answer: {correct_answer}
User's Answer: {user_answer}
Result: {"✓ CORRECT" if is_correct else "✗ INCORRECT"}

Base Explanation: {base_explanation}

Write 2-3 paragraphs that:
1. {"Reinforces why this answer is correct and acknowledges the user's knowledge" if is_correct else "Explains what the correct answer is and why the user's choice was incorrect"}
2. Provides brief context about non-profit management best practices
3. {"Encourages continued learning" if is_correct else "Offers constructive guidance for improvement"}

Keep the tone professional, educational, and encouraging."""
        
        try:
            return self.generate_completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=500,
                retry_count=3,
                backoff_factor=2.0
            )
        except Exception as e:
            print(f"⚠️ Failed to generate detailed explanation, using fallback: {e}")
            return base_explanation if base_explanation else f"The correct answer is {correct_answer}."
    
    def generate_quiz_summary(
        self,
        score: float,
        total: int,
        results: List[Dict],
        email_context: str = ""
    ) -> str:
        """Generate personalized quiz summary with retry logic"""
        correct_count = sum(1 for r in results if r.get('is_correct', False))
        incorrect_count = total - correct_count
        
        prompt = f"""Generate a personalized, encouraging learning summary for a non-profit education quiz.

QUIZ RESULTS:
- Score: {score}% ({correct_count}/{total} correct)
- Questions answered correctly: {correct_count}
- Questions answered incorrectly: {incorrect_count}

Create a summary with these sections:

1. PERFORMANCE OVERVIEW (1 paragraph)
   - Acknowledge their score
   - {"Celebrate their achievement" if score >= 80 else "Encourage continued learning"}

2. STRENGTHS (2-3 bullet points)
   - Specific areas they demonstrated understanding
   - {"Highlight their excellent performance" if score >= 90 else "Note what they got right"}

3. GROWTH AREAS (2-3 bullet points)
   - {f"Topics needing more attention (they missed {incorrect_count} questions)" if incorrect_count > 0 else "Areas for deeper understanding"}
   - Be constructive, not critical

4. RECOMMENDATIONS (3-4 bullet points)
   - Specific, actionable next steps
   - Resources or topics to study
   - How to apply this knowledge

5. ENCOURAGEMENT (1 paragraph)
   - Motivating closing statement
   - Reinforce the value of non-profit education
   - {"Congratulate their achievement" if score >= 80 else "Encourage them to keep learning"}

Keep the tone professional, supportive, and action-oriented. Focus on growth mindset."""
        
        try:
            return self.generate_completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=1200,
                retry_count=3,
                backoff_factor=2.0
            )
        except Exception as e:
            print(f"⚠️ Failed to generate detailed summary, using fallback: {e}")
            performance = "Excellent work!" if score >= 80 else "Good effort!" if score >= 60 else "Keep practicing!"
            return f"""QUIZ SUMMARY

You scored {score}% on this non-profit management assessment ({correct_count} out of {total} questions correct). {performance}

{"You demonstrated strong understanding of non-profit concepts. " if score >= 80 else ""}Review the explanations for each question to strengthen your understanding of donor relations, fundraising best practices, and ethical considerations in non-profit management.

Continue learning and applying these principles to become more effective in the non-profit sector."""

# Initialize singleton instance
llm_service = LLMService()