# src/java_docker_api/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, crew, task, agent
from crewai_tools import SerperDevTool

search_tool = SerperDevTool()


@CrewBase
class JavaDockerApiCrew:
    """Crew that generates a production-ready Java Spring-Boot REST service packaged in Docker."""

    agents_config = "config/agents.yaml"
    tasks_config   = "config/tasks.yaml"

    @agent
    def java_code_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["java_code_generator"],
            tools=[search_tool],
            verbose=True,
        )

    @agent
    def code_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["code_reviewer"],
            tools=[search_tool],
            verbose=True,
        )

    @agent
    def docker_expert(self) -> Agent:
        return Agent(
            config=self.agents_config["docker_expert"],
            tools=[search_tool],
            verbose=True,
        )

    @task
    def generate_project(self) -> Task:
        return Task(
            config=self.tasks_config["generate_project"],
            agent=self.java_code_generator(),
        )

    @task
    def review_project(self) -> Task:
        return Task(
            config=self.tasks_config["review_project"],
            agent=self.code_reviewer(),
        )

    @task
    def create_docker_assets(self) -> Task:
        return Task(
            config=self.tasks_config["create_docker_assets"],
            agent=self.docker_expert(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the JavaDockerApi crew"""
        return Crew(
            agents=[
                self.java_code_generator(),
                self.code_reviewer(),
                self.docker_expert(),
            ],
            tasks=[
                self.generate_project(),
                self.review_project(),
                self.create_docker_assets(),
            ],
            process=Process.sequential,
            verbose=True,
        )