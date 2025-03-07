from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import os

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

class GithubToolInput(BaseModel):
    """Esquema de entrada para GithubTool"""
    repo: str = Field(..., description="Repositorio en formato 'usuario/repositorio'")
    base: str = Field(..., description="Branch base para el Pull Request")
    head: str = Field(..., description="Branch con los cambios")
    titulo: str = Field(..., description="Título del Pull Request")
    cuerpo: str = Field(..., description="Descripción del Pull Request")

class GithubTool(BaseTool):
    name: str = "github_tool"
    description: str = "Herramienta para crear Pull Requests en GitHub."
    args_schema: Type[BaseModel] = GithubToolInput

    def _run(self, repo: str, base: str, head: str, titulo: str, cuerpo: str) -> str:
        """Crea un Pull Request en GitHub."""
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        data = {"title": titulo, "body": cuerpo, "head": head, "base": base}
        response = requests.post(f"{GITHUB_API_URL}/repos/{repo}/pulls", json=data, headers=headers)
        
        if response.status_code == 201:
            return f"Pull Request creado: {response.json().get('html_url')}"
        else:
            return f"Error en GitHub: {response.status_code} - {response.text}"
