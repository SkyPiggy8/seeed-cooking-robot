import argparse
from pathlib import Path
from scripts.test_pick_place import build_context
from rebot_cooking_agent.agent.recipe_executor import RecipeExecutor


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--recipe", default="recipes/tomato_egg.yaml")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    ctx = build_context(dry_run=not args.execute)
    executor = RecipeExecutor(ctx)
    results = executor.execute_file(Path(args.recipe))
    print("Final results:")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
