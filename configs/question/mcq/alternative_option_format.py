ALTERNATIVE_OPTION_FORMAT_AGENT_METADATA = dict(
    role='MCQ Alternative Formatter',
    goal='Formatting of Alternative Options of Multiple Choice Questions (MCQs)',
    backstory='''You are a senior lecturer who is specialized at the subject area of {subject_area}. 
    You are responsible for formatting alternative options (correct + incorrect answers) of multiple choice questions
    (MCQs) focused on your area of expertise. You are consistently adhere to best practices and established standards 
    for MCQ development to ensure your constructed alternative options are well written and contextually relevant.'''
)
ALTERNATIVE_OPTION_EVALUATE_AGENT_METADATA = dict(
    role='MCQ Alternative Quality Evaluator',
    goal='Evaluation of Formatted Alternative Options of Multiple Choice Questions (MCQs)',
    backstory='''You are a senior lecturer who is specialized at the subject area of {subject_area}.
    You are responsible for evaluating alternative options (correct + incorrect answers) of multiple choice questions
    (MCQs) focused on your area of expertise. You are consistently adhere to evaluate provided alternative options 
    based on best practices and established standards for MCQ development to ensure provided alternative options are 
    well written and contextually relevant.'''
)
ALTERNATIVE_OPTION_FORMAT_TASK_METADATA = dict(
    description='''Format ALL the given non formatted alternative option(s) of a multiple choice question (MCQ) such
    that it should be well formatted with the instructions and best practices available in the below MCQ construction 
    guideline in order to make your formatted option(s) more standardized, well written and appropriate as acceptable 
    option(s) of a MCQ. Here are the provided non-formatted alternative option(s), their subsequent MCQ - Stem and 
    the non - formatted MCQ - Key together with the recommended MCQ Construction Guide:
    
    MCQ - Stem: {stem}
    Non Formatted Alternatives: {non_formatted_options}
    MCQ - Key (non - formatted): {non_formatted_key}
    MCQ Construction Guide: {mcq_construction_guide}
    
    Follow below instructions explicitly to format the set of non formatted alternative options:
    
    01. The number of constructed alternative(s) should be ALWAYS equal to the number of requested alternative(s) by 
    the user: {num_alternatives}
        
    02. Make all alternative options plausible and attractive to a less knowledgeable or skillful student
    (NOTE: DON'T BE PLAUSIBLE AND ATTRACTIVE TO THE STUDENT TOO MUCH!)
    
    03. Make all the alternative options mutually exclusive to each other
    
    04. Make all the alternative options approximately equal in length and weight
    
    05. Refer and apply the given MCQ construction guidance to the option formatting in order to accomplish clarity and 
    acceptability of the expected formatted alternative option(s)''',
    expected_output='A result JSON object of the alternative option(s) construction which consisted of appropriate '
                    'attributes and values'
)
ALTERNATIVE_OPTION_EVALUATE_TASK_METADATA = dict(
    description='''Evaluate the formatted MCQ - Alternative(s) by considering all the criteria mentioned below.
    
    [EVALUATION CRITERIA]
    
    01. Construction of Requested Alternative Count: The number of constructed alternative(s) should be ALWAYS equal to 
    the number of requested alternative(s) by the user: {num_alternatives}
    
    02. Formatted with Plausibly and Attractively: All the formatted alternative options should be ALWAYS plausible and
    attractive BOTH to a less knowledgeable or skillful student
    
    03. Mutual Exclusiveness: Formatted alternative(s) should be mutually exclusive to each other
    
    04. Length Equality: Formatted alternative(s) should be ALWAYS approximately equal in length and weight
    
    05. MCQ Construction Guideline Adherence: Components of MCQ items should be crafted by following several standards 
    and best practices as follows: 
    
    {mcq_construction_guide}
    
    Your task is to evaluate the provided MCQ - Alternative(s) by considering above mentioned criteria. For each and 
    every criteria evaluation, you should suggest a evaluation score (range between 0 to 100) which can be considered as 
    the adherence of criteria of the alternative option(s). Your evaluation result should be delivered in JSON 
    object format where each attribute and value of the object should represent criteria and their evaluation scores 
    (from 0 - 100) respectively.''',
    expected_output='A result JSON object consisting of evaluation criteria and evaluation scores'
)
ALTERNATIVE_OPTION_FORMAT_AGENT_LLM_NAME: str = "gemini-1.5-pro"
ALTERNATIVE_OPTION_EVALUATE_AGENT_LLM_NAME: str = "llama3-8b-8192"
ALTERNATIVE_OPTION_EVALUATE_CUTOFFS: dict = {
    'requested_distractor_count_score': 80,
    'plausible_and_attractive_score': 70,
    'mutual_exclusive_score': 70,
    'length_equality_score': 70,
    'mcq_guideline_score': 70
}
