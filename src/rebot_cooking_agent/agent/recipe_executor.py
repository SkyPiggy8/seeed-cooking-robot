from pathlib import Path
from rich.console import Console
from rebot_cooking_agent.config import load_yaml
from rebot_cooking_agent.skills.context import SkillContext
from rebot_cooking_agent.skills.pick import pick
from rebot_cooking_agent.skills.place import place
from rebot_cooking_agent.skills.compound import pick_and_place
from rebot_cooking_agent.skills.pour import pour
from rebot_cooking_agent.skills.stir import stir
from rebot_cooking_agent.types import SkillResult

console = Console()


class RecipeExecutor:
    def __init__(self, ctx: SkillContext) -> None:
        self.ctx = ctx

    def execute_file(self, recipe_path: str | Path) -> list[SkillResult]:
        data = load_yaml(recipe_path)
        steps = data.get("recipe", {}).get("steps", [])
        return self.execute_steps(steps)

    def execute_steps(self, steps: list[dict]) -> list[SkillResult]:
        results: list[SkillResult] = []
        for i, step in enumerate(steps, start=1):
            skill = step.get("skill")
            console.rule(f"Step {i}: {skill}")
            if skill == "move_home":
                self.ctx.robot.move_home()
                result = SkillResult(True, "Moved home")
            elif skill == "detect":
                # detect is implicit in pick; here we only log for planning visibility.
                result = SkillResult(True, f"Detection requested: {step.get('object')}")
            elif skill == "pick":
                result = pick(self.ctx, step["object"])
            elif skill == "place":
                result = place(self.ctx, step["target"])
            elif skill == "pick_and_place":
                result = pick_and_place(self.ctx, step["object"], step["target"])
            elif skill == "pour":
                result = pour(self.ctx, step["source"], step["target"])
            elif skill == "stir":
                result = stir(self.ctx, step["target"], float(step.get("seconds", 5)))
            else:
                result = SkillResult(False, f"Unknown skill: {skill}")
            console.log(result)
            results.append(result)
            if not result.success:
                break
        return results
