from pydantic import BaseModel, Field
from typing import List, Union, Dict, Optional
from .__devmodels import Prompt


class OpenAIChatRequest(BaseModel):
    model: str = Field(..., description="ID of the model to use.")
    messages: List[Prompt] = Field(
        ..., description="The messages to generate chat completions for, in the chat format."
    )
    temperature: Optional[float] = Field(1.0, description="What sampling temperature to use, between 0 and 2.")
    top_p: Optional[float] = Field(
        1.0, description="An alternative to sampling with temperature, called nucleus sampling."
    )
    n: Optional[int] = Field(1, description="How many chat completion choices to generate for each input message.")
    stream: Optional[bool] = Field(False, description="If set, partial message deltas will be sent, like in ChatGPT.")
    stop: Optional[Union[str, List[str]]] = Field(
        None, description="Up to 4 sequences where the API will stop generating further tokens."
    )
    max_tokens: Optional[int] = Field(
        None, description="The maximum number of tokens to generate in the chat completion."
    )
    presence_penalty: Optional[float] = Field(
        0.0,
        description="Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far.",
    )
    frequency_penalty: Optional[float] = Field(
        0.0,
        description="Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far.",
    )
    logit_bias: Optional[Dict[str, float]] = Field(
        None, description="Modify the likelihood of specified tokens appearing in the completion."
    )
    user: Optional[str] = Field(
        None,
        description="A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.",
    )

    class Config:
        description = "Request body schema for OpenAI Chat API."
        schema_extra = {
            "example": {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Who won the world series in 2020?"},
                ],
                "temperature": 0.5,
                "top_p": 1,
                "n": 1,
                "stream": False,
                "stop": ["\n"],
                "max_tokens": 50,
                "presence_penalty": 0.0,
                "frequency_penalty": 0.0,
                "logit_bias": {"50256": -100},
                "user": "user-123",
            }
        }
