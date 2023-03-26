from enum import Enum
from typing import List, Iterator
from dataclasses import dataclass
from api.exceptions import BufferExceeded
from functools import lru_cache, cached_property

# NOTE: Question: How can I turn prompts into templates? Templates need to be a mix of system and user prompts
# NOTE: Question: Add typing.Protocols IsUserPrompt, IsSystemPrompt?


class Role(str, Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class Prompt:
    role: Role
    content: str

    def __post_init__(self):
        self._split_tokens = self.content.split()
        if len(self._split_tokens) > 2048:
            raise ValueError("The content length must be less than 2048 tokens(words)")

    @lru_cache
    def to_dict(self) -> dict[str, str]:
        return dict(role=self.role.value, content=self.content)

    @cached_property
    def length(self) -> int:
        return len(self._split_tokens)


class PromptBuffer:
    def __init__(self, max_prompts: int):
        if max_prompts < 0:
            raise ValueError("max_prompts must be a non-negative integer")
        self.max_prompts = max_prompts
        self._prompts: List[Prompt] = []

    def append(self, prompt: Prompt):
        if len(self._prompts) >= self.max_prompts:
            raise BufferExceeded(f"Buffer exceeded the maximum number of prompts: {self.max_prompts}")
        self._prompts.append(prompt)

    def extend(self, prompts: List[Prompt]):
        for prompt in prompts:
            self.append(prompt)

    def __len__(self):
        return len(self._prompts)

    def __iter__(self) -> Iterator[Prompt]:
        return iter(self._prompts)

    def __getitem__(self, index) -> Prompt:
        self._prompts[index]
        return self._prompts[index]

    def to_list(self) -> List[Prompt]:
        return self._prompts
