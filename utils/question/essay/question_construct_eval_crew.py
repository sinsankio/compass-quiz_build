from crewai import Agent, Task, Process, Crew


class CrewInit:
    agents: list[Agent]
    tasks: list[Task]
    process: Process = Process.sequential
    verbose: bool = True


def init_crew(crew_init: CrewInit) -> Crew:
    return Crew(
        agents=crew_init.agents,
        tasks=crew_init.tasks,
        process=crew_init.process,
        verbose=crew_init.verbose
    )


def kickoff_crew(crew_init: CrewInit, **kickoff_kwargs) -> str | dict:
    crew = init_crew(crew_init=crew_init)
    return crew.kickoff(kickoff_kwargs)


def kickoff_question_construct_eval_crew(crew_init: CrewInit, **kwargs) -> dict:
    crew = init_crew(crew_init=crew_init)
    kickoff_result = crew.kickoff(kwargs)
    result = {}
    try:
        result = {
            'crew-kickoff-result': kickoff_result,
            'question-format-task-result': dict(crew_init.tasks[1].output.exported_output),
            'question-evaluate-task-result': dict(crew_init.tasks[2].output.exported_output)
        }
    except ValueError:
        result['question-evaluate-task-result'] = {}
    return result


def kickoff_answer_construct_eval_crew(crew_init: CrewInit, **kwargs) -> dict:
    crew = init_crew(crew_init=crew_init)
    kickoff_result = crew.kickoff(kwargs)
    result = {}
    try:
        result = {
            'crew-kickoff-result': kickoff_result,
            'answer-format-task-result': dict(crew_init.tasks[1].output.exported_output),
            'answer-evaluate-task-result': dict(crew_init.tasks[2].output.exported_output)
        }
    except ValueError:
        result['answer-evaluate-task-result'] = {}
    return result
