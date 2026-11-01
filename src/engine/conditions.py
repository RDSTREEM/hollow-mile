from typing import Any

from engine.state import GameState


class Evaluator:

    def __init__(self, state: GameState):
        self.state = state

    def eval(self, condition: Any) -> bool:
        if condition is None:
            return True

        if not isinstance(condition, dict):
            raise ValueError("A condition must be a dictionary.")

        if "all" in condition:
            condition = condition["all"]
            return all(self.eval(item) for item in condition)

        if "any" in condition:
            condition = condition["any"]
            return any(self.eval(item) for item in condition)

        if "not" in condition:
            return not self.eval(condition["not"])

        if "flag" in condition:
            name = condition["flag"]
            expected = condition.get("equals", True)

            return self.state.get_flag(name) == expected

        if "variable" in condition:
            name = condition["variable"]
            actual = self.state.get_var(name)
            expected = condition.get("value")
            op = condition.get("operator", "==")

            compare = {
                "==": lambda a, b: a == b,
                "!=": lambda a, b: a != b,
                ">=": lambda a, b: a is not None and a >= b,
                "<=": lambda a, b: a is not None and a <= b,
                ">": lambda a, b: a is not None and a > b,
                "<": lambda a, b: a is not None and a < b,
            }

            if op not in compare:
                raise ValueError(f"Unknown condition operator: {op}")

            return compare[op](actual, expected)

        raise ValueError(f"Unrecognized condition: {condition}")
