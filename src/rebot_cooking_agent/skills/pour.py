from rebot_cooking_agent.skills.context import SkillContext
from rebot_cooking_agent.types import SkillResult


def pour(ctx: SkillContext, source_name: str, target_name: str) -> SkillResult:
    # Keep this dry-run until the gripper geometry and safe tilt angle are measured.
    return SkillResult(True, f"[mock] pour {source_name} into {target_name}")
