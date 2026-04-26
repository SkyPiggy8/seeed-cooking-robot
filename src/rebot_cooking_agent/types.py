from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(frozen=True)
class Point3D:
    x: float
    y: float
    z: float
    frame_id: str = "robot_base"


@dataclass(frozen=True)
class Pose3D:
    position: Point3D
    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0
    frame_id: str = "robot_base"


@dataclass(frozen=True)
class CameraIntrinsics:
    fx: float
    fy: float
    cx: float
    cy: float
    width: int
    height: int


@dataclass
class Detection:
    label: str
    confidence: float
    bbox_xyxy: tuple[int, int, int, int]
    angle_rad: Optional[float] = None
    mask: Optional[Any] = None


@dataclass
class ObjectPose:
    label: str
    pose: Pose3D
    confidence: float
    source_detection: Optional[Detection] = None


@dataclass
class SkillResult:
    success: bool
    message: str
    data: dict[str, Any] = field(default_factory=dict)
