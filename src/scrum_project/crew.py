from crewai import Crew, Process, Agent, Task
from crewai.project import CrewBase, agent, crew, task
from .tools.jira_tool import JiraTool  
from .tools.github_tool import GithubTool  
from .tools.slack_tool import SlackTool  

@CrewBase
class ScrumProject():
    """Crew para gestionar el proyecto SCRUM"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    tools = [JiraTool(), GithubTool(), SlackTool()]  # ⚠️ Agregar herramientas aquí

    print(f"Herramientas registradas en CrewBase: {[t.name for t in tools]}")
    
    @agent
    def product_owner(self) -> Agent:
        return Agent(
            config=self.agents_config['product_owner'],
            tools=[JiraTool(), SlackTool()],  # ⚠️ Agregar las herramientas correctamente
            verbose=True
        )

    @agent
    def scrum_master(self) -> Agent:
        return Agent(
            config=self.agents_config['scrum_master'],
            tools=[JiraTool(), SlackTool()],
            verbose=True
        )

    @agent
    def developer(self) -> Agent:
        return Agent(
            config=self.agents_config['developer'],
            tools=[GithubTool(), SlackTool()],
            verbose=True
        )

    @agent
    def tester(self) -> Agent:
        return Agent(
            config=self.agents_config['tester'],
            tools=[JiraTool(), SlackTool()],
            verbose=True
        )
    
    @task
    def refinamiento_backlog(self) -> Task:
        return Task(
            config=self.tasks_config['refinamiento_backlog'],
        )

    @task
    def planificacion_sprint(self) -> Task:
        return Task(
            config=self.tasks_config['planificacion_sprint'],
        )

    @task
    def desarrollo_codigo(self) -> Task:
        return Task(
            config=self.tasks_config['desarrollo_codigo'],
        )

    @task
    def pruebas_calidad(self) -> Task:
        return Task(
            config=self.tasks_config['pruebas_calidad'],
        )

    @task
    def revision_sprint(self) -> Task:
        return Task(
            config=self.tasks_config['revision_sprint'],
        )

    @crew
    def crew(self) -> Crew:
        """Crea el equipo SCRUM"""
        return Crew(
            agents=self.agents,  # Se generan automáticamente con los @agent
            tasks=self.tasks,  # Se generan automáticamente con los @task
            process=Process.sequential,
            verbose=True
        )
