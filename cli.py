from datetime import datetime
import json
from typing import List, Optional
import typer
from dataclasses import dataclass

from storage.local_storage import LocalStorage
from types_ import BinaryEmailChunkHeader, EmailChunk


@dataclass
class InboxMessage:
    id: str
    sender: str
    subject: str
    message: str
    received: datetime
    last_read: datetime
    parts: List[EmailChunk]


@dataclass
class OutboxMessage:
    recipient: str
    subject: str
    message: str
    id: str
    sent: datetime


storage = LocalStorage()

chunks = ([EmailChunk(BinaryEmailChunkHeader(x['header']),x['sender_or_recipient'],x['subject'],x['message']) for x in storage.read_file("chunks.json")])

inbox_messages = (
    [InboxMessage(**x) for x in json.loads(storage.read_file("inbox.json"))]
    if storage.exists("inbox.json")
    else []
)
outbox_messages = (
    [OutboxMessage(**x) for x in json.loads(storage.read_file("outbox.json"))]
    if storage.exists("outbox.json")
    else []
)

app = typer.Typer()


def main(name: str):
    typer.echo(f"Hello {name}")


def _read_email(msg: InboxMessage):
    typer.echo(f"""From: {msg.sender}
Subject: {msg.subject}

{msg.message}
""")
    msg.last_read = datetime.now()
    storage.write_file("inbox.json", json.dumps([x.__dict__ for x in inbox_messages]))


@app.command()
def check():
    pass


@app.command()
def inbox():
    ix = 0
    for msg in sorted(inbox_messages,key=lambda x: x.received)[::-1]:
        typer.echo(f"""
[{ix}] {msg.sender} | {msg.received} | {msg.subject}
""")
        ix += 1


@app.command()
def read(ordinal: int):
    if len(inbox_messages) <= ordinal:
        typer.echo(f"Email {ordinal} not found")
    else:
        _read_email(inbox_messages[ordinal])


@app.command()
def outbox():
    typer.echo(outbox_messages)

@app.command()
def send(recipient: str, subject: str, message: str):
    pass


if __name__ == "__main__":
    app()
