from rebot_cooking_agent.skills.context import SkillContext
from rebot_cooking_agent.types import SkillResult


def pick(ctx: SkillContext, object_name: str) -> SkillResult:
    rgb, depth, intrinsics = ctx.camera.read()
    detection = ctx.detector.find_one(rgb, object_name)
    if detection is None:
        return SkillResult(False, f"Object not detected: {object_name}")
    pose_cam = ctx.pose_estimator.estimate(detection, depth, intrinsics)
    pose_base = ctx.handeye.to_base(pose_cam)
    plan = ctx.grasp_planner.plan_top_down_grasp(pose_base)

    ctx.robot.move_to_pose(plan.pregrasp)
    ctx.robot.open_gripper()
    ctx.robot.move_to_pose(plan.grasp)
    ctx.robot.close_gripper()
    ctx.robot.move_to_pose(plan.lift)
    ctx.last_object_name = object_name
    return SkillResult(True, f"Picked {object_name}", {"pose_base": pose_base})
