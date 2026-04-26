from rebot_cooking_agent.perception.camera import RGBDCamera
from rebot_cooking_agent.perception.detector import ObjectDetector


def main() -> None:
    camera = RGBDCamera(mock_mode=True)
    detector = ObjectDetector(mock_mode=True)
    rgb, _, _ = camera.read()
    for det in detector.detect(rgb):
        print(det)


if __name__ == "__main__":
    main()
