from rebot_cooking_agent.skills.context import SkillContext
from rebot_cooking_agent.skills.pick import pick
from rebot_cooking_agent.skills.place import place
from rebot_cooking_agent.types import SkillResult


def pick_and_place(ctx: SkillContext, object_name: str, target_name: str) -> SkillResult:
    r1 = pick(ctx, object_name)
    if not r1.success:
        return r1
    r2 = place(ctx, target_name)
    if not r2.success:
        return r2
    return SkillResult(True, f"Pick-and-place complete: {object_name} -> {target_name}")
