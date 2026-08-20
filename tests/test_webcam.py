from gesture_controller.camera.webcam import Webcam


def test_webcam_class_has_required_methods():
    assert hasattr(Webcam, "read")
    assert hasattr(Webcam, "release")
