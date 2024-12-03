KEY_CONSTRUCT_AGENT_METADATA = dict(
    role='MCQ Key Constructor',
    goal='Construction of Keys for Multiple Choice Questions (MCQs)',
    backstory='''You are a senior lecturer who is specialized at the subject area of {subject_area}. 
    You are responsible for constructing key components (correct answers) of multiple choice questions (MCQs) focused on
    your area of expertise. You are consistently adhere to best practices and established standards for MCQ development 
    to ensure your keys are well written and contextually relevant.'''
)
KEY_EVALUATE_AGENT_METADATA = dict(
    role='MCQ Key Quality Evaluator',
    goal='Evaluation of Constructed Keys for Multiple Choice Questions (MCQs)',
    backstory='''You are a senior lecturer who is specialized at the subject area of {subject_area}. 
    You are responsible for evaluating key components (correct answers) of multiple choice questions (MCQs) focused on
    your area of expertise. You are consistently adhere to evaluate provided key components based on best practices 
    and established standards for MCQ development to ensure provided keys are well written and contextually relevant.'''
)
KEY_CONSTRUCT_TASK_METADATA = dict(
    description='''Construct key for the given stem of a multiple choice question (MCQ) with the {difficulty_level} 
    difficulty level.  The constructed key should be always matched completely, as the final answer of the dedicated 
    MCQ - Stem.
    
    MCQ - Stem: {stem}
    
    Expected MCQ - Key should be ONLY related to the {subject_area} subject area which means, the key should be 
    guessed after ONLY going through the given knowledge context. Use ONLY the below context knowledge for the 
    construction of key:
    
    {knowledge_context}
    
    Bias on below MCQ construction guideline, in order to make your key more standardized and well written:
    
    {mcq_construction_guide}
    
    NOTE: 
        01. Key should ALWAYS aligned with the provided difficulty level (difficulty level: {difficulty_level})
        02. Always ensure the integrity of constructed key component by ONLY aligning it with the provided knowledge 
        context, difficulty level and MCQ - Stem
        03. Refer and apply the given MCQ Construction guidance to the key construction in order to accomplish clarity 
        and acceptability of the expected question key''',
    expected_output='A result JSON object of the key construction which is consisted of an appropriate attribute and '
                    'it\'s value'
)
KEY_EVALUATE_TASK_METADATA = dict(
    description='''Evaluate the constructed MCQ - Key by considering all the criteria mentioned below.
    
    [EVALUATION CRITERIA]
    
    01. Knowledge Context Biasness: The provided MCQ - Key should have been constructed by ONLY referring to the below 
    knowledge context:
    
    {knowledge_context}
    
    02. Stem Context Biasness: The provided MCQ - Key should have been answered to the below MCQ - Stem precisely:
    
    {stem}
    
    03. Difficulty Level Appropriateness: MCQ - Key's difficulty level SHOULD BE EXACTLY matched with the requested 
    difficulty level by the user: {difficulty_level}
    
    03. MCQ Construction Guideline Adherence: Components of MCQ items should be crafted by following several standards 
    and best practices as follows: 
    
    {mcq_construction_guide}
    
    Your task is to evaluate the provided MCQ - Key by considering above mentioned criteria. For each and every
    criteria evaluation, you should suggest a evaluation score (range between 0 to 100) which can be considered as 
    the adherence of criteria of the key component. Your evaluation result should be delivered in JSON object format 
    where each attribute and value of the object should represent a criteria and it's evaluation score (from 0 - 100) 
    respectively.''',
    expected_output='A result JSON object consisting of evaluation criteria and evaluation scores'
)
KEY_CONSTRUCT_AGENT_LLM_NAME: str = "gemini-1.5-pro"
KEY_EVALUATE_AGENT_LLM_NAME: str = "llama3-8b-8192"
KEY_EVALUATE_CUTOFFS: dict = {
    'knowledge_context_score': 70,
    'stem_context_score': 80,
    'difficulty_level_score': 70,
    'mcq_guideline_score': 70
}
