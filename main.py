"""Fortune Cookie Funnies for Engineers — print the one-line fortune."""

from pathlib import Path

ENTRY_PATH = Path(__file__).with_name("entry.txt")
MIN_CHARS = 1
MAX_CHARS = 120


def load_fortune() -> str:
    text = ENTRY_PATH.read_text(encoding="utf-8")
    lines = [part for part in text.splitlines() if part.strip()]
    if len(lines) != 1:
        raise ValueError(f"entry.txt must hold exactly one line, found {len(lines)}")
    line = lines[0].strip()
    if len(line) < MIN_CHARS:
        raise ValueError("entry.txt is empty")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in line):
        raise ValueError("fortune holds a control character")
    if len(line) > MAX_CHARS:
        raise ValueError(f"fortune is {len(line)} chars, over the 120 limit")
    return line


def publish_fortune(line: str) -> None:
    """Write the validated line to the harness artifact path as well.

    The program/v1 harness reads the entry from /output/entry.txt, so
    mirror the printed line there. Best effort only: if the directory
    cannot be created (for example on a read-only run), the printed
    line on stdout is still the entry.
    """
    try:
        output_path = Path("/output/entry.txt")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(line + "\n", encoding="utf-8")
    except OSError:
        pass


def main() -> None:
    line = load_fortune()
    publish_fortune(line)
    print(line)


if __name__ == "__main__":
    main()
