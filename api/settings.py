from pydantic import SecretStr, Field
from pydantic import BaseSettings, BaseModel


class OpenAIAuthSettings(BaseSettings):
    api_key: SecretStr = Field(..., help="The secret api token you can obtain from your openai account")
    organization: str = Field(..., help="The organization id associated with your openai account")

    class Config:
        env_prefix = "OPENAI_"


class OpenAIAPISettings(BaseModel):
    system_prompt: str | None
    max_prompts: int
    ...
