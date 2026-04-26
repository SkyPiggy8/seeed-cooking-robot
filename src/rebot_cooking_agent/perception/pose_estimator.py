import numpy as np
from rebot_cooking_agent.types import CameraIntrinsics, Detection, ObjectPose, Point3D, Pose3D


class PoseEstimator:
    """Estimate object pose in camera frame using bbox center and depth median."""

    def estimate(self, detection: Detection, depth_image: np.ndarray, intrinsics: CameraIntrinsics) -> ObjectPose:
        x1, y1, x2, y2 = detection.bbox_xyxy
        u = int((x1 + x2) / 2)
        v = int((y1 + y2) / 2)
        patch = depth_image[max(0, v - 5): v + 6, max(0, u - 5): u + 6]
        valid = patch[np.isfinite(patch) & (patch > 0)]
        if valid.size == 0:
            raise ValueError(f"No valid depth for {detection.label}")
        z = float(np.median(valid))
        x = (u - intrinsics.cx) * z / intrinsics.fx
        y = (v - intrinsics.cy) * z / intrinsics.fy
        point = Point3D(x=x, y=y, z=z, frame_id="camera_color_optical_frame")
        pose = Pose3D(position=point, yaw=detection.angle_rad or 0.0, frame_id="camera_color_optical_frame")
        return ObjectPose(label=detection.label, pose=pose, confidence=detection.confidence, source_detection=detection)
