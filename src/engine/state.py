class GameState:
    def __init__(self):
        self.flags: dict[str, bool] = {}
        self.vars: dict[str, int | float | str] = {}

    def get_flat(self, name: str, default: bool = False) -> bool:
        return self.flags.get(name, default)

    def set_flag(self, name: str, val: bool) -> None:
        if not isinstance(val, bool):
            raise TypeError("Flag values must be bool")
        self.flags[name] = val

    def get_var(self, name: str, default=None):
        return self.vars.get(name, default)

    def set_var(self, name: str, val: int | float | str) -> None:
        self.vars[name] = val

    def inc_var(self, name: str, amt: int | float = 1) -> int | float:
        curr = self.vars.get(name, 0)

        if not isinstance(curr, (int, float)):
            raise TypeError(f"Variable '{name}' is not numeric")

        self.vars[name] = curr + amt
        return curr + amt

    def reset(self) -> None:
        self.flags.clear()
        self.vars.clear()
