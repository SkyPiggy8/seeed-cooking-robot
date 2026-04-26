import numpy as np
from rebot_cooking_agent.types import ObjectPose, Point3D, Pose3D


class HandEyeTransform:
    """Transform object pose from camera frame to robot base frame.

    Replace the identity-ish mock transform with calibrated hand_eye.npz values.
    """

    def __init__(self, transform_camera_to_base: np.ndarray | None = None) -> None:
        if transform_camera_to_base is None:
            transform_camera_to_base = np.array([
                [1.0, 0.0, 0.0, 0.35],
                [0.0, 1.0, 0.0, 0.00],
                [0.0, 0.0, 1.0, -0.35],
                [0.0, 0.0, 0.0, 1.0],
            ], dtype=float)
        self.T_camera_to_base = transform_camera_to_base

    @classmethod
    def from_npz(cls, path: str) -> "HandEyeTransform":
        data = np.load(path)
        key = "T_camera_to_base" if "T_camera_to_base" in data else list(data.keys())[0]
        return cls(transform_camera_to_base=data[key])

    def to_base(self, object_pose: ObjectPose) -> ObjectPose:
        p = object_pose.pose.position
        vec = np.array([p.x, p.y, p.z, 1.0])
        out = self.T_camera_to_base @ vec
        point = Point3D(float(out[0]), float(out[1]), float(out[2]), frame_id="robot_base")
        pose = Pose3D(position=point, yaw=object_pose.pose.yaw, frame_id="robot_base")
        return ObjectPose(label=object_pose.label, pose=pose, confidence=object_pose.confidence, source_detection=object_pose.source_detection)
