QUESTION_CONSTRUCT_FORMAT_AGENT_METADATA = dict(
    role='Essay Typed Question Constructor',
    goal='Construction and Formatting of Questions for Essay Typed Question Items',
    backstory='''You are a senior lecturer who is specialized at the subject area of {subject_area}. 
    You are responsible for constructing and formatting essay typed question items focused on your area of expertise. 
    You are consistently adhere to best practices and established standards for essay question development to ensure 
    your questions are well written and contextually relevant.'''
)
QUESTION_EVALUATE_AGENT_METADATA = dict(
    role='Essay Typed Question Quality Evaluator',
    goal='Evaluation of Constructed Questions for Essay Typed Question Items',
    backstory='''You are a senior lecturer who is specialized at the subject area of {subject_area}. 
    You are responsible for evaluating essay typed question items focused on your area of expertise. You are 
    consistently adhere to evaluate provided question items based on best practices and established standards for 
    essay question development to ensure provided questions are well written and contextually relevant.'''
)
QUESTION_CONSTRUCT_TASK_METADATA = dict(
    description='''Construct a question for a '{essay_type} Essay Typed Question Item' with the {difficulty_level} 
    difficulty level. Expected question should be ONLY related to the {subject_area} subject area. Use ONLY the below 
    context knowledge for the construction of question:
    
    {knowledge_context}
    
    Target question should be constructed by aligning it on the {bt_level} level of Bloom's Taxonomy model. Here is a
    brief guide on both of the Bloom's Taxonomy model and dedicated Bloom's Taxonomy level:
    
    {bt_model_guide}
    
    {bt_level_guide}
        
    Here are some of the examples for already created essay typed question items related to the requested 
    Bloom's Taxonomy level:
    
    {bt_level_examples}
    
    Always ensure that the created question should be non - existed within the already created essay question items 
    mentioned below.
    
    Already created essay question items: {pool_essay_questions}
    
    Bias on below essay question construction guideline in order to make your question more standardized and well 
    written:
    
    {essay_construction_guide}
    
    NOTE: 
        01. Question should ALWAYS be accepted as a {essay_type} Essay Typed Question Item
        02. Question should ALWAYS aligned with the provided difficulty level (difficulty level: {difficulty_level})
        03. Always ensure the integrity of constructed question item by ONLY aligning it with the provided knowledge 
        context
        03. Created question should be unique and distinguished such that, it SHOULD NOT be similar to any of the 
        already created essay typed question items
        04. Refer and apply the given Bloom's Taxonomy supervision (guide and examples) to the question construction 
        in order to accomplish learning outcome of the expected question
        05. Refer and apply the given Essay Typed Question Construction Guidance to the question construction in order 
        to accomplish clarity and acceptability of the expected question''',
    expected_output="A result JSON object of the question construction which is consisted of an appropriate attribute "
                    "and it's value"
)
QUESTION_FORMAT_TASK_METADATA = dict(
    description='''Format the given question of a '{essay_type} Essay Typed Question Item' such that it should be well 
    aligned with the instructions and best practices available in the below essay question construction guideline in 
    order to make your formatted question more standardized, well written and appropriate as a acceptable question of 
    an essay question item. 
    
    Essay Question Construction Guideline: {essay_construction_guide}''',
    expected_output='A result JSON object of the question construction which is consisted of an appropriate attribute '
                    'and it\'s value'
)
QUESTION_EVALUATE_TASK_METADATA = dict(
    description='''Evaluate the constructed question by considering all the criteria mentioned below.
    
    [EVALUATION CRITERIA]
    
    01. Essay Question Type Relevance: The provided question should have been constructed correctly in a format of a
    {essay_type} essay typed question item
    
    02. Knowledge Context Biasness: The provided question should have been constructed and could be answered by ONLY 
    referring to the below knowledge context:
    
    {knowledge_context}
     
    03. Difficulty Level Appropriateness: Question's difficulty level SHOULD BE EXACTLY matched with the requested 
    difficulty level by the user: {difficulty_level}
    
    04. Non Existence within Already Created Question Items: Created question should be unique and distinguished such 
    that, it should NOT be similar to any of the already created essay question items
    
    05. Bloom's Taxonomy Level Appropriateness: Any question should be well aligned with a user specified Bloom's 
    Taxonomy Level. The question should adhere with all the instructions and outcomes of the dedicated Bloom's Taxonomy 
    Level in order to archive expected learning effectivity. Here is the expected Bloom's Taxonomy Level guidance for 
    the provided essay question: 
    
    {bt_level_guide}
    
    06. Essay Question Construction Guideline Adherence: Essay question items should be crafted by following several 
    standards and best practices as follows: 
    
    {essay_construction_guide}
    
    Your task is to evaluate the provided essay question by considering above mentioned criteria. For each and every
    criteria evaluation, you should suggest a evaluation score (range between 0 to 100) which can be considered as 
    the adherence of criteria of the question component. Your evaluation result should be delivered in JSON object 
    format where each attribute and value of the object should represent a criteria and it's evaluation score 
    (from 0 - 100) respectively.''',
    expected_output='A result JSON object consisting of evaluation criteria and evaluation scores'
)
QUESTION_CONSTRUCT_FORMAT_AGENT_LLM_NAME: str = "gemini-1.5-pro"
QUESTION_EVALUATE_AGENT_LLM_NAME: str = "llama3-8b-8192"
QUESTION_EVALUATE_CUTOFFS: dict = {
    'question_type_relevance_score': 70,
    'knowledge_context_score': 70,
    'difficulty_level_score': 70,
    'non_existence_level_score': 80,
    'bt_level_score': 70,
    'essay_question_guideline_score': 70
}
