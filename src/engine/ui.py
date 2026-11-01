# if u can call this a ui *insert laughing emoji*

from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Input, RichLog, Static

from engine import Engine


class UI(App):
    TITLE = "HOLLOW MILE"
    SUB_TITLE = "A Station That Should Not Exist"

    ENABLE_COMMAND_PALETTE = False

    CSS = """
    
    Header {
        background: #000000;
        color: #888888;
        text-style: none;
    }

    HeaderTitle {
        color: #aaaaaa;
        text-style: none;
    }

    HeaderSubtitle {
        color: #777777;
        text-style: none;
    }

    HeaderIcon {
        color: #888888;
    }

    CommandPalette {
        display: none;
    }

    Screen {
        background: #000000;
        color: #b5b5b5;
    }

    #main {
        height: 1fr;
    }

    #content {
        width: 1fr;
        height: 1fr;
        padding: 1 2;
    }

    #story-log {
        height: 1fr;
        border: none;
        background: #000000;
        padding: 1 2;
        scrollbar-color: #333333;
    }

    #command {
        height: 3;
        margin-top: 1;
        border: round #555555;
        background: #000000;
    }

    #sidebar {
        width: 32;
        height: 1fr;
        border-left: solid #333333;
        padding: 1 2;
        background: #000000;
    }

    #sidebar-title {
        color: #cccccc;
        text-style: bold;
        margin-bottom: 1;
    }

    #sidebar-info {
        height: 1fr;
    }

    Input {
        color: #cccccc;
        background: #000000;
    }

    Input:focus {
        border: round #aaaaaa;
    }

    Footer {
        background: #080808;
        color: #777777;
    }    """

    BINDINGS = [
        ("ctrl + s", "save_game", "Save"),
        ("ctrl + o", "load_game", "Load"),
        ("f1", "show_help", "Help"),
        ("ctrl + q", "quit_game", "Quit"),
    ]

    def __init__(self, engine: Engine):
        super().__init__()
        self.engine = engine

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        with Horizontal(id="main"):
            with Vertical(id="content"):
                yield RichLog(id="story-log", wrap=True, highlight=False, markup=False)

                yield Input(placeholder="What do you do?", id="command")

            with Vertical(id="sidebar"):
                yield Static("HOLLOW MILE", id="sidebar-title")
                yield Static("", id="sidebar-info")

        # yield Footer()

    def on_mount(self) -> None:
        self._write_line("HOLLOW MILE", style="bold #d5a85f")
        self._write_line("A Station That Should Not Exist", style="italic #9ca88e")
        self._write_line("")
        self._write_line("Type 'help' for available commands.")
        self._write_line("")

        res = self.engine.start()
        self._display_result(res)
        self._update_sidebar()

        self.query_one("#command", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        cmd = event.value.strip()
        event.input.value = ""

        if not cmd:
            return

        self._write_line(f"\n> {cmd}", style="bold #d5a85f")

        if cmd.lower() in {"quit", "exit"}:
            self.action_quit_game()
            return

        res = self.engine.execute(cmd)
        self._display_result(res)
        self._update_sidebar()

    def _write_line(self, content, style: str = ""):
        log = self.query_one("#story-log", RichLog)
        log.write(Text(content, style=style))

    def _display_result(self, res):
        style = "#d7ddcf" if res.success else "#d58b76"
        self._write_line(res.text, style)

        if res.suggestions:
            self._write_line("")
            self._write_line("Suggested actions: ", style="bold #9ca88e")

            for sug in res.suggestions:
                self._write_line(f" - {sug}")

    def _update_sidebar(self):
        info = Text()

        info.append("LOCATION\n", style="bold #d5a85f")

        room = self.engine.world.curr_room

        if room:
            info.append(f"{room.name}\n")
        else:
            info.append(f"Unknown\n")

        info.append("\nINVENTORY\n", style="bold #d5a85f")

        if self.engine.inv.is_empty():
            info.append("Empty\n")
        else:
            for _id in self.engine.inv.items:
                entity = self.engine.world.get_entity(_id)
                info.append(f"- {entity.name}\n")

        self.query_one("#sidebar-info", Static).update(info)

    def action_save_game(self) -> None:
        res = self.engine.execute("save")
        self._display_result(res)

    def action_load_game(self) -> None:
        res = self.engine.execute("load")
        self._display_result(res)
        self._update_sidebar()

    def action_show_help(self) -> None:
        res = self.engine.execute("help")
        self._display_result(res)

    def action_quit_game(self) -> None:
        self._write_line("Your train remains silent.", style="italic #9ca88e")
        self._write_line("HOLLOW MILE - SESSION ENDED", style="bold #d5a85f")
        self.exit()
