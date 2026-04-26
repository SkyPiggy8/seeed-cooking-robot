from rebot_cooking_agent.skills.context import SkillContext
from rebot_cooking_agent.types import Point3D, Pose3D, SkillResult


DEFAULT_TARGETS: dict[str, Pose3D] = {
    "bowl": Pose3D(Point3D(0.42, 0.18, 0.08), pitch=3.14159),
    "pan": Pose3D(Point3D(0.48, -0.12, 0.10), pitch=3.14159),
    "plate": Pose3D(Point3D(0.32, 0.25, 0.08), pitch=3.14159),
    "burger_prep_area": Pose3D(Point3D(0.40, 0.00, 0.08), pitch=3.14159),
}


def place(ctx: SkillContext, target_name: str) -> SkillResult:
    target = DEFAULT_TARGETS.get(target_name)
    if target is None:
        return SkillResult(False, f"Unknown place target: {target_name}")
    pre = Pose3D(Point3D(target.position.x, target.position.y, target.position.z + 0.12), pitch=target.pitch, yaw=target.yaw)
    ctx.robot.move_to_pose(pre)
    ctx.robot.move_to_pose(target)
    ctx.robot.open_gripper()
    ctx.robot.move_to_pose(pre)
    return SkillResult(True, f"Placed object to {target_name}")
