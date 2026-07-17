# Sabdo Pandito Ratu - Open-Source Deliberation Engine
# Copyright (C) 2026 OptimaSeo Indonesia
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from abc import ABC, abstractmethod

from core.models import Argument, Perspective


class BaseAdvisor(ABC):
    def __init__(self, advisor_id: str, model: str, config: dict | None = None):
        self.advisor_id = advisor_id
        self.model = model
        self.config = config or {}

    @abstractmethod
    async def generate_perspective(self, question: str, context: dict) -> Perspective:
        ...

    @abstractmethod
    async def generate_counter_argument(
        self, perspectives: list[Perspective]
    ) -> Argument:
        ...

    @abstractmethod
    async def judge(
        self, arguments: list[Argument], question: str
    ) -> dict:
        ...
