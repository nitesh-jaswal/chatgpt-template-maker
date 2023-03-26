import pytest
import pytest
from api.models.openai_models import Role, Prompt, PromptBuffer
from api.exceptions import BufferExceeded
from typing import List


def test_prompt_buffer_append_within_limit():
    buffer = PromptBuffer(2)
    prompt1 = Prompt(Role.SYSTEM, "Hello")
    prompt2 = Prompt(Role.USER, "Hi")

    buffer.append(prompt1)
    buffer.append(prompt2)

    assert len(buffer) == 2
    assert buffer[0] == prompt1
    assert buffer[1] == prompt2


def test_prompt_buffer_append_exceed_limit():
    # Test raises when more than max_prompts
    # Arrange
    buffer = PromptBuffer(1)
    prompt1 = Prompt(Role.SYSTEM, "Hello")
    prompt2 = Prompt(Role.USER, "Hi")
    buffer.append(prompt1)
    # Act, Assert
    with pytest.raises(BufferExceeded) as exc:
        buffer.append(prompt2)
    msg = exc.value.args
    assert len(msg) == 1
    assert msg[0] == f"Buffer exceeded the maximum number of prompts: 1"


def test_prompt_buffer_extend_within_limit():
    # Arrange
    buffer = PromptBuffer(3)
    prompts: List[Prompt] = [Prompt(Role.SYSTEM, "Hello"), Prompt(Role.USER, "Hi"), Prompt(Role.SYSTEM, "How are you?")]

    # Act
    buffer.extend(prompts)
    # Assert
    assert len(buffer) == 3
    for i, prompt in enumerate(prompts):
        assert buffer[i] == prompt
    prompts_in_buffer = []
    for prompt in prompts:
        prompts_in_buffer.append(prompt)
    assert prompts == prompts_in_buffer


def test_prompt_buffer_extend_exceed_limit():
    # Arrange
    buffer = PromptBuffer(2)
    prompts: List[Prompt] = [Prompt(Role.SYSTEM, "Hello"), Prompt(Role.USER, "Hi"), Prompt(Role.SYSTEM, "How are you?")]

    # Act,Assert
    with pytest.raises(BufferExceeded) as exc:
        buffer.extend(prompts)
    msg = exc.value.args
    assert len(msg) == 1
    assert msg[0] == f"Buffer exceeded the maximum number of prompts: 2"


def test_prompt_buffer_iter():
    # Arrange
    buffer = PromptBuffer(2)
    prompt1 = Prompt(Role.SYSTEM, "Hello")
    prompt2 = Prompt(Role.USER, "Hi")
    # Act
    buffer.append(prompt1)
    buffer.append(prompt2)
    for i, prompt in enumerate(buffer):
        # Assert
        assert prompt == buffer[i]


def test_negative_max_prompts():
    # Arrange, Act, Assert
    with pytest.raises(ValueError):
        PromptBuffer(-1)
