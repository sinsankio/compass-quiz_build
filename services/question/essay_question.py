from typing import Any

from configs.question.essay.answer_construct import ANSWER_EVALUATE_CUTOFFS
from configs.question.essay.question_construct import QUESTION_EVALUATE_CUTOFFS
from entities.blooms_taxonomy_level import EssayBloomsTaxonomyLevel
from entities.difficulty_level import DifficultyLevel
from entities.question.essay.question_type import EssayQuestionType
from services.question.template import QuestionService
from services.question_cache import QuestionCacheService
from utils.question.essay.question_construct import str_cast_pool_essay_questions
from utils.question.essay.question_construct_eval_crew import CrewInit
from utils.question.essay.question_construct_eval_crew import (
    kickoff_question_construct_eval_crew,
    kickoff_answer_construct_eval_crew
)
from utils.question.essay.supervision import load_essay_question_construction_supervision, load_bt_supervision


class EssayQuestionService(QuestionService):
    QUESTION_EVALUATE_CRITERIA: set = {
        'question_type_relevance_score',
        'knowledge_context_score',
        'difficulty_level_score',
        'non_existence_level_score',
        'bt_level_score',
        'essay_question_guideline_score'
    }
    ANSWER_EVALUATE_CRITERIA: set = {
        'answer_type_relevance_score',
        'question_context_biasness',
        'difficulty_level_score',
        'essay_question_guideline_score'
    }

    @staticmethod
    def evaluate(eval_result: Any, eval_criteria: set, eval_cutoffs: dict):
        if type(eval_result) is not dict:
            return False
        if not eval_criteria == set(eval_result.keys()):
            return False
        for criteria in eval_criteria:
            if eval_result[criteria] < eval_cutoffs[criteria]:
                return False
        return True

    @staticmethod
    def evaluate_question(eval_result: Any) -> bool:
        return EssayQuestionService.evaluate(
            eval_result,
            EssayQuestionService.QUESTION_EVALUATE_CRITERIA,
            QUESTION_EVALUATE_CUTOFFS
        )

    @staticmethod
    def evaluate_answer(eval_result: Any) -> bool:
        return EssayQuestionService.evaluate(
            eval_result,
            EssayQuestionService.ANSWER_EVALUATE_CRITERIA,
            ANSWER_EVALUATE_CUTOFFS
        )

    @staticmethod
    def construct_question(
            crew_init: CrewInit,
            question_cache_service: QuestionCacheService,
            subject_description: str,
            knowledge_context: str,
            essay_type: EssayQuestionType = EssayQuestionType.RESTRICTED_RESPONSE,
            blooms_taxonomy_level: EssayBloomsTaxonomyLevel = EssayBloomsTaxonomyLevel.APPLICATION,
            difficulty_level: DifficultyLevel = DifficultyLevel.EASY,
            essay_construction_guide: str = load_essay_question_construction_supervision()
    ) -> dict:
        blooms_taxonomy_supervision = load_bt_supervision(essay_type, blooms_taxonomy_level)
        crew_exec_result = kickoff_question_construct_eval_crew(
            crew_init,
            subject_area=subject_description,
            essay_type=essay_type.value,
            difficulty_level=difficulty_level,
            knowledge_context=knowledge_context,
            bt_level=blooms_taxonomy_level.value,
            bt_model_guide=blooms_taxonomy_supervision['model_guide'],
            bt_level_guide=blooms_taxonomy_supervision['level_guide'],
            bt_level_examples=blooms_taxonomy_supervision['examples'],
            pool_essay_questions=str_cast_pool_essay_questions(
                question_cache_service.get_already_constructed_essay_questions()
            ),
            essay_construction_guide=essay_construction_guide
        )
        if EssayQuestionService.evaluate_question(crew_exec_result['question-evaluate-task-result']):
            return crew_exec_result['question-format-task-result']
        return EssayQuestionService.construct_question(
            crew_init,
            question_cache_service,
            subject_description,
            knowledge_context,
            essay_type,
            blooms_taxonomy_level,
            difficulty_level,
            essay_construction_guide
        )

    @staticmethod
    def construct_answer(
            crew_init: CrewInit,
            subject_description: str,
            essay_question: str,
            knowledge_context: str,
            min_word_count: int | str = 50,
            max_word_count: int | str = 100,
            essay_type: EssayQuestionType = EssayQuestionType.RESTRICTED_RESPONSE,
            difficulty_level: DifficultyLevel = DifficultyLevel.EASY,
            essay_construction_guide: str = load_essay_question_construction_supervision()
    ) -> dict:
        crew_exec_result = kickoff_answer_construct_eval_crew(
            crew_init=crew_init,
            subject_area=subject_description,
            essay_question=essay_question,
            essay_type=essay_type.value,
            difficulty_level=difficulty_level.value,
            knowledge_context=knowledge_context,
            min_word_count=min_word_count,
            max_word_count=max_word_count,
            essay_construction_guide=essay_construction_guide
        )
        if EssayQuestionService.evaluate_answer(crew_exec_result['answer-evaluate-task-result']):
            return crew_exec_result['answer-format-task-result']
        return EssayQuestionService.construct_answer(
            crew_init,
            subject_description,
            essay_question,
            knowledge_context,
            min_word_count,
            max_word_count,
            essay_type,
            difficulty_level,
            essay_construction_guide
        )

    @staticmethod
    def construct(
            question_crew_init: CrewInit,
            answer_crew_init: CrewInit,
            question_cache_service: QuestionCacheService,
            subject_description: str,
            knowledge_context: str,
            min_word_count: int | str = 100,
            max_word_count: int | str = 200,
            essay_type: EssayQuestionType = EssayQuestionType.RESTRICTED_RESPONSE,
            blooms_taxonomy_level: EssayBloomsTaxonomyLevel = EssayBloomsTaxonomyLevel.APPLICATION,
            difficulty_level: DifficultyLevel = DifficultyLevel.EASY
    ) -> dict:
        question = EssayQuestionService.construct_question(
            question_crew_init,
            question_cache_service,
            subject_description,
            knowledge_context,
            essay_type,
            blooms_taxonomy_level,
            difficulty_level
        )
        answer = EssayQuestionService.construct_answer(
            answer_crew_init,
            subject_description,
            question['question'],
            knowledge_context,
            min_word_count,
            max_word_count,
            essay_type,
            difficulty_level
        )
        return {
            'question': question['question'],
            'answer': answer['answer'],
            'type': essay_type.value
        }

    @staticmethod
    def backup():
        pass
