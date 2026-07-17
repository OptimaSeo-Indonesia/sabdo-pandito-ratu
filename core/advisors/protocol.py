# Sabdo Pandito Ratu
# Copyright (c) 2026 OptimaSeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, version 3.
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
