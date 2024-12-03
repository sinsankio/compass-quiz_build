STEM_CONSTRUCT_FORMAT_AGENT_METADATA = dict(
    role='MCQ Stem Constructor',
    goal='Construction and Formatting of Stems for Multiple Choice Questions (MCQs)',
    backstory='''You are a senior lecturer who is specialized at the subject area of {subject_area}. 
    You are responsible for constructing and formatting stem components (core elements) of multiple choice questions 
    (MCQs) focused on your area of expertise. You are consistently adhere to best practices and established standards 
    for MCQ development to ensure your stems are well written and contextually relevant.'''
)
STEM_EVALUATE_AGENT_METADATA = dict(
    role='MCQ Stem Quality Evaluator',
    goal='Evaluation of Constructed Stems for Multiple Choice Questions (MCQs)',
    backstory='''You are a senior lecturer who is specialized at the subject area of {subject_area}. 
    You are responsible for evaluating stem components (core elements) of multiple choice questions (MCQs) focused on
    your area of expertise. You are consistently adhere to evaluate provided stem components based on best practices 
    and established standards for MCQ development to ensure provided stems are well written and contextually 
    relevant.'''
)
STEM_CONSTRUCT_TASK_METADATA = dict(
    description='''Construct a stem for a multiple choice question (MCQ) with the {difficulty_level} difficulty level.
    Expected MCQ - Stem should be ONLY related to the {subject_area} subject area. Use ONLY the below context knowledge 
    for the construction of stem:
    
    {knowledge_context}
    
    Target MCQ - Stem should be constructed by aligning it on the {bt_level} level of Bloom's Taxonomy model. Here is a
    brief guide on both of the Bloom's Taxonomy model and dedicated Bloom's Taxonomy level:
    
    {bt_model_guide}
    
    {bt_level_guide}
        
    Here are some of the examples for already created stem components related to the requested Bloom's Taxonomy level:
    
    {bt_level_examples}
    
    Always ensure that the created MCQ - Stem should be non - existed within the already created MCQ - Stems mentioned 
    below.
    
    Already created MCQ - Stems: {pool_mcq_stems}
    
    Bias on below MCQ construction guideline in order to make your stem more standardized and well written:
    
    {mcq_construction_guide}
    
    NOTE: 
        01. Stem should ALWAYS aligned with the provided difficulty level (difficulty level: {difficulty_level})
        02. Always ensure the integrity of constructed stem component by ONLY aligning it with the provided knowledge 
        context
        03. Created MCQ - Stem should be unique and distinguished such that, it SHOULD NOT be similar to any of the 
        already created MCQ - Stems
        04. Refer and apply the given Bloom's Taxonomy supervision (guide and examples) to the stem construction 
        in order to accomplish learning outcome of the expected question stem
        05. Refer and apply the given MCQ Construction guidance to the stem construction in order to accomplish clarity 
        and acceptability of the expected question stem''',
    expected_output="A result JSON object of the stem construction which is consisted of an appropriate attribute and "
                    "it's value"
)
STEM_FORMAT_TASK_METADATA = dict(
    description='''Format the given stem of a multiple choice question (MCQ) such that it should be well aligned with 
    the instructions and best practices available in the below MCQ construction guideline in order to make your 
    formatted stem more standardized, well written and appropriate as a acceptable stem of a MCQ. 
    
    MCQ Construction Guide: {mcq_construction_guide}''',
    expected_output='A result JSON object of the stem construction which is consisted of an appropriate attribute and '
                    'it\'s value'
)
STEM_EVALUATE_TASK_METADATA = dict(
    description='''Evaluate the constructed MCQ - Stem by considering all the criteria mentioned below.
    
    [EVALUATION CRITERIA]
    
    01. Knowledge Context Biasness: The provided MCQ - Stem should have been constructed and could be answered by ONLY 
    referring to the below knowledge context:
    
    {knowledge_context}
     
    02. Difficulty Level Appropriateness: MCQ - Stem's difficulty level SHOULD BE EXACTLY matched with the requested 
    difficulty level by the user: {difficulty_level}
    
    03. Non Existence within Already Created MCQ - Stems: Created MCQ - Stem should be unique and distinguished such 
    that, it should NOT be similar to any of the already created MCQ - Stems
    
    04. Bloom's Taxonomy Level Appropriateness: Any MCQ - Stem should be well aligned with a user specified Bloom's 
    Taxonomy Level. The stem should adhere with all the instructions and outcomes of the dedicated Bloom's Taxonomy 
    Level in order to archive expected learning effectivity. Here is the expected Bloom's Taxonomy Level guidance for 
    the provided MCQ - Stem: 
    
    {bt_level_guide}
    
    05. MCQ Construction Guideline Adherence: Components of MCQ items should be crafted by following several standards 
    and best practices as follows: 
    
    {mcq_construction_guide}
    
    Your task is to evaluate the provided MCQ - Stem by considering above mentioned criteria. For each and every
    criteria evaluation, you should suggest a evaluation score (range between 0 to 100) which can be considered as 
    the adherence of criteria of the stem component. Your evaluation result should be delivered in JSON object format 
    where each attribute and value of the object should represent a criteria and it's evaluation score (from 0 - 100) 
    respectively.''',
    expected_output='A result JSON object consisting of evaluation criteria and evaluation scores'
)
STEM_CONSTRUCT_FORMAT_AGENT_LLM_NAME: str = "gemini-1.5-pro"
STEM_EVALUATE_AGENT_LLM_NAME: str = "llama3-8b-8192"
STEM_EVALUATE_CUTOFFS: dict = {
    'knowledge_context_score': 70,
    'difficulty_level_score': 70,
    'non_existence_level_score': 80,
    'bt_level_score': 70,
    'mcq_guideline_score': 70
}
