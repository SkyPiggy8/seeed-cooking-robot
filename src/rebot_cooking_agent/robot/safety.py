from dataclasses import dataclass
from rebot_cooking_agent.types import Point3D, Pose3D


@dataclass(frozen=True)
class WorkspaceBounds:
    x_min: float = 0.15
    x_max: float = 0.65
    y_min: float = -0.35
    y_max: float = 0.35
    z_min: float = 0.02
    z_max: float = 0.55


class SafetyValidator:
    def __init__(self, bounds: WorkspaceBounds | None = None) -> None:
        self.bounds = bounds or WorkspaceBounds()
        self._estop = False

    def emergency_stop(self) -> None:
        self._estop = True

    def clear_emergency_stop(self) -> None:
        self._estop = False

    def validate_workspace(self, point: Point3D) -> bool:
        b = self.bounds
        return b.x_min <= point.x <= b.x_max and b.y_min <= point.y <= b.y_max and b.z_min <= point.z <= b.z_max

    def validate_pose(self, pose: Pose3D) -> bool:
        if self._estop:
            return False
        return self.validate_workspace(pose.position)

    def assert_pose_safe(self, pose: Pose3D) -> None:
        if self._estop:
            raise RuntimeError("Emergency stop is active")
        if not self.validate_pose(pose):
            raise ValueError(f"Unsafe pose outside workspace: {pose}")
