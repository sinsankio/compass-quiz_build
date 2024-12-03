from services.file_upload import FileUploadService
from services.knowledge.lecture_note_knowledge import LectureNoteKnowledgeService
from services.question.essay_question import EssayQuestionService
from services.question.export.doc_export import DocExportService
from services.question.mcq import MCQService
from services.user import UserService
from utils.db.mongo_nosql import MongoNoSQL


class QuizPlanService(
    LectureNoteKnowledgeService,
    MCQService,
    EssayQuestionService,
    FileUploadService,
    UserService,
    DocExportService
):
    MONGO_COLLECTION_NAME: str = "quiz_plans"

    @staticmethod
    def create_question_plan(db_client: MongoNoSQL, quiz_plan: dict, user: dict) -> dict | None:
        if plan_id := db_client.insert(QuizPlanService.MONGO_COLLECTION_NAME, quiz_plan):
            if quiz_plan := db_client.search(QuizPlanService.MONGO_COLLECTION_NAME, {'_id': plan_id}):
                user['quizPlans'].append(quiz_plan)
                return quiz_plan

    @staticmethod
    def get_question_plan(db_client: MongoNoSQL, plan_id: str) -> dict | None:
        return db_client.search(QuizPlanService.MONGO_COLLECTION_NAME, {'_id': plan_id})

    @staticmethod
    def get_user_question_plan_pos(plan_id: str, user: dict) -> int | None:
        for i in range(len(user['quizPlans'])):
            if user['quizPlans'][i]['_id'] == plan_id:
                return i + 1

    @staticmethod
    def get_user_question_plan(plan_id: str, user: dict) -> dict | None:
        for quiz_plan in user['quizPlans']:
            if quiz_plan['_id'] == plan_id:
                return quiz_plan

    @staticmethod
    def get_question_plan_for_quiz_construction(plan_id: str, user: dict) -> dict | None:
        if quiz_plan := QuizPlanService.get_user_question_plan(plan_id, user):
            if knowledge_base := LectureNoteKnowledgeService.get_user_knowledge_base(
                    user,
                    quiz_plan['knowledgeBaseId']
            ):
                i = 0
                while i < len(quiz_plan['questionStructures']):
                    structure = quiz_plan['questionStructures'][i]
                    if isinstance(structure['topic'], str):
                        if topic := LectureNoteKnowledgeService.get_quiz_plan_knowledge_base_topic(knowledge_base,
                                                                                                   structure['topic']):
                            structure['topic'] = topic
                            i += 1
                        else:
                            quiz_plan['questionStructures'].pop(i)
                    else:
                        i += 1
                quiz_plan['subjectDescription'] = knowledge_base['subjectDescription']
                return quiz_plan

    @staticmethod
    def update_question_plan(db_client: MongoNoSQL, plan_id: str, updated_quiz_plan: dict, user: dict) -> dict | None:
        if pos := QuizPlanService.get_user_question_plan_pos(plan_id, user):
            if db_client.update(
                    QuizPlanService.MONGO_COLLECTION_NAME,
                    {'_id': plan_id},
                    updated_quiz_plan
            ).modified_count >= 1:
                if updated_quiz_plan := QuizPlanService.get_question_plan(db_client, plan_id):
                    user['quizPlans'][pos - 1] = updated_quiz_plan
                    return updated_quiz_plan

    @staticmethod
    def delete_question_plan(db_client: MongoNoSQL, plan_id: str, user: dict) -> int | None:
        if pos := QuizPlanService.get_user_question_plan_pos(plan_id, user):
            if deleted_count := db_client.delete(
                    QuizPlanService.MONGO_COLLECTION_NAME, {'_id': plan_id}).deleted_count:
                user['quizPlans'].pop(pos - 1)
                return deleted_count
