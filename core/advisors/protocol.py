from typing import Protocol

from core.models import Argument, Perspective


class AdvisorProtocol(Protocol):
    async def generate_perspective(self, question: str, context: dict) -> Perspective:
        ...

    async def generate_counter_argument(
        self, perspectives: list[Perspective]
    ) -> Argument:
        ...

    async def judge(
        self, arguments: list[Argument], question: str
    ) -> dict:
        ...
