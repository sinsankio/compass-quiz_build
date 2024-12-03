from pydantic import BaseModel, Field


class StemConstructFormatOutput(BaseModel):
    stem: str = Field(description='The constructed/formatted stem of the MCQ')


class StemEvaluateOutput(BaseModel):
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
        description='Evaluation score for Non Existence within Already Created MCQ - Stems (0 to 100)',
        le=100,
        ge=0
    )
    bt_level_score: int = Field(
        description='Evaluation score for Bloom\'s Taxonomy Level Appropriateness (0 to 100)',
        le=100,
        ge=0
    )
    mcq_guideline_score: int = Field(
        description='Evaluation score for MCQ Construction Guideline Adherence (0 to 100)',
        le=100,
        ge=0
    )


class KeyConstructOutput(BaseModel):
    key: str = Field(description='The constructed key of the MCQ')


class KeyEvaluateOutput(BaseModel):
    knowledge_context_score: int = Field(
        description='Evaluation score for Knowledge Context Biasness (0 to 100)',
        le=100,
        ge=0
    )
    stem_context_score: int = Field(
        description='Evaluation score for Stem Context Biasness (0 to 100)',
        le=100,
        ge=0
    )
    difficulty_level_score: int = Field(
        description='Evaluation score for Difficulty Level Appropriateness (0 to 100)',
        le=100,
        ge=0
    )
    mcq_guideline_score: int = Field(
        description='Evaluation score for MCQ Construction Guideline Adherence (0 to 100)',
        le=100,
        ge=0
    )


class DistractorConstructOutput(BaseModel):
    distractors: list[str] = Field(description='List of constructed distractor options for a given MCQ')


class DistractorEvaluateOutput(BaseModel):
    requested_distractor_count_score: int = Field(
        description='Evaluation score for Construction of Requested Distractor Count (0 to 100)',
        le=100,
        ge=0
    )
    knowledge_context_score: int = Field(
        description='Evaluation score for Knowledge Context Biasness (0 to 100)',
        le=100,
        ge=0
    )
    key_similarity_score: int = Field(
        description='Evaluation score for Similarity with the Key (0 to 100)',
        le=100,
        ge=0
    )
    difficulty_level_score: int = Field(
        description='Evaluation score for Difficulty Level Appropriateness (0 to 100)',
        le=100,
        ge=0
    )
    distraction_level_score: int = Field(
        description='Evaluation score for Distraction to the Key (0 to 100)',
        le=100,
        ge=0
    )
    mcq_guideline_score: int = Field(
        description='Evaluation score for MCQ Construction Guideline Adherence (0 to 100)',
        le=100,
        ge=0
    )


class AlternativeOptionFormatOutput(BaseModel):
    alternatives: list[str] = Field(description='List of formatted alternative options for a given MCQ')
    key: str = Field(description='Formatted MCQ - Key alternative (correct answer) among all the formatted alternative '
                                 'options for a given MCQ. NOTE: Replace the exact correct answer content')


class AlternativeOptionEvaluateOutput(BaseModel):
    requested_distractor_count_score: int = Field(
        description='Evaluation score for Construction of Requested Alternative Count (0 to 100)',
        le=100,
        ge=0
    )
    plausible_and_attractive_score: int = Field(
        description='Evaluation score for Formatted with Plausibly and Attractively (0 to 100)',
        le=100,
        ge=0
    )
    mutual_exclusive_score: int = Field(
        description='Evaluation score for Mutual Exclusiveness (0 to 100)',
        le=100,
        ge=0
    )
    length_equality_score: int = Field(
        description='Evaluation score for Length Equality (0 to 100)',
        le=100,
        ge=0
    )
    mcq_guideline_score: int = Field(
        description='Evaluation score for MCQ Construction Guideline Adherence (0 to 100)',
        le=100,
        ge=0
    )
