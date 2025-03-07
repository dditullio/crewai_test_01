from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import os

JIRA_API_URL = os.getenv("JIRA_API_URL")
JIRA_API_KEY = os.getenv("JIRA_API_KEY")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")

class JiraToolInput(BaseModel):
    """Esquema de entrada para JiraTool"""
    proyecto_id: str = Field(..., description="ID del proyecto en JIRA")

class JiraTool(BaseTool):
    name: str = "jira_tool"
    description: str = "Herramienta para obtener y priorizar el backlog en JIRA."
    args_schema: Type[BaseModel] = JiraToolInput

    def _run(self, proyecto_id: str) -> str:
        """Obtiene el backlog del proyecto en JIRA."""
        headers = {
            "Authorization": f"Basic {JIRA_API_KEY}",
            "Content-Type": "application/json"
        }
        response = requests.get(f"{JIRA_API_URL}/rest/api/3/search?jql=project={proyecto_id}", headers=headers)
        
        if response.status_code == 200:
            return response.text  # CrewAI espera un string como salida
        else:
            return f"Error en JIRA: {response.status_code} - {response.text}"
