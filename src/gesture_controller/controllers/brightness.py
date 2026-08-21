from __future__ import annotations

from gesture_controller.controllers.system import CommandRunner


class BrightnessController:
    
    def __init__(
        self,
        runner: CommandRunner | None = None,
    ) -> None:
        self.runner = runner or CommandRunner()

    def set_percentage(self, percentage: float) -> None:
        percentage = max(0.0, min(100.0, percentage))

        command = [
            "brightnessctl",
            "set",
            f"{percentage:.0f}%",
        ]

        self.runner.run(command)
