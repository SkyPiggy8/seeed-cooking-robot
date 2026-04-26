from rebot_cooking_agent.skills.context import SkillContext
from rebot_cooking_agent.types import SkillResult


def stir(ctx: SkillContext, target_name: str, seconds: float = 5.0) -> SkillResult:
    # Keep this dry-run until we measure a pan-safe stirring radius.
    return SkillResult(True, f"[mock] stir {target_name} for {seconds:.1f}s")
