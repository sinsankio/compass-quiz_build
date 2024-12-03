from typing import Any

from flair.data import Sentence
from flair.nn import Classifier

from configs.ner import *

TAGGER: Classifier | None = None


def load_tagger(model_name: str = FLAIR_NER_MODEL_NAME) -> Any:
    global TAGGER

    if not TAGGER:
        TAGGER = Classifier.load(model_name)
    return TAGGER


def predict_labels(text_content: str) -> list:
    load_tagger()
    sentence = Sentence(text_content)
    TAGGER.predict(sentence)
    return sentence.get_labels()


def get_named_entity_conventions(text_content: str) -> dict:
    labels = predict_labels(text_content)
    named_entity_conventions = {}
    for label in labels:
        label_name = label.unlabeled_identifier.replace('"', '').replace("'", "").strip().split(': ')[1]
        entity = label.value
        if entity in NER_TAG_MEANINGS and label_name not in named_entity_conventions:
            named_entity_conventions[label_name] = NER_TAG_MEANINGS[entity]
    return named_entity_conventions
