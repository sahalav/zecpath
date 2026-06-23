from .models import JobQuestion


class QuestionEngine:

    def get_questions(self, job_id):

        questions = JobQuestion.objects.filter(
            job_id=job_id
        )

        return [
            q.question.question_text
            for q in questions
        ]
class AIFlowManager:

    def next_question(
        self,
        current_index
    ):

        return current_index + 1

class AIBridgeService:

    def generate_question(self):

        return {
            "question":
            "Tell me about yourself"
        }

    def evaluate_answer(
        self,
        answer
    ):

        return {
            "score": 80
        }

class VoiceCallService:

    def trigger_call(
        self,
        phone
    ):

        return {
            "status":
            "call_initiated"
        }
def has_feature(subscription, feature):

    plans = {

        "FREE": [
            "job_post"
        ],

        "PREMIUM": [
            "job_post",
            "analytics",
            "ai_ranking"
        ],

        "ENTERPRISE": [
            "job_post",
            "analytics",
            "ai_ranking",
            "prediction"
        ]
    }

    return feature in plans.get(
        subscription.plan_name,
        []
    )