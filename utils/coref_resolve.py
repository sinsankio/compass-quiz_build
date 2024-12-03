from configs.coref_resolve import COREF_RESOLVE_ENDPOINT
from utils.api import perform_request, HttpMethod


def coref_resolve(text: str, conv_dict: dict) -> str | None:
    data = {
        'text': text,
        'convDict': conv_dict
    }
    if resolved := perform_request(HttpMethod.POST, COREF_RESOLVE_ENDPOINT, data):
        return resolved['text']
