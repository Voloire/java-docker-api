# src/java_docker_api/main.py
import sys
from typing import Any

from java_docker_api.crew import JavaDockerApiCrew


def run() -> None:
    """Run the Java-Docker API generation crew."""
    inputs = {
        "project_name": "java-docker-api",
        "java_version": "17",
        "spring_boot_version": "3.2.0",
        "base_package": "com.example.demo",
    }

    try:
        # ✅ Instantiate the crew, then kick it off
        JavaDockerApiCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}") from e


if __name__ == "__main__":
    run()