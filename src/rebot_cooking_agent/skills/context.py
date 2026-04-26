from dataclasses import dataclass
from rebot_cooking_agent.perception.camera import RGBDCamera
from rebot_cooking_agent.perception.detector import ObjectDetector
from rebot_cooking_agent.perception.pose_estimator import PoseEstimator
from rebot_cooking_agent.perception.handeye_transform import HandEyeTransform
from rebot_cooking_agent.grasping.grasp_planner import GraspPlanner
from rebot_cooking_agent.robot.rebot_arm import RebotArmController


@dataclass
class SkillContext:
    camera: RGBDCamera
    detector: ObjectDetector
    pose_estimator: PoseEstimator
    handeye: HandEyeTransform
    grasp_planner: GraspPlanner
    robot: RebotArmController
    last_object_name: str | None = None
