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


def kickoff_stem_construct_eval_crew(crew_init: CrewInit, **kwargs) -> dict:
    crew = init_crew(crew_init)
    kickoff_result = crew.kickoff(kwargs)
    result = {}
    try:
        result = {
            'crew-kickoff-result': kickoff_result,
            'stem-format-task-result': dict(crew_init.tasks[1].output.exported_output),
            'stem-evaluate-task-result': dict(crew_init.tasks[2].output.exported_output)
        }
    except ValueError:
        result['stem-evaluate-task-result'] = {}
    return result


def kickoff_key_construct_eval_crew(crew_init: CrewInit, **kwargs) -> dict:
    crew = init_crew(crew_init)
    kickoff_result = crew.kickoff(kwargs)
    result = {}
    try:
        result = {
            'crew-kickoff-result': kickoff_result,
            'key-construct-task-result': dict(crew_init.tasks[0].output.exported_output),
            'key-evaluate-task-result': dict(crew_init.tasks[1].output.exported_output)
        }
    except ValueError:
        result['key-evaluate-task-result'] = {}
    return result


def kickoff_distractor_construct_eval_crew(crew_init: CrewInit, **kwargs) -> dict:
    crew = init_crew(crew_init)
    kickoff_result = crew.kickoff(kwargs)
    result = {}
    try:
        result = {
            'crew-kickoff-result': kickoff_result,
            'distractor-construct-task-result': dict(crew_init.tasks[0].output.exported_output),
            'distractor-evaluate-task-result': dict(crew_init.tasks[1].output.exported_output)
        }
    except ValueError:
        result['distractor-evaluate-task-result'] = {}
    return result


def kickoff_alternative_option_format_eval_crew(crew_init: CrewInit, **kwargs) -> dict:
    crew = init_crew(crew_init)
    kickoff_result = crew.kickoff(kwargs)
    result = {}
    try:
        result = {
            'crew-kickoff-result': kickoff_result,
            'alternatives-format-task-result': dict(crew_init.tasks[0].output.exported_output),
            'alternatives-evaluate-task-result': dict(crew_init.tasks[1].output.exported_output)
        }
    except ValueError:
        result['alternatives-evaluate-task-result'] = {}
    return result
