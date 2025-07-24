# src/java_docker_api/main.py
import os
import sys
import zipfile
from pathlib import Path
from typing import Any

from crewai import TaskOutput
from java_docker_api.crew import JavaDockerApiCrew

# ------------------------------------------------------------------
# 1. Where to drop the artefacts
# ------------------------------------------------------------------
OUT_DIR = Path("generated")
OUT_DIR.mkdir(exist_ok=True)

# ------------------------------------------------------------------
# 2. Crew inputs
# ------------------------------------------------------------------
inputs = {
    "project_name": "java-docker-api",
    "java_version": "17",
    "spring_boot_version": "3.2.0",
    "base_package": "com.example.demo",
}

# ------------------------------------------------------------------
# 3. Helper that writes TaskOutput -> disk
# ------------------------------------------------------------------
def save_task_output(task_output: TaskOutput, filename: str) -> None:
    """
    task_output.raw: str  – the actual text returned by the agent.
    """
    file_path = OUT_DIR / filename
    file_path.write_text(task_output.raw)
    print(f"✅  Saved {file_path}")

# ------------------------------------------------------------------
# 4. Run the crew and wire the callbacks
# ------------------------------------------------------------------
def run() -> None:
    crew_instance = JavaDockerApiCrew()

    # ------------------------------------------------------------------
    # grab the tasks in the same order they are defined
    # ------------------------------------------------------------------
    tasks = [
        crew_instance.generate_project(),
        crew_instance.review_project(),
        crew_instance.create_docker_assets(),
    ]

    # ------------------------------------------------------------------
    # register post-execution callbacks
    # ------------------------------------------------------------------
    tasks[0].callback = lambda out: save_task_output(out, "spring-boot-project.zip")
    tasks[1].callback = lambda out: save_task_output(out, "review_report.md")
    tasks[2].callback = lambda out: save_task_output(out, "docker-files.zip")

    # ------------------------------------------------------------------
    # run the crew
    # ------------------------------------------------------------------
    crew = crew_instance.crew()
    crew.kickoff(inputs=inputs)
    print(f"\n📦  All artefacts written to {OUT_DIR.resolve()}")

# ------------------------------------------------------------------
if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        raise RuntimeError(f"Error while running crew: {e}") from e