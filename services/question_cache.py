import json
import uuid

from api.models import MCQ, Essay
from utils.db.redis_question_cache import RedisQuestionCache


class QuestionCacheService:
    def __init__(self):
        self.__cache_id: str = f'session:{str(uuid.uuid4())}'
        self.__cache_db_client: RedisQuestionCache = RedisQuestionCache()
        self.__cache_db_client.init_db_setup()
        self.set_question_cache({
            'mcq': [],
            'essay': []
        })

    def get_question_cache(self) -> dict:
        cache_result = self.__cache_db_client.search(self.__cache_id)
        return json.loads(cache_result)['questions']

    def set_question_cache(self, data: dict) -> None:
        self.__cache_db_client.insert(self.__cache_id, json.dumps({'questions': data}))

    def update_question_cache(self, data: dict) -> None:
        self.__cache_db_client.update(self.__cache_id, json.dumps({'questions': data}))

    def get_already_constructed_mcq_stems(self) -> list:
        stems = []
        question_cache = self.get_question_cache()
        if 'mcq' in question_cache:
            mcqs = question_cache['mcq']
            for mcq in mcqs:
                stems.append(mcq['stem'])
        return stems

    def get_already_constructed_essay_questions(self) -> list:
        questions = []
        question_cache = self.get_question_cache()
        if 'essay' in question_cache:
            essays = question_cache['essay']
            for essay in essays:
                questions.append(essay['question'])
        return questions

    def get_already_constructed_mcq_items(self) -> list[MCQ]:
        question_cache = self.get_question_cache()
        mcq_items = []
        for mcq in question_cache['mcq']:
            mcq_model = MCQ(**mcq)
            mcq_items.append(mcq_model)
        return mcq_items

    def get_already_constructed_essay_items(self) -> list[Essay]:
        question_cache = self.get_question_cache()
        essay_items = []
        for essay in question_cache['essay']:
            essay_model = Essay(**essay)
            essay_items.append(essay_model)
        return essay_items

    def add_new_mcq_item(self, mcq: dict) -> None:
        questions = self.get_question_cache()
        if 'mcq' in questions:
            questions['mcq'].append(mcq)
        else:
            questions['mcq'] = [mcq]
        self.update_question_cache(questions)

    def add_new_essay_item(self, essay: dict) -> None:
        questions = self.get_question_cache()
        if 'essay' in questions:
            questions['essay'].append(essay)
        else:
            questions['essay'] = [essay]
        self.update_question_cache(questions)
