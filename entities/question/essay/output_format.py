from pydantic import BaseModel, Field


class EssayQuestionConstructFormatOutput(BaseModel):
    question: str = Field(description='The constructed/formatted question of the Essay Question Item')


class EssayQuestionEvaluateOutput(BaseModel):
    question_type_relevance_score: int = Field(
        description='Evaluation score for Question Type Relevance (0 to 100)',
        le=100,
        ge=0
    )
    knowledge_context_score: int = Field(
        description='Evaluation score for Knowledge Context Biasness (0 to 100)',
        le=100,
        ge=0
    )
    difficulty_level_score: int = Field(
        description='Evaluation score for Difficulty Level Appropriateness (0 to 100)',
        le=100,
        ge=0
    )
    non_existence_level_score: int = Field(
        description='Evaluation score for Non Existence within Already Created Essay Question Items (0 to 100)',
        le=100,
        ge=0
    )
    bt_level_score: int = Field(
        description='Evaluation score for Bloom\'s Taxonomy Level Appropriateness (0 to 100)',
        le=100,
        ge=0
    )
    essay_question_guideline_score: int = Field(
        description='Evaluation score for Essay Question Construction Guideline Adherence (0 to 100)',
        le=100,
        ge=0
    )


class EssayAnswerConstructFormatOutput(BaseModel):
    answer: str = Field(description='The constructed/formatted answer of the Essay Question Item')


class EssayAnswerEvaluateOutput(BaseModel):
    answer_type_relevance_score: int = Field(
        description='Evaluation score for Essay Answer Type Relevance (0 to 100)',
        le=100,
        ge=0
    )
    question_context_biasness: int = Field(
        description='Evaluation score for Question Context Biasness (0 to 100)',
        le=100,
        ge=0
    )
    difficulty_level_score: int = Field(
        description='Evaluation score for Difficulty Level Appropriateness (0 to 100)',
        le=100,
        ge=0
    )
    essay_question_guideline_score: int = Field(
        description='Evaluation score for Essay Question Construction Guideline Adherence (0 to 100)',
        le=100,
        ge=0
    )
