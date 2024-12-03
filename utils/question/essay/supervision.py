import os

from entities.blooms_taxonomy_level import EssayBloomsTaxonomyLevel
from entities.question.essay.question_type import EssayQuestionType


def load_bt_supervision(
        essay_type: EssayQuestionType,
        bt_level: EssayBloomsTaxonomyLevel,
        guide_dir_path: str = 'prompts/blooms_taxonomy_guide/',
        example_dir_path: str = 'prompts/question/essay/'
) -> dict:
    if essay_type == EssayQuestionType.RESTRICTED_RESPONSE:
        example_dir_path = os.path.join(example_dir_path, 'blooms_taxonomy_restricted_response_question_examples')
    else:
        example_dir_path = os.path.join(example_dir_path, 'blooms_taxonomy_extended_response_question_examples')
    bt_supervision = dict(model_guide='', level_guide='', examples='')
    with open(os.path.join(guide_dir_path, 'what-is-bt-guide.txt'), encoding='utf8') as bt_model_guide_file:
        bt_supervision['model_guide'] = bt_model_guide_file.read()
    with (open(os.path.join(guide_dir_path, f'{bt_level.value}-level-guide.txt'), encoding='utf8') as
          bt_level_guide_file):
        bt_supervision['level_guide'] = bt_level_guide_file.read()
    with (open(os.path.join(example_dir_path, f'{bt_level.value}-level-question-examples.txt'), encoding='utf8') as
          bt_level_example_file):
        bt_supervision['examples'] = bt_level_example_file.read()
    return bt_supervision


def load_essay_question_construction_supervision(
        file_path: str = 'prompts/question/essay/essay-construct-guideline.txt'
) -> str:
    with open(file_path, encoding='utf8') as essay_question_construct_guide_file:
        return essay_question_construct_guide_file.read()
