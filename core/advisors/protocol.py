# Sabdo Pandito Ratu - Open-Source Deliberation Engine
# Copyright (C) 2025 OptimaSeo Indonesia
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
