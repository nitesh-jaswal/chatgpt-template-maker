from pydantic import BaseSettings, SecretStr, Field


class OpenAISettings(BaseSettings):
    api_secret: SecretStr = Field(..., help="The api_token you can obtain from your openai account")
    organization_id: str = Field(..., help="The organization_id associated with your openai account")

    class Config:
        env_prefix = "OPENAI_"
