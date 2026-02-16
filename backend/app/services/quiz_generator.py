from app.services.llm_service import llm_service
from app.services.vector_db import vector_db
from app.models.schemas import Quiz, Question, QuizResult, QuestionResult
from typing import List, Dict
import uuid
from datetime import datetime

class QuizGenerator:
    def __init__(self):
        self.llm = llm_service
        self.vector_db = vector_db
    
    async def generate_quiz(
        self,
        user_id: str,
        email_content: str,
        num_questions: int = 5
    ) -> Quiz:
        """Generate a quiz from donor email content"""
        
        # Store email in vector DB for future reference
        email_id = str(uuid.uuid4())
        self.vector_db.add_email(
            email_id=email_id,
            content=email_content,
            metadata={
                "user_id": user_id,
                "created_at": datetime.now().isoformat()
            }
        )
        
        # Generate questions using LLM
        questions_data = self.llm.generate_quiz_questions(
            email_content=email_content,
            num_questions=num_questions
        )
        
        # Convert to Question objects
        questions = [
            Question(**q) for q in questions_data
        ]
        
        # Create quiz object
        quiz = Quiz(
            quiz_id=str(uuid.uuid4()),
            user_id=user_id,
            email_context=email_content,
            questions=questions,
            created_at=datetime.now()
        )
        
        return quiz
    
    async def evaluate_quiz(
        self,
        quiz: Quiz,
        user_answers: List[Dict[str, str]]
    ) -> QuizResult:
        """Evaluate user's quiz submission"""
        
        results = []
        correct_count = 0
        
        # Create answer lookup
        answer_map = {ans['question_id']: ans['selected_answer'] for ans in user_answers}
        
        for question in quiz.questions:
            user_answer = answer_map.get(question.id, "")
            is_correct = user_answer.strip().upper() == question.correct_answer.strip().upper()
            
            if is_correct:
                correct_count += 1
            
            # Generate detailed explanation
            detailed_explanation = self.llm.evaluate_answer(
                question=question.question_text,
                correct_answer=question.correct_answer,
                user_answer=user_answer,
                base_explanation=question.explanation,
                context=quiz.email_context[:500]
            )
            
            results.append(
                QuestionResult(
                    question_id=question.id,
                    question_text=question.question_text,
                    selected_answer=user_answer,
                    correct_answer=question.correct_answer,
                    is_correct=is_correct,
                    explanation=detailed_explanation
                )
            )
        
        # Calculate score
        total_questions = len(quiz.questions)
        score = (correct_count / total_questions) * 100
        
        # Generate summary
        summary = self.llm.generate_quiz_summary(
            score=score,
            total=total_questions,
            results=[r.dict() for r in results],
            email_context=quiz.email_context
        )
        
        return QuizResult(
            quiz_id=quiz.quiz_id,
            user_id=quiz.user_id,
            score=score,
            total_questions=total_questions,
            correct_answers=correct_count,
            results=results,
            summary=summary,
            completed_at=datetime.now()
        )

quiz_generator = QuizGenerator()