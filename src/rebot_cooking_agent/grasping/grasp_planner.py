from dataclasses import dataclass
from rebot_cooking_agent.types import ObjectPose, Point3D, Pose3D


@dataclass(frozen=True)
class GraspPlan:
    pregrasp: Pose3D
    grasp: Pose3D
    lift: Pose3D
    yaw: float


class GraspPlanner:
    def __init__(self, pregrasp_lift_m: float = 0.10, lift_m: float = 0.12) -> None:
        self.pregrasp_lift_m = pregrasp_lift_m
        self.lift_m = lift_m

    def plan_top_down_grasp(self, obj: ObjectPose) -> GraspPlan:
        p = obj.pose.position
        yaw = obj.pose.yaw
        grasp = Pose3D(Point3D(p.x, p.y, max(p.z, 0.03), frame_id="robot_base"), pitch=3.14159, yaw=yaw, frame_id="robot_base")
        pre = Pose3D(Point3D(p.x, p.y, p.z + self.pregrasp_lift_m, frame_id="robot_base"), pitch=3.14159, yaw=yaw, frame_id="robot_base")
        lift = Pose3D(Point3D(p.x, p.y, p.z + self.lift_m, frame_id="robot_base"), pitch=3.14159, yaw=yaw, frame_id="robot_base")
        return GraspPlan(pregrasp=pre, grasp=grasp, lift=lift, yaw=yaw)
