from rich.console import Console
from rebot_cooking_agent.types import Pose3D
from rebot_cooking_agent.robot.safety import SafetyValidator

console = Console()


class RebotArmController:
    """Safe wrapper for reBot Arm.

    Current implementation is mock/dry-run. Replace _hardware_* methods with MotorBridge / SDK calls.
    """

    def __init__(self, dry_run: bool = True, safety: SafetyValidator | None = None) -> None:
        self.dry_run = dry_run
        self.safety = safety or SafetyValidator()
        self.current_pose: Pose3D | None = None

    def move_home(self) -> None:
        console.log("[robot] move_home")

    def move_to_pose(self, pose: Pose3D, speed: float = 0.2) -> None:
        self.safety.assert_pose_safe(pose)
        if self.dry_run:
            console.log(f"[robot][dry-run] move_to_pose={pose} speed={speed}")
        else:
            self._hardware_move_to_pose(pose, speed)
        self.current_pose = pose

    def open_gripper(self) -> None:
        console.log("[robot] open_gripper" if not self.dry_run else "[robot][dry-run] open_gripper")

    def close_gripper(self) -> None:
        console.log("[robot] close_gripper" if not self.dry_run else "[robot][dry-run] close_gripper")

    def stop(self) -> None:
        self.safety.emergency_stop()
        console.log("[robot] emergency stop")

    def _hardware_move_to_pose(self, pose: Pose3D, speed: float) -> None:
        raise NotImplementedError("Connect reBot Arm MotorBridge / Python SDK here.")
