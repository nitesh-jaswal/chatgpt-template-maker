from pydantic import SecretStr, Field 
from pydantic import BaseSettings, BaseModel


class OpenAIAuthSettings(BaseSettings):
    api_secret: SecretStr = Field(..., help="The api_token you can obtain from your openai account")
    organization_id: str = Field(..., help="The organization_id associated with your openai account")

    class Config:
        env_prefix = "OPENAI_"


class OpenAIAPISettings(BaseModel):
    system_prompt: str | None
    max_prompts: int
    ...