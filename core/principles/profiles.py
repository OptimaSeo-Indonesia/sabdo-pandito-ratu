from pydantic import BaseModel, Field


class PrincipleWeights(BaseModel):
    fairness: float = Field(default=0.20, ge=0, le=1)
    transparency: float = Field(default=0.20, ge=0, le=1)
    sustainability: float = Field(default=0.20, ge=0, le=1)
    human_impact: float = Field(default=0.20, ge=0, le=1)
    accountability: float = Field(default=0.10, ge=0, le=1)

    @property
    def total(self) -> float:
        return (
            self.fairness
            + self.transparency
            + self.sustainability
            + self.human_impact
            + self.accountability
        )

    def normalized(self) -> dict[str, float]:
        t = self.total or 1.0
        return {
            "fairness": round(self.fairness / t, 4),
            "transparency": round(self.transparency / t, 4),
            "sustainability": round(self.sustainability / t, 4),
            "human_impact": round(self.human_impact / t, 4),
            "accountability": round(self.accountability / t, 4),
        }


class PrincipleProfile(BaseModel):
    name: str
    description: str
    weights: PrincipleWeights


PRINCIPLE_PROFILES: dict[str, PrincipleProfile] = {
    "balanced": PrincipleProfile(
        name="Balanced Decision",
        description="Default profile with equal weight across all principles",
        weights=PrincipleWeights(
            fairness=0.20,
            transparency=0.20,
            sustainability=0.20,
            human_impact=0.20,
            accountability=0.20,
        ),
    ),
    "public_policy": PrincipleProfile(
        name="Public Policy",
        description="Emphasizes transparency and fairness for policy decisions",
        weights=PrincipleWeights(
            fairness=0.30,
            transparency=0.30,
            sustainability=0.15,
            human_impact=0.15,
            accountability=0.10,
        ),
    ),
    "startup": PrincipleProfile(
        name="Startup Decision",
        description="Emphasizes sustainability and impact for business decisions",
        weights=PrincipleWeights(
            fairness=0.10,
            transparency=0.15,
            sustainability=0.30,
            human_impact=0.15,
            accountability=0.30,
        ),
    ),
    "healthcare": PrincipleProfile(
        name="Healthcare Ethics",
        description="Emphasizes human impact and fairness for medical decisions",
        weights=PrincipleWeights(
            fairness=0.25,
            transparency=0.20,
            sustainability=0.10,
            human_impact=0.35,
            accountability=0.10,
        ),
    ),
    "personal": PrincipleProfile(
        name="Personal Decision",
        description="Balanced with lighter accountability for personal choices",
        weights=PrincipleWeights(
            fairness=0.15,
            transparency=0.25,
            sustainability=0.20,
            human_impact=0.30,
            accountability=0.10,
        ),
    ),
}


class PrincipleProfileManager:
    def __init__(self):
        self._profiles = dict(PRINCIPLE_PROFILES)

    def get(self, name: str) -> PrincipleProfile:
        return self._profiles.get(name, self._profiles["balanced"])

    def list(self) -> list[PrincipleProfile]:
        return list(self._profiles.values())

    def register(self, profile: PrincipleProfile) -> None:
        self._profiles[profile.name] = profile

    def apply_weights(
        self, profile_name: str, evaluations: list
    ) -> list:
        profile = self.get(profile_name)
        normalized = profile.weights.normalized()

        for eval_ in evaluations:
            principle_name = eval_.principle if hasattr(eval_, "principle") else ""
            if principle_name in normalized:
                eval_.weight = normalized[principle_name]

        return evaluations
