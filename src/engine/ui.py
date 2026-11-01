# if u can call this a ui *insert laughing emoji*

from rich.text import Text
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Input, RichLog, Static

from engine import Engine


class UI(App):
    ENABLE_COMMAND_PALETTE = False

    BINDINGS = [
        ("ctrl + s", "save_game", "Save"),
        ("ctrl + o", "load_game", "Load"),
        ("f1", "show_help", "Help"),
        ("ctrl + q", "quit_game", "Quit"),
    ]

    def __init__(self, engine: Engine):
        super().__init__()
        self.engine = engine

        config = engine.story.config.get("ui", {})

        self.ui_config = config
        self._theme: dict = config.get("theme", {})
        self.layout = config.get("layout", {})
        self.command_config = config.get("command", {})

        self.game_title = config.get("title", "HOLLOW MILE")
        self.game_subtitle = config.get("subtitle", "A Station That Should Not Exist")

        self.title = self.game_title
        self.sub_title = self.game_subtitle

        self.sidebar_enabled = self.layout.get("sidebar", True)
        self.sidebar_width = self.layout.get("sidebar_width", 32)
        self.header_enabled = self.layout.get("header", True)
        self.footer_enabled = self.layout.get("footer", False)

        UI.CSS = self._build_css()

    def _build_css(self) -> str:
        bg = self._theme.get("background", "#000000")
        surface = self._theme.get("surface", "#080808")
        text = self._theme.get("text", "#b5b5b5")
        muted = self._theme.get("muted", "#777777")
        border = self._theme.get("border", "#333333:w")

        return f"""
        Screen {{
            background: {bg};
            color: {text};
        }}
        
        #main {{
            height: 1fr;
        }}
        
        #content {{
            width: 1fr;
            height: 1fr;
            padding: 1 2;
        }}
        
        #story-log {{
            height: 1fr;
            border: none;
            background: {bg};
            padding: 1 2;
            scrollbar-color: {border};
        }}
        
        #command {{
            height: 3;
            margin-top: 1;
            border: round {muted};
            background: {bg}
        }}
        
        #command:focus {{
            border: round {text};
        }}
        
        Input {{
            color: {text};
            background: {bg};
        }}
        
        #sidebar {{
            width: {self.sidebar_width};
            height: 1fr;
            border-left: solid {border};
            padding: 1 2;
            background: {bg};
        }}
        
        #sidebar-title {{
            color: {text};
            text-style: bold;
            margin-bottom: 1;
        }}
        
        #sidebar-info {{
            height: 1fr;
        }}
        
        Footer {{
            background: {surface};
            color: {muted};
        }}
        
        Header {{
            background: {bg};
            color: {muted};
            text-style: none;
        }}
        
        HeaderTitle {{
            color: {text};
            text-style: none;
        }}
        
        HeaderSubtitle {{
            color: {muted};
            text-style: none;
        }}
        
        HeaderIcon {{
            color: {muted};
        }}
        
        CommandPalette {{
            display: none;
        }}
        
        """

    def compose(self) -> ComposeResult:
        if self.header_enabled:
            yield Header(show_clock=True)

        with Horizontal(id="main"):
            with Vertical(id="content"):
                yield RichLog(id="story-log", wrap=True, highlight=False, markup=False)

                yield Input(
                    placeholder=self.command_config.get(
                        "placeholder", "What do you do?"
                    ),
                    id="command",
                )

            if self.sidebar_enabled:
                with Vertical(id="sidebar"):
                    yield Static(self.game_title, id="sidebar-title")
                    yield Static("", id="sidebar-info")

        if self.footer_enabled:
            yield Footer()

    def on_mount(self) -> None:
        accent = self._theme.get("accent", "#d5a85f")
        secondary = self._theme.get("secondary", "#9ca88e")

        self._write_line("HOLLOW MILE", style=f"bold {accent}")
        self._write_line("A Station That Should Not Exist", style=f"italic {secondary}")
        self._write_line("")
        self._write_line("Type 'help' for available commands.")
        self._write_line("")

        res = self.engine.start()
        self._display_result(res)
        if self.sidebar_enabled:
            self._update_sidebar()

        self.query_one("#command", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        cmd = event.value.strip()
        event.input.value = ""

        if not cmd:
            return

        accent = self._theme.get("accent", "#d5a85f")
        self._write_line(f"\n> {cmd}", style=f"bold {accent}")

        if cmd.lower() in {"quit", "exit"}:
            self.action_quit_game()
            return

        res = self.engine.execute(cmd)
        self._display_result(res)
        if self.sidebar_enabled:
            self._update_sidebar()

    def _write_line(self, content, style: str = ""):
        log = self.query_one("#story-log", RichLog)
        log.write(Text(content, style=style))

    def _display_result(self, res):
        normal = self._theme.get("text", "#b5b5b5")
        error = self._theme.get("error", "#d58b76")
        secondary = self._theme.get("secondary", "#9ca88e")

        style = normal if res.success else error
        self._write_line(res.text, style)

        if res.suggestions:
            self._write_line("")
            self._write_line("Suggested actions: ", style=f"bold {secondary}")

            for sug in res.suggestions:
                self._write_line(f" - {sug}")

    def _update_sidebar(self):
        info = Text()

        accent = self._theme.get("accent", "#d5a85f")
        info.append("LOCATION\n", style=f"bold {accent}")

        room = self.engine.world.curr_room

        if room:
            info.append(f"{room.name}\n")
        else:
            info.append(f"Unknown\n")

        info.append("\nINVENTORY\n", style=f"bold {accent}")

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
        if self.sidebar_enabled:
            self._update_sidebar()

    def action_show_help(self) -> None:
        res = self.engine.execute("help")
        self._display_result(res)

    def action_quit_game(self) -> None:
        self._write_line("Your train remains silent.", style="italic #9ca88e")
        self._write_line("HOLLOW MILE - SESSION ENDED", style="bold #d5a85f")
        self.exit()
