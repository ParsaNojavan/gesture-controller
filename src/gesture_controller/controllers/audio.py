from __future__ import annotations

from gesture_controller.controllers.system import CommandRunner


class VolumeController:

    def __init__(
        self,
        runner: CommandRunner | None = None,
    ) -> None:
        self.runner = runner or CommandRunner()

    def set_percentage(self, percentage: float) -> None:
        percentage = max(0.0, min(100.0, percentage))

        command = [
            "wpctl",
            "set-volume",
            "@DEFAULT_AUDIO_SINK@",
            f"{percentage / 100.0:.3f}",
        ]

        self.runner.run(command)