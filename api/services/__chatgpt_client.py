from __future__ import annotations

import logging 
from api.settings import OpenAIAuthSettings, OpenAIAPISettings
from api.exceptions import OpenAIClientAuthException, BufferExceeded
from api.models import Role, Prompt, PromptBuffer
from api.models.dev_models import ModelResponse, ModelResponseBuffer
from typing import List, cast

DEFAULT_SYSTEM_PROMPT = Prompt(
    role=Role.SYSTEM,
    content="Please answer in less than 200 words the response to the following query"
)

def _get_logger() -> logging.Logger:
    logger = logging.getLogger()
    logging.basicConfig(level=logging.DEBUG)
    return logger

class ChatGPTClient:
    auth: OpenAIAuthSettings | None = None

    def __init__(self, api_settings: OpenAIAPISettings, logger: logging.Logger | None = None):
        if self.auth is None:
            raise OpenAIClientAuthException("Client auth settings not available. Please verify")
        self.logger = logger if logger else _get_logger()
        self.system_prompt = DEFAULT_SYSTEM_PROMPT if api_settings.system_prompt is None else api_settings.system_prompt
        
        self._buffer: PromptBuffer = PromptBuffer(api_settings.max_prompts)

    def buffer_length(self) -> int:
        return len(self._buffer)
    
    def add_messages(self, messages: List[Prompt]) -> ChatGPTClient:
        self._buffer.extend(messages)
        return self
    
    def send_messages(self) -> ModelResponse:
        return cast(ModelResponse, None)

        
    @property
    def buffer_list(self) -> List[Prompt]:
        return cast(List[Prompt], self._buffer[:] )