from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import os

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

class SlackToolInput(BaseModel):
    """Esquema de entrada para SlackTool"""
    canal: str = Field(..., description="Canal de Slack donde enviar el mensaje")
    mensaje: str = Field(..., description="Texto del mensaje a enviar")

class SlackTool(BaseTool):
    name: str = "slack_tool"
    description: str = "Herramienta para enviar mensajes a un canal de Slack."
    args_schema: Type[BaseModel] = SlackToolInput

    def _run(self, canal: str, mensaje: str) -> str:
        """Envía un mensaje a un canal de Slack."""
        data = {"channel": canal, "text": mensaje}
        response = requests.post(SLACK_WEBHOOK_URL, json=data)
        
        if response.status_code == 200:
            return "Mensaje enviado correctamente a Slack."
        else:
            return f"Error en Slack: {response.status_code} - {response.text}"
