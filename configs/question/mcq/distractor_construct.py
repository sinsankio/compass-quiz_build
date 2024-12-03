DISTRACTOR_CONSTRUCT_AGENT_METADATA = dict(
    role='MCQ Distractor Constructor',
    goal='Construction of Distractors for Multiple Choice Questions (MCQs)',
    backstory='''You are a senior lecturer who is specialized at the subject area of {subject_area}. 
    You are responsible for constructing distractor components (incorrect answers) of multiple choice questions (MCQs) 
    focused on your area of expertise. You are consistently adhere to best practices and established standards for MCQ 
    development to ensure your distractors are well written and contextually relevant.'''
)
DISTRACTOR_EVALUATE_AGENT_METADATA = dict(
    role='MCQ Distractor Quality Evaluator',
    goal='Evaluation of Constructed Distractors for Multiple Choice Questions (MCQs)',
    backstory='''You are a senior lecturer who is specialized at the subject area of {subject_area}. 
    You are responsible for evaluating distractor components (incorrect answers) of multiple choice questions (MCQs) 
    focused on your area of expertise. You are consistently adhere to evaluate provided distractor components based on 
    best practices and established standards for MCQ development to ensure provided distractors are well written and 
    contextually relevant.'''
)
DISTRACTOR_CONSTRUCT_TASK_METADATA = dict(
    description='''Construct {num_distractors} distractor(s) (not including the stem) for the given stem and the key of 
    a multiple choice question (MCQ) with the {difficulty_level} difficulty level. The constructed distractor(s) should 
    be always completely acceptable, as the best fitting incorrect answer(s) of the dedicated MCQ - Stem by referring 
    ALL OF THE difficulty level, MCQ - Stem and MCQ - Key respectively.
    
    MCQ - Stem: {stem}
    MCQ - Key: {key}
    
    Expected MCQ - Distractor(s) should be ONLY related to the {subject_area} subject area which means, that a given 
    distractor should ALWAYS be inherited ONLY from the given knowledge context. Use ONLY the below context knowledge 
    for the construction of distractor(s):
    
    {knowledge_context}
    
    Bias on below MCQ construction guideline, in order to make your distractor(s) more standardized and well written:
    
    {mcq_construction_guide}
    
    NOTE: 
        01. The number of constructed distractor(s) should be ALWAYS equal to the number of requested distractor(s) by 
        the user: {num_distractors}
        02. A given distractor should ALWAYS aligned with the provided difficulty level (difficulty level: 
        {difficulty_level})
        03. Always ensure the integrity of constructed distractor component(s) by ONLY aligning it with the provided 
        knowledge context, difficulty level, MCQ - Stem and MCQ - Key
        04. Distractor(s) should be always sentimentally look similar to the provided MCQ - Key, but should be always 
        technically incorrect as the answer to the provided MCQ - Stem
        05. Constructed MCQ - Distractor(s) should be identical to each other and should distract to the guessing of 
        MCQ - Key (correct answer) of MCQ - Stem of the dedicated MCQ item
        06. Refer and apply the given MCQ Construction guidance to the distractor construction in order to accomplish 
        clarity and acceptability of the expected set of distractor(s)''',
    expected_output='A result JSON object of the distractor construction which is consisted of appropriate attributes '
                    'and values'
)
DISTRACTOR_EVALUATE_TASK_METADATA = dict(
    description='''Evaluate the constructed MCQ - Distractor(s) by considering all the criteria mentioned below.
    
    [EVALUATION CRITERIA]
    
    01. Construction of Requested Distractor Count: The number of constructed distractor(s) should be ALWAYS equal to 
    the number of requested distractor(s) by the user: {num_distractors}
    
    02. Knowledge Context Biasness: The provided MCQ - Distractor(s) should have been constructed by ONLY referring to 
    the below knowledge context:
    
    {knowledge_context}
    
    03. Similarity with the Key: Distractor(s) should be always sentimentally look similar to the provided MCQ - Key AND
    should be always technically incorrect as the answer to the provided MCQ - Stem
    
    04. Difficulty Level Appropriateness: MCQ - Distractor(s)' difficulty level SHOULD BE EXACTLY matched with the 
    requested difficulty level by the user: {difficulty_level}
    
    05. Distraction to the Key: The provided MCQ - Distractor(s) should be distracted for the guessing of 
    MCQ - Key (correct answer) of MCQ - Stem of the dedicated MCQ item:
    
    MCQ - Stem: {stem}
    MCQ - Key: {key}
    
    06. MCQ Construction Guideline Adherence: Components of MCQ items should be crafted by following several standards 
    and best practices as follows: 
    
    {mcq_construction_guide}
    
    Your task is to evaluate the provided MCQ - Distractor(s) by considering above mentioned criteria. For each and 
    every criteria evaluation, you should suggest a evaluation score (range between 0 to 100) which can be considered as 
    the adherence of criteria of the distractor(s) component(s). Your evaluation result should be delivered in JSON 
    object format where each attribute and value of the object should represent criteria and their evaluation scores 
    (from 0 - 100) respectively.''',
    expected_output='A result JSON object consisting of evaluation criteria and evaluation scores'
)
DISTRACTOR_CONSTRUCT_AGENT_LLM_NAME: str = "gemini-1.5-pro"
DISTRACTOR_EVALUATE_AGENT_LLM_NAME: str = "llama3-8b-8192"
DISTRACTOR_EVALUATE_CUTOFFS: dict = {
    'requested_distractor_count_score': 80,
    'knowledge_context_score': 70,
    'key_similarity_score': 80,
    'difficulty_level_score': 70,
    'distraction_level_score': 70,
    'mcq_guideline_score': 70
}
