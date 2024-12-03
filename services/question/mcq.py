from typing import Any

from configs.question.mcq.alternative_option_format import ALTERNATIVE_OPTION_EVALUATE_CUTOFFS
from configs.question.mcq.distractor_construct import DISTRACTOR_EVALUATE_CUTOFFS
from configs.question.mcq.key_construct import KEY_EVALUATE_CUTOFFS
from configs.question.mcq.stem_construct import STEM_EVALUATE_CUTOFFS
from entities.blooms_taxonomy_level import McqBloomsTaxonomyLevel
from entities.difficulty_level import DifficultyLevel
from entities.prompt_number import PromptNumber
from services.question.template import QuestionService
from services.question_cache import QuestionCacheService
from utils.question.mcq.question_construct_eval_crew import CrewInit
from utils.question.mcq.question_construct_eval_crew import (
    kickoff_stem_construct_eval_crew,
    kickoff_key_construct_eval_crew,
    kickoff_distractor_construct_eval_crew,
    kickoff_alternative_option_format_eval_crew,
)
from utils.question.mcq.stem_construct import str_cast_pool_mcq_stems
from utils.question.mcq.supervision import (
    load_blooms_taxonomy_supervision,
    load_mcq_construction_supervision
)


class MCQService(QuestionService):
    STEM_EVALUATE_CRITERIA: set = {
        'knowledge_context_score',
        'difficulty_level_score',
        'non_existence_level_score',
        'bt_level_score',
        'mcq_guideline_score'
    }
    KEY_EVALUATE_CRITERIA: set = {
        'knowledge_context_score',
        'stem_context_score',
        'difficulty_level_score',
        'mcq_guideline_score'
    }
    DISTRACTOR_EVALUATE_CRITERIA: set = {
        'requested_distractor_count_score',
        'knowledge_context_score',
        'key_similarity_score',
        'difficulty_level_score',
        'distraction_level_score',
        'mcq_guideline_score'
    }
    ALTERNATIVE_OPTION_EVALUATE_CRITERIA: set = {
        'requested_distractor_count_score',
        'plausible_and_attractive_score',
        'mutual_exclusive_score',
        'length_equality_score',
        'mcq_guideline_score'
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
    def evaluate_stem(eval_result: Any) -> bool:
        return MCQService.evaluate(eval_result, MCQService.STEM_EVALUATE_CRITERIA, STEM_EVALUATE_CUTOFFS)

    @staticmethod
    def evaluate_key(eval_result: Any) -> bool:
        return MCQService.evaluate(eval_result, MCQService.KEY_EVALUATE_CRITERIA, KEY_EVALUATE_CUTOFFS)

    @staticmethod
    def evaluate_distractors(eval_result: Any) -> bool:
        return MCQService.evaluate(
            eval_result,
            MCQService.DISTRACTOR_EVALUATE_CRITERIA,
            DISTRACTOR_EVALUATE_CUTOFFS
        )

    @staticmethod
    def evaluate_alternative_options(eval_result: Any) -> bool:
        return MCQService.evaluate(
            eval_result,
            MCQService.ALTERNATIVE_OPTION_EVALUATE_CRITERIA,
            ALTERNATIVE_OPTION_EVALUATE_CUTOFFS
        )

    @staticmethod
    def construct_stem(
            crew_init: CrewInit,
            question_cache_service: QuestionCacheService,
            subject_description: str,
            knowledge_context: str,
            blooms_taxonomy_level: McqBloomsTaxonomyLevel = McqBloomsTaxonomyLevel.KNOWLEDGE,
            difficulty_level: DifficultyLevel = DifficultyLevel.EASY,
            mcq_construction_guide: str = load_mcq_construction_supervision()
    ) -> dict:
        blooms_taxonomy_supervision = load_blooms_taxonomy_supervision(blooms_taxonomy_level)
        crew_exec_result = kickoff_stem_construct_eval_crew(
            crew_init=crew_init,
            subject_area=subject_description,
            difficulty_level=difficulty_level.value,
            knowledge_context=knowledge_context,
            bt_model_guide=blooms_taxonomy_supervision['model_guide'],
            bt_level=blooms_taxonomy_level.value,
            bt_level_guide=blooms_taxonomy_supervision['level_guide'],
            bt_level_examples=blooms_taxonomy_supervision['examples'],
            pool_mcq_stems=str_cast_pool_mcq_stems(question_cache_service.get_already_constructed_mcq_stems()),
            mcq_construction_guide=mcq_construction_guide
        )
        if MCQService.evaluate_stem(crew_exec_result['stem-evaluate-task-result']):
            # implement embedding save
            return crew_exec_result['stem-format-task-result']
        return MCQService.construct_stem(
            crew_init,
            question_cache_service,
            subject_description,
            knowledge_context,
            blooms_taxonomy_level,
            difficulty_level
        )

    @staticmethod
    def construct_key(
            crew_init: CrewInit,
            stem: str,
            subject_description: str,
            knowledge_context: str,
            difficulty_level: DifficultyLevel = DifficultyLevel.EASY,
            mcq_construction_guide: str = load_mcq_construction_supervision()
    ) -> dict:
        crew_exec_result = kickoff_key_construct_eval_crew(
            crew_init=crew_init,
            stem=stem,
            subject_area=subject_description,
            difficulty_level=difficulty_level.value,
            knowledge_context=knowledge_context,
            mcq_construction_guide=mcq_construction_guide
        )
        if MCQService.evaluate_key(crew_exec_result['key-evaluate-task-result']):
            return crew_exec_result['key-construct-task-result']
        return MCQService.construct_key(crew_init, stem, subject_description, knowledge_context, difficulty_level)

    @staticmethod
    def construct_distractors(
            crew_init: CrewInit,
            stem: str,
            key: str,
            subject_description: str,
            knowledge_context: str,
            num_distractors: PromptNumber = PromptNumber.FOUR,
            difficulty_level: DifficultyLevel = DifficultyLevel.EASY,
            mcq_construction_guide: str = load_mcq_construction_supervision()
    ) -> dict:
        crew_exec_result = kickoff_distractor_construct_eval_crew(
            crew_init=crew_init,
            stem=stem,
            key=key,
            subject_area=subject_description,
            difficulty_level=difficulty_level.value,
            knowledge_context=knowledge_context,
            num_distractors=num_distractors.value,
            mcq_construction_guide=mcq_construction_guide
        )
        if MCQService.evaluate_distractors(crew_exec_result['distractor-evaluate-task-result']):
            return crew_exec_result['distractor-construct-task-result']
        return MCQService.construct_distractors(
            crew_init,
            stem,
            key,
            subject_description,
            knowledge_context,
            num_distractors,
            difficulty_level
        )

    @staticmethod
    def format_options(
            crew_init: CrewInit,
            subject_description: str,
            stem: str,
            alternatives: list,
            non_formatted_key: str,
            num_alternatives: PromptNumber = PromptNumber.FIVE,
            mcq_construction_guide: str = load_mcq_construction_supervision()
    ) -> dict:
        crew_exec_result = kickoff_alternative_option_format_eval_crew(
            crew_init=crew_init,
            stem=stem,
            subject_area=subject_description,
            non_formatted_key=non_formatted_key,
            non_formatted_options=alternatives,
            num_alternatives=num_alternatives.value,
            mcq_construction_guide=mcq_construction_guide
        )
        if MCQService.evaluate_alternative_options(crew_exec_result['alternatives-evaluate-task-result']):
            return crew_exec_result['alternatives-format-task-result']
        return MCQService.format_options(
            crew_init,
            subject_description,
            stem,
            alternatives,
            non_formatted_key,
            num_alternatives
        )

    @staticmethod
    def construct(
            stem_construct_eval_crew_init: CrewInit,
            key_construct_eval_crew_init: CrewInit,
            distractor_construct_eval_crew_init: CrewInit,
            alternatives_format_eval_crew_init: CrewInit,
            question_cache_service: QuestionCacheService,
            subject_description: str,
            knowledge_context: str,
            num_alternatives: PromptNumber = PromptNumber.FIVE,
            blooms_taxonomy_level: McqBloomsTaxonomyLevel = McqBloomsTaxonomyLevel.KNOWLEDGE,
            difficulty_level: DifficultyLevel = DifficultyLevel.EASY
    ) -> dict:
        stem = MCQService.construct_stem(
            stem_construct_eval_crew_init,
            question_cache_service,
            subject_description,
            knowledge_context,
            blooms_taxonomy_level,
            difficulty_level
        )
        key = MCQService.construct_key(
            key_construct_eval_crew_init,
            stem['stem'],
            subject_description,
            knowledge_context,
            difficulty_level
        )
        distractors = MCQService.construct_distractors(
            distractor_construct_eval_crew_init,
            stem['stem'],
            key['key'],
            subject_description,
            knowledge_context,
            num_alternatives,
            difficulty_level
        )
        alternatives = [distractor for distractor in distractors['distractors']]
        alternatives.append(key['key'])
        formatted_alternatives = MCQService.format_options(
            alternatives_format_eval_crew_init,
            subject_description,
            stem['stem'],
            alternatives,
            key['key'],
            num_alternatives
        )
        result = {
            'stem': stem['stem'],
            'alternatives': formatted_alternatives['alternatives'],
            'key': formatted_alternatives['key']
        }
        if result['key'] in result['alternatives']:
            return result
        result['key'] = key['key']
        return result

    @staticmethod
    def backup():
        pass
