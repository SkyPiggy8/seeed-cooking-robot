import numpy as np
from rebot_cooking_agent.types import CameraIntrinsics


class RGBDCamera:
    """RGB-D camera interface. First version uses mock frames.

    Replace the internals with Orbbec Gemini 2 SDK / ROS topic subscription later.
    """

    def __init__(self, mock_mode: bool = True) -> None:
        self.mock_mode = mock_mode
        self.intrinsics = CameraIntrinsics(fx=600.0, fy=600.0, cx=640.0, cy=360.0, width=1280, height=720)

    def read(self) -> tuple[np.ndarray, np.ndarray, CameraIntrinsics]:
        if not self.mock_mode:
            raise NotImplementedError("Connect Orbbec Gemini 2 SDK or ROS image topics here.")
        rgb = np.zeros((720, 1280, 3), dtype=np.uint8)
        depth = np.full((720, 1280), 0.45, dtype=np.float32)
        return rgb, depth, self.intrinsics
