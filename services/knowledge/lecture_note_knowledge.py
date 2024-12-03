import os

from fastapi.encoders import jsonable_encoder
from langchain_community.vectorstores import FAISS

from api.models import Topic
from services.file_upload import FileUploadService
from services.knowledge.template import KnowledgeService
from utils.coref_resolve import coref_resolve
from utils.db.mongo_nosql import MongoNoSQL
from utils.doc_extract import load_pages
from utils.extractive_summarize import extractive_summarize
from utils.lecture_note_knowledge import (
    process_docs,
    generate_knowledge_vector_db,
    extract_topic_knowledge,
    load_embedding_model
)
from utils.ner import get_named_entity_conventions
from utils.topic_model import (
    preprocess_data,
    generate_id2word_mapping,
    generate_corpus,
    train_lda_model,
    eval_lda_model_on_coherence_score,
    generate_topics,
    generate_meaningful_topic
)


class LectureNoteKnowledgeService(KnowledgeService):
    MONGO_COLLECTION_NAME: str = "quiz-knowledge-bases"
    VECTOR_DB_FILE_SAVE_PATH: str = "api/vector_dbs/"

    @staticmethod
    def extract_lecture_note_pages(knowledge_id: str) -> list:
        knowledge_dir = os.path.join(FileUploadService.FILE_UPLOAD_SAVE_ROOT_PATH, f'{knowledge_id}')
        lecture_note_files = os.listdir(knowledge_dir)
        lecture_note_pages = []
        for f_name in lecture_note_files:
            lecture_note_pages.extend(load_pages(os.path.join(knowledge_dir, f_name)))
        return lecture_note_pages

    @staticmethod
    def extract_knowledge(knowledge: dict) -> list:
        lecture_note_pages = LectureNoteKnowledgeService.extract_lecture_note_pages(knowledge['_id'])
        for i in range(len(lecture_note_pages)):
            lecture_note_pages[i] = lecture_note_pages[i].page_content
        return lecture_note_pages

    @staticmethod
    def get_named_entity_conventions(lecture_note_contents: list) -> list:
        conventions = []
        for content in lecture_note_contents:
            conventions.append(get_named_entity_conventions(content))
        return conventions

    @staticmethod
    def coref_resolve(lecture_note_contents: list, named_entity_conventions: list) -> list | None:
        coref_resolved = []
        for i in range(len(lecture_note_contents)):
            coref_resolved.append(coref_resolve(lecture_note_contents[i], named_entity_conventions[i]))
        return coref_resolved

    @staticmethod
    def preprocess_knowledge(lecture_note_page_contents: list) -> list | None:
        named_entity_conventions = LectureNoteKnowledgeService.get_named_entity_conventions(lecture_note_page_contents)
        if coref_resolved := LectureNoteKnowledgeService.coref_resolve(
                lecture_note_page_contents,
                named_entity_conventions
        ):
            return preprocess_data(coref_resolved)

    @staticmethod
    def generate_meaningful_topics(generated_topics: list, subject_description: str) -> list:
        meaningful_topics = []
        for topic in generated_topics:
            meaningful_topics.append(generate_meaningful_topic(topic, subject_description)['topic'])
        return meaningful_topics

    @staticmethod
    def model_topics(preprocessed_knowledge: list, num_topics: int, subject_description: str) -> dict:
        id2word = generate_id2word_mapping(preprocessed_knowledge)
        corpus = generate_corpus(preprocessed_knowledge, id2word)
        lda = train_lda_model(
            corpus=corpus,
            num_topics=num_topics,
            id2word=id2word
        )
        coherence_score = eval_lda_model_on_coherence_score(
            lda_model=lda,
            processed_texts=preprocessed_knowledge,
            id2word=id2word
        )
        generated_topics = generate_topics(lda)
        return {
            'topics': LectureNoteKnowledgeService.generate_meaningful_topics(generated_topics, subject_description),
            'coherence_score': coherence_score
        }

    # RAG Search and Summarization

    @staticmethod
    def map_topic_knowledge(knowledge: dict) -> None:
        lecture_note_pages = LectureNoteKnowledgeService.extract_lecture_note_pages(knowledge['_id'])
        processed_docs = process_docs(lecture_note_pages)
        vector_db = generate_knowledge_vector_db(processed_docs)
        vector_db.save_local(f'{os.path.join(LectureNoteKnowledgeService.VECTOR_DB_FILE_SAVE_PATH, knowledge['_id'])}')

    @staticmethod
    def extract_topic_knowledge(knowledge: dict, topic: str) -> str:
        knowledge_vector_db = FAISS.load_local(
            f'{os.path.join(LectureNoteKnowledgeService.VECTOR_DB_FILE_SAVE_PATH, knowledge['_id'])}',
            load_embedding_model(),
            allow_dangerous_deserialization=True
        )
        topic_knowledge = extract_topic_knowledge(knowledge_vector_db, topic)
        return ''.join(content for content in topic_knowledge)

    # Pipelines

    @staticmethod
    def model_topics_in_pipeline(knowledge: dict, num_topics: int, subject_description: str) -> dict:
        knowledge_content = LectureNoteKnowledgeService.extract_knowledge(knowledge)
        preprocessed_knowledge = LectureNoteKnowledgeService.preprocess_knowledge(knowledge_content)
        return LectureNoteKnowledgeService.model_topics(
            preprocessed_knowledge,
            num_topics,
            subject_description
        )

    @staticmethod
    def extractive_summarize_in_pipeline(knowledge: dict, topic_description: str) -> str:
        extracted_topic_knowledge = LectureNoteKnowledgeService.extract_topic_knowledge(knowledge, topic_description)
        return extractive_summarize(topic_description, extracted_topic_knowledge)

    @staticmethod
    def create_knowledge_base(
            db_client: MongoNoSQL,
            knowledge: dict,
            user: dict,
            num_topics: int | None = None
    ) -> dict | None:
        if not os.path.exists(os.path.join(FileUploadService.FILE_UPLOAD_SAVE_ROOT_PATH, knowledge['_id'])):
            return
        if knowledge := LectureNoteKnowledgeService.generate_knowledge_base(knowledge, num_topics):
            if inserted_id := db_client.insert(LectureNoteKnowledgeService.MONGO_COLLECTION_NAME, knowledge):
                if knowledge := db_client.search(
                        LectureNoteKnowledgeService.MONGO_COLLECTION_NAME, {'_id': inserted_id}
                ):
                    user['knowledgeBases'].append(knowledge)
                    return knowledge

    @staticmethod
    def generate_knowledge_base(knowledge: dict, num_topics: int | None = None) -> dict | None:
        if not knowledge:
            return
        if not knowledge['topics']:
            topic_modeling_result = LectureNoteKnowledgeService.model_topics_in_pipeline(
                knowledge,
                num_topics,
                knowledge['subjectDescription']
            )
            knowledge['topics'] = []
            for topic_name in topic_modeling_result['topics']:
                topic = Topic(description=topic_name)
                knowledge['topics'].append(jsonable_encoder(topic))
                knowledge['topicModelingCoherenceScore'] = topic_modeling_result['coherence_score']
        LectureNoteKnowledgeService.map_topic_knowledge(knowledge)
        for topic in knowledge['topics']:
            topic['summarizedContent'] = LectureNoteKnowledgeService.extractive_summarize_in_pipeline(
                knowledge,
                topic['description']
            )
        return knowledge

    @staticmethod
    def get_knowledge_base(db_client: MongoNoSQL, knowledge_id: str) -> dict | None:
        if knowledge := db_client.search(
                LectureNoteKnowledgeService.MONGO_COLLECTION_NAME,
                {'_id': knowledge_id}
        ):
            return knowledge

    @staticmethod
    def get_user_knowledge_base(user: dict, knowledge_id: str) -> dict | None:
        for knowledge_base in user['knowledgeBases']:
            if knowledge_base['_id'] == knowledge_id:
                return knowledge_base

    @staticmethod
    def get_user_knowledge_base_pos(user: dict, knowledge_id: str) -> int | None:
        for i in range(len(user['knowledgeBases'])):
            if user['knowledgeBases'][i]['_id'] == knowledge_id:
                return i + 1    

    @staticmethod
    def get_quiz_plan_knowledge_base_topic(knowledge_base: dict, topic_id: str) -> dict | None:
        for topic in knowledge_base['topics']:
            if topic['_id'] == topic_id:
                return topic

    @staticmethod
    def update_knowledge_base(
            db_client: MongoNoSQL,
            knowledge: dict,
            user: dict,
            num_topics: int | None = None
    ) -> dict | None:
        if not os.path.exists(os.path.join(FileUploadService.FILE_UPLOAD_SAVE_ROOT_PATH, knowledge['_id'])):
            return
        if pos := LectureNoteKnowledgeService.get_user_knowledge_base_pos(user, knowledge['_id']):
            if knowledge := LectureNoteKnowledgeService.generate_knowledge_base(knowledge, num_topics):
                if db_client.update(
                        LectureNoteKnowledgeService.MONGO_COLLECTION_NAME,
                        {'_id': knowledge['_id']},
                        knowledge
                ).modified_count >= 1:
                    if updated_knowledge := LectureNoteKnowledgeService.get_knowledge_base(db_client, knowledge['_id']):
                        user['knowledgeBases'][pos - 1] = updated_knowledge
                        return updated_knowledge

    @staticmethod
    def delete_knowledge_base(db_client: MongoNoSQL, knowledge_id: str, user: dict) -> int | None:
        if pos := LectureNoteKnowledgeService.get_user_knowledge_base_pos(user, knowledge_id):
            if deleted_count := db_client.delete(
                    LectureNoteKnowledgeService.MONGO_COLLECTION_NAME,
                    {'_id': knowledge_id}
            ).deleted_count:
                user['knowledgeBases'].pop(pos - 1)
                FileUploadService.delete_existing_files(
                    os.path.join(FileUploadService.FILE_UPLOAD_SAVE_ROOT_PATH, knowledge_id)
                )
                return deleted_count
