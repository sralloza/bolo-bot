from pathlib import Path
from enum import Enum
from typing import List
from click.exceptions import ClickException

import typer
from pydantic import BaseModel, parse_file_as
from telegram import Bot


class BroadcastChannel(BaseModel):
    name: str
    chat_id: int


app = typer.Typer(add_completion=False)
helps = {
    "to": "broadcast receiver",
    "message": "broadcast message",
    "clipboard": "take the message from the clipboard",
    "yes": "skip message confirmation",
    "enable_wp": "enable web page preview",
}
mapper_path = (
    Path(__file__).parent.with_name("app") / "db/files/broadcast_channels.json"
)
mapper = parse_file_as(List[BroadcastChannel], mapper_path)
valid_names = [x.name for x in mapper]
BroadCastReceiver = Enum("BroadCastReceiver", {x: x for x in valid_names})


def get_chat_id_from_receiver(name: BroadCastReceiver):
    for channel in mapper:
        if channel.name == name.name:
            return channel.chat_id
    raise ClickException(f"Invalid name: {name!r}")


@app.command()
def send_message(
    to: BroadCastReceiver = typer.Argument(..., case_sensitive=False, help=helps["to"]),
    message: str = typer.Option(None, "--message", "-m", help=helps["message"]),
    clipboard: bool = typer.Option(False, "--clipboard", "-c", help=helps["clipboard"]),
    yes: bool = typer.Option(False, "--yes", "-y", help=helps["yes"]),
    enable_web_page_preview: bool = typer.Option(False, help=helps["enable_wp"]),
):
    from app.core.bot import create_updater

    if message is None:
        if clipboard:
            import pyperclip

            try:
                message = pyperclip.paste()  # type:ignore
            except pyperclip.PyperclipException:
                raise ClickException("pyperclip not supported")
        else:
            message = typer.edit("")

        if not message:
            raise typer.Abort()

    # typer.secho(f"Message length: {len(message)}")

    n = max([len(x) for x in message.splitlines()])
    if n > typer.get_terminal_size()[0]:
        n = typer.get_terminal_size()[0]

    line = "-" * n
    if not yes:
        typer.confirm(
            f"\n{line}\n{message}\n{line}\nConfirm message to {to.name!r}?", abort=True
        )

    chat_id = get_chat_id_from_receiver(to)

    bot: Bot = create_updater().bot
    bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode="markdown",
        disable_web_page_preview=not enable_web_page_preview,
    )
    typer.secho("Done", fg="bright_green")


if __name__ == "__main__":
    app()
