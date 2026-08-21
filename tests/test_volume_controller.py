from gesture_controller.controllers.audio import VolumeController


class FakeRunner:
    def __init__(self) -> None:
        self.commands: list[list[str]] = []

    def run(self, command: list[str]):
        self.commands.append(command)
        return None


def test_volume_percentage_is_converted_to_wpctl_value():
    runner = FakeRunner()
    controller = VolumeController(runner=runner)

    controller.set_percentage(50.0)

    assert runner.commands == [
        [
            "wpctl",
            "set-volume",
            "@DEFAULT_AUDIO_SINK@",
            "0.500",
        ]
    ]


def test_volume_is_clamped_to_zero():
    runner = FakeRunner()
    controller = VolumeController(runner=runner)

    controller.set_percentage(-20.0)

    assert runner.commands[0][-1] == "0.000"


def test_volume_is_clamped_to_hundred():
    runner = FakeRunner()
    controller = VolumeController(runner=runner)

    controller.set_percentage(150.0)

    assert runner.commands[0][-1] == "1.000"
