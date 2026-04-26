import argparse
from rebot_cooking_agent.perception.camera import RGBDCamera
from rebot_cooking_agent.perception.detector import ObjectDetector
from rebot_cooking_agent.perception.pose_estimator import PoseEstimator
from rebot_cooking_agent.perception.handeye_transform import HandEyeTransform
from rebot_cooking_agent.grasping.grasp_planner import GraspPlanner
from rebot_cooking_agent.robot.rebot_arm import RebotArmController
from rebot_cooking_agent.skills.context import SkillContext
from rebot_cooking_agent.skills.compound import pick_and_place


def build_context(dry_run: bool = True) -> SkillContext:
    return SkillContext(
        camera=RGBDCamera(mock_mode=True),
        detector=ObjectDetector(mock_mode=True),
        pose_estimator=PoseEstimator(),
        handeye=HandEyeTransform(),
        grasp_planner=GraspPlanner(),
        robot=RebotArmController(dry_run=dry_run),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--object", default="tomato")
    parser.add_argument("--target", default="bowl")
    parser.add_argument("--execute", action="store_true", help="Disable dry-run; requires real hardware implementation.")
    args = parser.parse_args()
    ctx = build_context(dry_run=not args.execute)
    result = pick_and_place(ctx, args.object, args.target)
    print(result)


if __name__ == "__main__":
    main()
