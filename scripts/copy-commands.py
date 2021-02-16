import re
from pathlib import Path
from typing import List

import typer
from telegram import BotCommand

app = typer.Typer(add_completion=False, help="Bot's commands manager")


def get_commands() -> List[BotCommand]:
    commands_path = Path(__file__).absolute().parent.with_name("commands.md")
    commands_info = commands_path.read_text("utf8")

    commands = []
    for line in commands_info.splitlines():
        if line.strip().startswith("-"):
            line = re.sub(r"- \/([\w]+)", r"\1", line).replace("\\_", "_")
            command, description = re.split(" - ", line, maxsplit=1)
            commands.append(BotCommand(command, description))

    return commands


@app.command("copy")
def copy_commands():
    """Copies the command in a format @BotFather understands."""
    import pyperclip

    commands = get_commands()
    result = "\n".join([f"{x.command} - {x.description}" for x in commands])
    pyperclip.copy(result)
    typer.secho("Done", fg="bright_green")


@app.command("update")
def update_commands():
    """Updates the bot's commands via Telegram API."""
    from app.core.bot import create_updater

    bot = create_updater().bot
    commands = get_commands()
    bot.set_my_commands(commands)
    typer.secho("Done", fg="bright_green")


if __name__ == "__main__":
    app()
