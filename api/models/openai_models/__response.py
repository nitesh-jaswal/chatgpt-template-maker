import enum
from typing import List
from pydantic import BaseModel, validator
from .__devmodels import Prompt

# NOTE: Question: How can I turn prompts into templates? Templates need to be a mix of system and user prompts
# NOTE: Question: Add typing.Protocols IsUserPrompt, IsSystemPrompt?


class FinishReason(str, enum.Enum):
    STOP = "stop" # API returned complete model output
    LENGTH = "length" # Incomplete model output due to max_tokens parameter or token limit
    CONTENT_FILTER = "content_filter" # Omitted content due to a flag from our content filters
    NULL = "null" # API response still in progress or incomplete


class Choice(BaseModel):
    message: Prompt
    finish_reason: FinishReason
    index: int

    @validator('finish_reason', pre=True)
    def convert_to_enum(cls, value) -> FinishReason:
        if isinstance(value, str):
            return FinishReason(value)
        return value


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class OpenAIChatResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    usage: Usage
    choices: List[Choice]

if __name__ == "__main__":
    import json
    # Example usage
    response_json = {
        "id": "chatcmpl-abc123",
        "object": "chat.completion",
        "created": 1677858242,
        "model": "gpt-3.5-turbo-0301",
        "usage": {"prompt_tokens": 13, "completion_tokens": 7, "total_tokens": 20},
        "choices": [
            {"message": {"role": "assistant", "content": "\n\nThis is a test!"}, "finish_reason": "stop", "index": 0}
        ],
    }

    parsed_response = OpenAIChatResponse(**response_json)
    print(parsed_response)
    assert json.loads(parsed_response.json()) == response_json
