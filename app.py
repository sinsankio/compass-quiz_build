import os

from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from fastapi import (
    FastAPI,
    Body,
    status,
    HTTPException,
    Query,
    Form,
    UploadFile
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse

from api.models import (
    QuizPlan,
    QuizPlanForQuizBuild,
    UpdatableQuizPlan,
    Knowledge,
    KnowledgeInit,
    User,
    Authentication,
    AllowedFileNames,
    Quiz,
    McqQuestionStructure,
    EssayQuestionStructure,
    Topic
)
from configs.api import get_base_router
from entities.question.essay.question_type import EssayQuestionType
from services.question.essay_question import EssayQuestionService
from services.question.mcq import MCQService
from services.question_cache import QuestionCacheService
from services.quiz_plan import QuizPlanService
from utils.datetime import get_time_duration
from utils.db.mongo_nosql import MongoNoSQL
from utils.question.essay.answer_construct import (
    init_answer_construct_format_agent,
    init_answer_evaluate_agent,
    init_answer_construct_task,
    init_answer_format_task,
    init_answer_evaluate_task
)
from utils.question.essay.question_construct import (
    init_question_construct_format_agent,
    init_question_evaluate_agent,
    init_question_construct_task,
    init_question_format_task,
    init_question_evaluate_task
)
from utils.question.essay.question_construct_eval_crew import CrewInit as EssayCrewInit
from utils.question.mcq.alternative_option_format import (
    init_alternative_option_format_agent,
    init_alternative_option_evaluate_agent,
    init_alternative_option_format_task,
    init_alternative_option_evaluate_task
)
from utils.question.mcq.distractor_construct import (
    init_distractor_construct_agent,
    init_distractor_evaluate_agent,
    init_distractor_construct_task,
    init_distractor_evaluate_task
)
from utils.question.mcq.key_construct import (
    init_key_construct_agent,
    init_key_evaluate_agent,
    init_key_construct_task,
    init_key_evaluate_task
)
from utils.question.mcq.question_construct_eval_crew import CrewInit as McqCrewInit
from utils.question.mcq.stem_construct import (
    init_stem_construct_format_agent,
    init_stem_evaluate_agent,
    init_stem_construct_task,
    init_stem_format_task,
    init_stem_evaluate_task
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongo_client = MongoNoSQL()
    app.mongo_client.init_db_setup()
    yield
    app.mongo_client.close()


app = FastAPI(lifespan=lifespan)
base_router = get_base_router()


@base_router.post(
    path='/users',
    response_description='create new user',
    status_code=status.HTTP_200_OK,
    response_model=User
)
async def create_user(user: User = Body()) -> dict | None:
    if user := QuizPlanService.create_user(app.mongo_client, jsonable_encoder(user)):
        return user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user creation failed')


@base_router.get(
    path='/users',
    response_description='retrieve users',
    status_code=status.HTTP_200_OK,
    response_model=list[User]
)
async def get_users() -> list[dict]:
    if users := QuizPlanService.get_users(app.mongo_client):
        return users
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user retrieval failed')


@base_router.post(
    path='/plans',
    response_description='initialize question plan',
    status_code=status.HTTP_200_OK,
    response_model=QuizPlan
)
async def create_question_plan(auth: Authentication = Body(),
                               quiz_plan: QuizPlan = Body(alias="quizPlan")) -> dict | None:
    if auth_user := QuizPlanService.auth_user(app.mongo_client, auth.api_key):
        if quiz_plan := QuizPlanService.create_question_plan(app.mongo_client, jsonable_encoder(quiz_plan), auth_user):
            if _ := QuizPlanService.update_user(app.mongo_client, auth.api_key, auth_user):
                return quiz_plan
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user updation failed')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='quiz plan initialization failed')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


@base_router.post(
    path='/plan',
    response_description='retrieve question plan',
    status_code=status.HTTP_200_OK,
    response_model=QuizPlan
)
async def get_question_plan(auth: Authentication = Body(), plan_id: str = Query(alias='pId')) -> dict | None:
    if auth_user := QuizPlanService.auth_user(app.mongo_client, auth.api_key):
        if quiz_plan := QuizPlanService.get_user_question_plan(plan_id, auth_user):
            return quiz_plan
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='quiz plan retrieval failed')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


@base_router.post(
    path='/plans-all',
    response_description='retrieve question plans',
    status_code=status.HTTP_200_OK,
    response_model=list[QuizPlan]
)
async def get_question_plans(auth: Authentication = Body()) -> list[dict]:
    if auth_user := QuizPlanService.auth_user(app.mongo_client, auth.api_key):
        return auth_user['quizPlans']
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


@base_router.put(
    path='/plans',
    response_description='update question plan',
    status_code=status.HTTP_200_OK,
    response_model=QuizPlan
)
async def update_question_plan(auth: Authentication = Body(), plan_id: str = Query(alias='pId'),
                               updated_quiz_plan: UpdatableQuizPlan = Body(alias='updatedQuizPlan')) -> dict | None:
    if auth_user := QuizPlanService.auth_user(app.mongo_client, auth.api_key):
        if updated_quiz_plan := QuizPlanService.update_question_plan(
                app.mongo_client,
                plan_id,
                jsonable_encoder(updated_quiz_plan),
                auth_user
        ):
            if _ := QuizPlanService.update_user(app.mongo_client, auth.api_key, auth_user):
                return updated_quiz_plan
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user updation failed')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='quiz plan updation failed')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


@base_router.delete(
    path='/plans',
    response_description='delete question plan',
    status_code=status.HTTP_200_OK
)
async def delete_question_plan(auth: Authentication = Body(), plan_id: str = Query(alias='pId')) -> int | None:
    if auth_user := QuizPlanService.auth_user(app.mongo_client, auth.api_key):
        if deleted_count := QuizPlanService.delete_question_plan(app.mongo_client, plan_id, auth_user):
            if _ := QuizPlanService.update_user(app.mongo_client, auth.api_key, auth_user):
                return deleted_count
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user updation failed')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='quiz plan deletion failed')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


@base_router.post(
    path='/knowledges/lecture-note-files',
    response_description='upload lecture note files',
    status_code=status.HTTP_200_OK
)
async def upload_lecture_note_files(files: list[UploadFile], api_key: str = Form(alias='apiKey')) -> dict | None:
    if _ := QuizPlanService.auth_user(app.mongo_client, api_key):
        knowledge = KnowledgeInit().model_dump()
        if QuizPlanService.upload_files(knowledge['id'], files):
            return knowledge
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='lecture note uploading failed')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


@base_router.post(
    path='/knowledges/lecture-note-file-names',
    response_description='retrieve existing lecture note file names',
    status_code=status.HTTP_200_OK
)
async def get_existing_lecture_note_file_names(knowledge_id: str = Query(alias='kId'),
                                               auth: Authentication = Body()) -> list | None:
    if QuizPlanService.auth_user(app.mongo_client, auth.api_key):
        return QuizPlanService.get_existing_file_names(knowledge_id)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


@base_router.patch(
    path='/knowledges/lecture-note-files',
    response_description='update existing lecture note files',
    status_code=status.HTTP_200_OK
)
async def update_existing_lecture_note_files(
        auth: Authentication = Body(),
        knowledge_id: str = Query(alias='kId'),
        allowed_file_names: AllowedFileNames = Body(alias='allowedFileNames')
) -> list | None:
    if QuizPlanService.auth_user(app.mongo_client, auth.api_key):
        file_names = QuizPlanService.update_existing_files(
            knowledge_id,
            jsonable_encoder(allowed_file_names)['fileNames']
        )
        if file_names is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='modification of existing lecture note files failed')
        return file_names
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


@base_router.put(
    path='/knowledges/lecture-note-files',
    response_description='update existing lecture note materials by uploading more',
    status_code=status.HTTP_200_OK
)
async def add_new_lecture_note_files(
        files: list[UploadFile],
        kid: str = Form(alias='kId'),
        api_key: str = Form(alias='apiKey')
) -> list | None:
    if QuizPlanService.auth_user(app.mongo_client, api_key):
        if file_names := QuizPlanService.add_new_files(kid, files):
            return file_names
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='addition of new lecture note files failed')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


@base_router.delete(
    path='/knowledges/lecture-note-files',
    response_description='delete all the existing lecture note materials',
    status_code=status.HTTP_200_OK
)
async def delete_existing_lecture_note_files(
        knowledge_id: str = Query(alias='kId'),
        auth: Authentication = Body()
) -> bool | None:
    if QuizPlanService.auth_user(app.mongo_client, auth.api_key):
        if QuizPlanService.delete_existing_files(knowledge_id):
            return True
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='deletion of existing lecture note files failed')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


@base_router.post(
    path='/knowledges',
    response_description='create knowledge base',
    status_code=status.HTTP_200_OK,
    response_model=Knowledge
)
async def create_knowledge_base(
        auth: Authentication = Body(),
        knowledge: Knowledge = Body(),
        num_topics: int | None = Query(default=None, ge=1, alias='topics')
) -> dict | None:
    if auth_user := QuizPlanService.auth_user(app.mongo_client, auth.api_key):
        if knowledge := QuizPlanService.create_knowledge_base(
                app.mongo_client,
                jsonable_encoder(knowledge),
                auth_user,
                num_topics
        ):
            if _ := QuizPlanService.update_user(app.mongo_client, auth.api_key, auth_user):
                return knowledge
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user updation failed')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='knowledge base initialization failed')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


@base_router.post(
    path='/knowledge',
    response_description='retrieve knowledge base',
    status_code=status.HTTP_200_OK,
    response_model=Knowledge
)
async def get_knowledge_base(auth: Authentication = Body(), knowledge_id: str = Query(alias='kId')) -> dict | None:
    if auth_user := QuizPlanService.auth_user(app.mongo_client, auth.api_key):
        if knowledge := QuizPlanService.get_user_knowledge_base(auth_user, knowledge_id):
            return knowledge
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='knowledge base retrieval failed')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


@base_router.post(
    path='/knowledges-all',
    response_description='retrieve knowledge bases',
    status_code=status.HTTP_200_OK,
    response_model=list[Knowledge]
)
async def get_knowledge_bases(auth: Authentication = Body()) -> list[dict]:
    if auth_user := QuizPlanService.auth_user(app.mongo_client, auth.api_key):
        return auth_user['knowledgeBases']
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


@base_router.put(
    path='/knowledges',
    response_description='update knowledge base',
    status_code=status.HTTP_200_OK,
    response_model=Knowledge
)
async def update_knowledge_base(
        auth: Authentication = Body(),
        updated_knowledge: Knowledge = Body(alias='updatedKnowledge'),
        num_topics: int | None = Query(default=None, ge=1, alias='topics')
) -> dict | None:
    if auth_user := QuizPlanService.auth_user(app.mongo_client, auth.api_key):
        if updated_knowledge := QuizPlanService.update_knowledge_base(
                app.mongo_client,
                jsonable_encoder(updated_knowledge),
                auth_user,
                num_topics
        ):
            if _ := QuizPlanService.update_user(app.mongo_client, auth.api_key, auth_user):
                return updated_knowledge
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user updation failed')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='knowledge base updation failed')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


@base_router.delete(
    path='/knowledges',
    response_description='delete knowledge base',
    status_code=status.HTTP_200_OK
)
async def delete_knowledge_base(auth: Authentication = Body(), knowledge_id: str = Query(alias='kId')) -> bool | None:
    if auth_user := QuizPlanService.auth_user(app.mongo_client, auth.api_key):
        if deleted_count := QuizPlanService.delete_knowledge_base(app.mongo_client, knowledge_id, auth_user):
            if _ := QuizPlanService.update_user(app.mongo_client, auth.api_key, auth_user):
                return deleted_count
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user updation failed')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='knowledge base deletion failed')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


@base_router.post(
    path='/quiz',
    response_description='construct quiz',
    status_code=status.HTTP_200_OK,
    response_model=QuizPlan
)
async def construct_quiz(auth: Authentication = Body(), plan_id: str = Query(alias='pId')):
    if auth_user := QuizPlanService.auth_user(app.mongo_client, auth.api_key):
        if quiz_plan := QuizPlanForQuizBuild(
                **QuizPlanService.get_question_plan_for_quiz_construction(plan_id, auth_user)):
            question_cache_service = QuestionCacheService()
            stem_crew_init = McqCrewInit()
            key_crew_init = McqCrewInit()
            distractor_crew_init = McqCrewInit()
            alternatives_crew_init = McqCrewInit()
            question_crew_init = EssayCrewInit()
            answer_crew_init = EssayCrewInit()

            stem_crew_init.agents = [init_stem_construct_format_agent(), init_stem_evaluate_agent()]
            stem_crew_init.tasks = [init_stem_construct_task(), init_stem_format_task(), init_stem_evaluate_task()]
            key_crew_init.agents = [init_key_construct_agent(), init_key_evaluate_agent()]
            key_crew_init.tasks = [init_key_construct_task(), init_key_evaluate_task()]
            distractor_crew_init.agents = [init_distractor_construct_agent(), init_distractor_evaluate_agent()]
            distractor_crew_init.tasks = [init_distractor_construct_task(), init_distractor_evaluate_task()]
            alternatives_crew_init.agents = [init_alternative_option_format_agent(),
                                             init_alternative_option_evaluate_agent()]
            alternatives_crew_init.tasks = [init_alternative_option_format_task(),
                                            init_alternative_option_evaluate_task()]
            question_crew_init.agents = [init_question_construct_format_agent(), init_question_evaluate_agent()]
            question_crew_init.tasks = [init_question_construct_task(), init_question_format_task(),
                                        init_question_evaluate_task()]
            answer_crew_init.agents = [init_answer_construct_format_agent(), init_answer_evaluate_agent()]
            answer_crew_init.tasks = [init_answer_construct_task(), init_answer_format_task(),
                                      init_answer_evaluate_task()]

            build_start_datetime = datetime.now()
            if quiz_plan.question_structures:
                for question_structure in quiz_plan.question_structures:
                    if isinstance(question_structure, McqQuestionStructure) and isinstance(question_structure.topic,
                                                                                           Topic):
                        for i in range(question_structure.num_questions):
                            mcq_item = MCQService.construct(
                                stem_crew_init,
                                key_crew_init,
                                distractor_crew_init,
                                alternatives_crew_init,
                                question_cache_service,
                                quiz_plan.subject_description,
                                question_structure.topic.summarized_content,
                                question_structure.num_distractors,
                                question_structure.blooms_taxonomy_level,
                                question_structure.difficulty_level
                            )
                            question_cache_service.add_new_mcq_item(mcq_item)
                    elif isinstance(question_structure, EssayQuestionStructure) and isinstance(question_structure.topic,
                                                                                               Topic):
                        for i in range(question_structure.num_questions):
                            essay_item = EssayQuestionService.construct(
                                question_crew_init,
                                answer_crew_init,
                                question_cache_service,
                                quiz_plan.subject_description,
                                question_structure.topic.summarized_content,
                                question_structure.min_word_count,
                                question_structure.max_word_count,
                                question_structure.question_type,
                                question_structure.blooms_taxonomy_level,
                                question_structure.difficulty_level
                            )
                            question_cache_service.add_new_essay_item(essay_item)
                mcqs = question_cache_service.get_already_constructed_mcq_items()
                essays = question_cache_service.get_already_constructed_essay_items()
                quiz_dict = {
                    'mcqs': mcqs,
                    'essays': essays,
                    'buildTime': get_time_duration(build_start_datetime, datetime.now())
                }
                quiz = Quiz(**quiz_dict)
                quiz_plan.quizzes.append(quiz)
                if updated_quiz_plan := QuizPlanService.update_question_plan(app.mongo_client, plan_id,
                                                                             jsonable_encoder(quiz_plan), auth_user):
                    if _ := QuizPlanService.update_user(app.mongo_client, auth.api_key, auth_user):
                        return updated_quiz_plan
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user updation failed')
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='quiz plan updation failed')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='no any question structure available')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='no matching quiz plan available')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


@base_router.delete(
    path='/quiz',
    response_description='delete quiz',
    status_code=status.HTTP_200_OK,
    response_model=QuizPlan
)
async def delete_quiz(auth: Authentication = Body(), plan_id: str = Query(alias='pId'),
                      quiz_id: str = Query(alias='qId')):
    if auth_user := QuizPlanService.auth_user(app.mongo_client, auth.api_key):
        if pos := QuizPlanService.get_user_question_plan_pos(plan_id, auth_user):
            for i in range(len(auth_user['quizPlans'][pos - 1]['quizzes'])):
                if auth_user['quizPlans'][pos - 1]['quizzes'][i]['_id'] == quiz_id:
                    auth_user['quizPlans'][pos - 1]['quizzes'].pop(i)
                    if updated_quiz_plan := QuizPlanService.update_question_plan(
                            app.mongo_client,
                            plan_id,
                            auth_user['quizPlans'][pos - 1],
                            auth_user
                    ):
                        if _ := QuizPlanService.update_user(app.mongo_client, auth.api_key, auth_user):
                            return updated_quiz_plan
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='user updation failed')
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='quiz plan updation failed')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='quiz retrieval failed')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='quiz plan retrieval failed')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


@base_router.post(
    path='/quiz/export',
    response_description='export quiz',
    status_code=status.HTTP_200_OK,
    response_class=FileResponse
)
async def export_quiz(auth: Authentication = Body(), plan_id: str = Query(alias='pId'),
                      quiz_id: str = Query(alias='qId')):
    if auth_user := QuizPlanService.auth_user(app.mongo_client, auth.api_key):
        if quiz_plan := QuizPlanService.get_user_question_plan(plan_id, auth_user):
            for quiz in quiz_plan['quizzes']:
                if quiz['_id'] == quiz_id:
                    if quiz['mcqs'] or quiz['essays']:
                        export_file_save_path = QuizPlanService.generate_export(
                            quiz_plan['subjectDescription'],
                            quiz['mcqs'],
                            [essay for essay in quiz['essays'] if
                             essay['type'] == EssayQuestionType.RESTRICTED_RESPONSE.value],
                            [essay for essay in quiz['essays'] if
                             essay['type'] == EssayQuestionType.EXTENDED_RESPONSE.value]
                        )
                        return FileResponse(
                            path=export_file_save_path,
                            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                        )
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='null quiz without questions')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='quiz retrieval failed')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='quiz plan retrieval failed')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized access')


if __name__ == "__main__":
    app.include_router(base_router)
    try:
        uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))
    except KeyboardInterrupt:
        pass
