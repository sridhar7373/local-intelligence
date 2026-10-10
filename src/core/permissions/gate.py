
from dataclasses import dataclass


@dataclass
class PermissionDecision:
    allowed: bool
    reason: str


class PermissionGate:
    def __init__(self) -> None:
        self.allowed_capabilities: set[str] = {
            "data.calculate",
            "data.read",
        }

    def check(self, capability: str) -> PermissionDecision:
        if capability in self.allowed_capabilities:
            return PermissionDecision(
                allowed=True,
                reason="Capability is allowed.",
            )

        return PermissionDecision(
            allowed=False,
            reason=f"Capability '{capability}' is not allowed.",
        )
