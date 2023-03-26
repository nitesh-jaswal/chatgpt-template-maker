import pytest
from typing import cast
from api.services import ChatGPTClient
from api.settings import OpenAIAuthSettings, OpenAIAPISettings
from api.exceptions import OpenAIClientAuthException
from api.models.openai_models import Role, Prompt, PromptBuffer, OpenAIChatResponse, Choice, Usage
from unittest.mock import MagicMock, patch
@pytest.fixture
def mock_auth_settings() -> OpenAIAuthSettings:
    return OpenAIAuthSettings(api_key="Th!5_iS_@_s3cREt", organization="sample_organization_id")  # type: ignore


@pytest.fixture
def mock_api_settings() -> OpenAIAPISettings:
    return OpenAIAPISettings(max_prompts=10)  # type: ignore

@pytest.fixture
def mock_openai_client(mocker: MagicMock) -> MagicMock:
    client = MagicMock()
    client.send.return_value = Prompt(Role.ASSISTANT, "This is a test")
    return client

def test_client_raises_auth_is_none(mock_api_settings: OpenAIAPISettings):
    # Arrange, Act, Assert
    with pytest.raises(OpenAIClientAuthException) as exc:
        gpt_client = ChatGPTClient(api_settings=mock_api_settings)
    msg = exc.value.args
    assert len(msg) == 1
    assert msg[0] == "Client auth settings not available. Please verify"


def test_client_default_system_prompt(mock_auth_settings: OpenAIAuthSettings, mock_api_settings: OpenAIAPISettings):
    # Arrange
    ChatGPTClient.auth = mock_auth_settings
    default_prompt = Prompt(
        role=Role.SYSTEM, content="Please answer in less than 200 words the response to the following query"
    )
    # Act
    gpt_client = ChatGPTClient(api_settings=mock_api_settings)
    assert isinstance(gpt_client.system_prompt, Prompt)
    assert gpt_client.system_prompt == default_prompt


def test_client_buffer_list(mock_auth_settings: OpenAIAuthSettings, mock_api_settings: OpenAIAPISettings):
    # Arrange
    ChatGPTClient.auth = mock_auth_settings
    # Act
    gpt_client = ChatGPTClient(api_settings=mock_api_settings)
    # Assert
    assert gpt_client.buffer_list == []

    # Arrange
    messages = [Prompt(Role.USER, prompt) for prompt in (f"test prompt {i}" for i in range(5))]
    # Act
    return_value = gpt_client.add_messages(messages=messages)
    # Assert
    assert isinstance(return_value, ChatGPTClient)
    assert gpt_client.buffer_list == messages


def test_client_add_messages(mock_auth_settings: OpenAIAuthSettings, mock_api_settings: OpenAIAPISettings):
    # Arrange
    messages = [Prompt(Role.USER, prompt) for prompt in (f"test prompt {i}" for i in range(5))]
    ChatGPTClient.auth = mock_auth_settings
    gpt_client = ChatGPTClient(api_settings=mock_api_settings)
    # Assert
    assert isinstance(gpt_client.system_prompt, Prompt)
    # Act
    _ = gpt_client.add_messages(messages=messages).add_messages([Prompt(Role.USER, "extended_prompt")])
    # Assert
    assert gpt_client.buffer_list[-1].content == "extended_prompt"


def test_client_send_messages(mock_auth_settings: OpenAIAuthSettings, mock_api_settings: OpenAIAPISettings, mock_openai_client: MagicMock):
    # Arrange
    messages = [Prompt(Role.USER, prompt) for prompt in (f"test prompt {i}" for i in range(5))]
    ChatGPTClient.auth = mock_auth_settings
    # Prepare the mock response
    mock_response = OpenAIChatResponse(
        id="response-12345",
        object="list",
        created=1615298982,
        model="gpt-3.5-turbo",
        usage=Usage(prompt_tokens=10, completion_tokens=5, total_tokens=15),
        choices=[
            Choice(index=0, message=Prompt(role=Role.USER, content="This is a user response"), finish_reason="stop"), # type: ignore
            Choice(index=0, message=Prompt(role=Role.ASSISTANT, content="This is the assistant response"), finish_reason="stop") # type: ignore
        ] 
    )
    # Act
    gpt_client = ChatGPTClient(api_settings=mock_api_settings)
    # Assert
    with patch("api.services.__baseclient.BaseClient.send", return_value=mock_response) as mock_send:
        response_prompt: Prompt = gpt_client.add_messages(messages=messages).send_messages()
        assert response_prompt.role == Role.ASSISTANT
        assert response_prompt.content == "This is the assistant response"
        assert mock_send.call_count == 1
