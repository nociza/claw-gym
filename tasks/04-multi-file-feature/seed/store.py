"""In-memory note store."""

from __future__ import annotations

from datetime import datetime

from models import Note


class NoteStore:
    def __init__(self) -> None:
        self._notes: dict[int, Note] = {}
        self._next_id: int = 1

    def add(self, title: str, content: str) -> Note:
        """Create and store a new note."""
        note = Note(
            id=self._next_id,
            title=title,
            content=content,
            created_at=datetime.now(),
        )
        self._notes[note.id] = note
        self._next_id += 1
        return note

    def get(self, note_id: int) -> Note | None:
        """Get a note by ID."""
        return self._notes.get(note_id)

    def list_all(self) -> list[Note]:
        """List all notes ordered by creation time."""
        return sorted(self._notes.values(), key=lambda n: n.created_at)

    def delete(self, note_id: int) -> bool:
        """Delete a note. Returns True if found and deleted."""
        if note_id in self._notes:
            del self._notes[note_id]
            return True
        return False
