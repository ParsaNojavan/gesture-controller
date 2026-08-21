from gesture_controller.controllers.brightness import (
    BrightnessController,
)


class FakeRunner:
    def __init__(self) -> None:
        self.commands: list[list[str]] = []

    def run(self, command: list[str]):
        self.commands.append(command)
        return None


def test_brightness_percentage_is_converted_to_integer_percent():
    runner = FakeRunner()
    controller = BrightnessController(runner=runner)

    controller.set_percentage(63.7)

    assert runner.commands == [
        [
            "brightnessctl",
            "set",
            "64%",
        ]
    ]


def test_brightness_is_clamped_to_zero():
    runner = FakeRunner()
    controller = BrightnessController(runner=runner)

    controller.set_percentage(-10.0)

    assert runner.commands[0][-1] == "0%"


def test_brightness_is_clamped_to_hundred():
    runner = FakeRunner()
    controller = BrightnessController(runner=runner)

    controller.set_percentage(140.0)

    assert runner.commands[0][-1] == "100%"
