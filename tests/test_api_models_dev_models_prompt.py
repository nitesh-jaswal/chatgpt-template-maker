import pytest
import pytest
import random
from string import ascii_letters
from api.models import Role, Prompt
from typing import Callable

@pytest.fixture
def get_random_word() -> Callable[..., str]:
    def _() -> str:
        word_length = random.randint(1, 9)
        return "".join(random.choices(ascii_letters, k=word_length))
    return _

@pytest.fixture
def random_2048_tokens_string(get_random_word: Callable[..., str]) -> str:
    return " ".join([get_random_word() for _ in range(2048)])

def test_prompt_less_than_2048_tokens(random_2048_tokens_string: str):
    # Arrange, Act, Assert
    user_prompt = Prompt(role=Role.SYSTEM, content=random_2048_tokens_string)
    system_prompt = Prompt(role=Role.USER, content=random_2048_tokens_string)
    assert system_prompt and user_prompt

def test_prompt_greater_than_2048_tokens(random_2048_tokens_string: str):
    # Arrange
    random_2048_tokens_string = random_2048_tokens_string + " extra_token"
    # Act, Assert
    with pytest.raises(ValueError) as exc:
        user_prompt = Prompt(role=Role.SYSTEM, content=random_2048_tokens_string)
        system_prompt = Prompt(role=Role.USER, content=random_2048_tokens_string)
    msg = exc.value.args
    assert len(msg) == 1
    assert msg[0] == "The content length must be less than 2048 tokens(words)"

def test_prompt_length():
    # Arrange, Act
    prompt = Prompt(role=Role.SYSTEM, content="This is some content")
    # Assert
    assert prompt.length == 4