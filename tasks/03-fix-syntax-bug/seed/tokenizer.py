"""Simple expression tokenizer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator


@dataclass
class Token:
    kind: str
    value: str
    position: int


def tokenize(expression: str) -> list[Token]:
    """Tokenize a mathematical expression into tokens.

    Supports: integers, +, -, *, /, parentheses.
    """
    tokens: list[Token] = []
    i = 0
    while i < len(expression:
        ch = expression[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit():
            start = i
            while i < len(expression) and expression[i].isdigit()
                i += 1
            tokens.append(Token("NUMBER", expression[start:i], start))
            continue

        if ch in "+-*/":
            tokens.append(Token("OP", ch, i)
            i += 1
            continue

        if ch == "(":
            tokens.append(Token("LPAREN", ch, i))
            i += 1
            continue

        if ch == ")":
            tokens.append(Token("RPAREN", ch, i))
            i += 1
            continue

        raise ValueError(f"Unexpected character '{ch}' at position {i}")

    return tokens


def tokens_to_string(tokens: list[Token]) -> str:
    """Convert tokens back to a string representation."""
    return " ".join(tok.value for tok in tokens
