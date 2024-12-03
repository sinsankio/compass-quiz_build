import os

from entities.blooms_taxonomy_level import McqBloomsTaxonomyLevel


def load_blooms_taxonomy_supervision(
        bt_level: McqBloomsTaxonomyLevel,
        guide_dir_path: str = 'prompts/blooms_taxonomy_guide/',
        example_dir_path: str = 'prompts/question/mcq/blooms_taxonomy_stem_examples/'
) -> dict:
    bt_supervision = dict(model_guide='', level_guide='', examples='')
    with open(os.path.join(guide_dir_path, 'what-is-bt-guide.txt'), encoding='utf8') as bt_model_guide_file:
        bt_supervision['model_guide'] = bt_model_guide_file.read()
    with (open(os.path.join(guide_dir_path, f'{bt_level.value}-level-guide.txt'), encoding='utf8') as
          bt_level_guide_file):
        bt_supervision['level_guide'] = bt_level_guide_file.read()
    with (open(os.path.join(example_dir_path, f'{bt_level.value}-level-stem-examples.txt'), encoding='utf8') as
          bt_level_example_file):
        bt_supervision['examples'] = bt_level_example_file.read()
    return bt_supervision


def load_mcq_construction_supervision(
        file_path: str = 'prompts/question/mcq/mcq-construct-guideline.txt'
) -> str:
    with open(file_path, encoding='utf8') as mcq_construct_guide_file:
        return mcq_construct_guide_file.read()
