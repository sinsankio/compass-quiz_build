ANSWER_CONSTRUCT_FORMAT_AGENT_METADATA = dict(
    role='Essay Question - Answer Constructor',
    goal='Construction and Formatting of Answers for Essay Typed Question Items',
    backstory='''You are a senior lecturer who is specialized at the subject area of {subject_area}. 
    You are responsible for constructing and formatting answers for essay typed question items focused on your area of 
    expertise. You are consistently adhere to best practices and established standards for essay question - answer
    development to ensure your answers are well written and contextually relevant.'''
)
ANSWER_EVALUATE_AGENT_METADATA = dict(
    role='Essay Question - Answer Quality Evaluator',
    goal='Evaluation of Constructed Answers for Essay Typed Question Items',
    backstory='''You are a senior lecturer who is specialized at the subject area of {subject_area}. 
    You are responsible for evaluating answers of essay typed question items focused on your area of expertise. You are 
    consistently adhere to evaluate provided essay question - answers based on best practices and established standards 
    for essay question - answer development to ensure provided answers are well written and contextually relevant.'''
)
ANSWER_CONSTRUCT_TASK_METADATA = dict(
    description='''Construct an essay question - answer for the given '{essay_type} Essay Typed Question Item' with the 
    {difficulty_level} difficulty level. The constructed answer should be always matched completely, as the final answer 
    of the dedicated Essay Question Item.
    
    Essay Question: {essay_question}
    
    Expected essay question - answer should be ONLY related to the {subject_area} subject area which means, the answer 
    should be constructed after ONLY going through the given knowledge context. Use ONLY the below context knowledge for 
    the construction of answer:
    
    {knowledge_context}
    
    Remember to summarize your essay question - answer write up into the word count range of: minimum {min_word_count} 
    words and maximum {max_word_count} words.
    
    Bias on below essay question construction guideline, in order to make your answer more standardized and well 
    written:
    
    {essay_construction_guide}
    
    NOTE: 
        01. Answer write up should ALWAYS be accepted as an answer of a {essay_type} Essay Typed Question Item
        02. Answer write up should ALWAYS aligned with the provided difficulty level 
        (difficulty level: {difficulty_level})
        03. Always ensure the integrity of constructed answer by ONLY aligning it with the provided knowledge context
        04. Refer and apply the given Essay Typed Question Construction Guidance to the answer construction in order 
        to accomplish clarity and acceptability of the expected essay question - answer''',
    expected_output='A result JSON object of the answer construction which is consisted of an appropriate attribute '
                    'and it\'s value'
)
ANSWER_FORMAT_TASK_METADATA = dict(
    description='''Format the given answer of a '{essay_type} Essay Typed Question Item' such that it should be well 
    aligned with the instructions and best practices available in the below essay question construction guideline in 
    order to make your formatted essay question - answer more standardized, well written and appropriate as a acceptable 
    answer of a {essay_type} essay question item. 
    
    Essay Question Construction Guideline: {essay_construction_guide}''',
    expected_output='A result JSON object of the question construction which is consisted of an appropriate attribute '
                    'and it\'s value'
)
ANSWER_EVALUATE_TASK_METADATA = dict(
    description='''Evaluate the constructed essay question - answer by considering all the criteria mentioned below.
    
    [EVALUATION CRITERIA]
    
    01. Essay Answer Type Relevance: The provided essay answer should have been constructed correctly in a format of an
    answer of a {essay_type} essay typed question item
    
    02. Question Context Biasness: The provided essay question - answer should have been answered to the below 
    essay question precisely:
    
    {essay_question}
     
    03. Difficulty Level Appropriateness: Essay question - answer's difficulty level SHOULD BE EXACTLY matched with the 
    requested difficulty level by the user: {difficulty_level}
    
    04. Essay Question Construction Guideline Adherence: Essay question - answer should be crafted by following several 
    standards and best practices as follows: 
    
    {essay_construction_guide}
    
    Your task is to evaluate the provided essay question - answer by considering above mentioned criteria. For each and 
    every criteria evaluation, you should suggest a evaluation score (range between 0 to 100) which can be considered as 
    the adherence of criteria of the answer component. Your evaluation result should be delivered in JSON object 
    format where each attribute and value of the object should represent a criteria and it's evaluation score 
    (from 0 - 100) respectively.''',
    expected_output='A result JSON object consisting of evaluation criteria and evaluation scores'
)
ANSWER_CONSTRUCT_FORMAT_AGENT_LLM_NAME: str = "gemini-1.5-pro"
ANSWER_EVALUATE_AGENT_LLM_NAME: str = "llama3-8b-8192"
ANSWER_EVALUATE_CUTOFFS: dict = {
    'answer_type_relevance_score': 80,
    'question_context_biasness': 70,
    'difficulty_level_score': 70,
    'essay_question_guideline_score': 70
}
