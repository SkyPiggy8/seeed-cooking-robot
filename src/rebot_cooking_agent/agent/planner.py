
class SimpleCookingPlanner:
    """Small rule-based planner used before the planner becomes configurable."""

    def plan(self, user_task: str) -> list[dict]:
        text = user_task.lower()
        if "番茄" in user_task or "tomato" in text:
            return [
                {"skill": "move_home"},
                {"skill": "pick", "object": "tomato"},
                {"skill": "place", "target": "pan"},
                {"skill": "pick", "object": "egg_bowl"},
                {"skill": "pour", "source": "egg_bowl", "target": "pan"},
                {"skill": "stir", "target": "pan", "seconds": 5},
                {"skill": "move_home"},
            ]
        if "汉堡" in user_task or "burger" in text or "hamburger" in text:
            return [
                {"skill": "move_home"},
                {"skill": "detect", "object": "burger"},
                {"skill": "pick", "object": "burger"},
                {"skill": "place", "target": "plate"},
                {"skill": "move_home"},
            ]
        return [{"skill": "move_home"}]
