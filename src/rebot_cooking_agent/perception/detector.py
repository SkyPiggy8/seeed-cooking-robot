import numpy as np
from rebot_cooking_agent.types import Detection


class ObjectDetector:
    """Object detector interface.

    In mock mode we return a fixed tabletop scene. That keeps camera, pose
    estimation, grasp planning, and recipe execution testable before the real
    detector weights are ready.
    """

    def __init__(self, model_path: str | None = None, mock_mode: bool = True, confidence_threshold: float = 0.35) -> None:
        self.model_path = model_path
        self.mock_mode = mock_mode
        self.confidence_threshold = confidence_threshold

    def detect(self, image: np.ndarray) -> list[Detection]:
        if self.mock_mode:
            return [
                Detection(label="tomato", confidence=0.92, bbox_xyxy=(560, 320, 640, 400), angle_rad=0.0),
                Detection(label="bowl", confidence=0.91, bbox_xyxy=(760, 300, 900, 440), angle_rad=0.0),
                Detection(label="pan", confidence=0.88, bbox_xyxy=(430, 250, 620, 430), angle_rad=0.0),
                Detection(label="egg_bowl", confidence=0.84, bbox_xyxy=(920, 320, 1040, 440), angle_rad=0.0),
                Detection(label="seasoning", confidence=0.80, bbox_xyxy=(250, 330, 320, 430), angle_rad=0.0),
                Detection(label="burger", confidence=0.87, bbox_xyxy=(680, 330, 800, 450), angle_rad=0.0),
            ]
        raise NotImplementedError("Real detector backend is not wired yet. Load YOLO / YOLO-OBB here.")

    def find_one(self, image: np.ndarray, label: str) -> Detection | None:
        detections = self.detect(image)
        candidates = [d for d in detections if d.label == label and d.confidence >= self.confidence_threshold]
        return max(candidates, key=lambda d: d.confidence) if candidates else None
