"""Pipeline for translating enGB.json into Italian, batch by batch.

Subcommands:
  prepare            splits the unique strings into batches in work/chunks/
  check [--out DIR] [CHUNK...]
                     validates the translated batches in work/out/ (or in DIR)
  status             shows how many batches are translated and valid
  merge [OUTPUT]     rebuilds the translated JSON (default: itIT.json)
  pairs CHUNK [START [COUNT]]
                     prints source and translation side by side, from block
                     number START (1-based, default 1), COUNT blocks (default all)

Batch format (input and output), no escaping needed:
  ### u000123
  text, possibly
  spanning several lines
"""

import json
import re
import sys
from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "enGB.json"
WORK = ROOT / "work"
CHUNKS = WORK / "chunks"
OUT = WORK / "out"
UNITS = WORK / "units.json"

CHUNK_WORDS = 8000
HEADER = re.compile(r"^### (u\d{6})$", re.MULTILINE)
CURLY_TAG = re.compile(r"\{[^{}]*\}")
ANGLE_TAG = re.compile(r"<[^<>]+>")
# Tags whose arguments are translatable text: Italian may need to add or drop them
# (gender agreement), so they are left out of the check.
GENDERED_HEADS = frozenset({"mf", "rt_mf", "nc"})


@dataclass(frozen=True, slots=True)
class Problem:
    chunk: str
    unit: str
    message: str


def load_source() -> dict[str, Any]:
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def dump_like_source(data: dict[str, Any]) -> bytes:
    """Serialises with the same format as the original (indent 2, CRLF, UTF-8)."""
    return json.dumps(data, ensure_ascii=False, indent=2).replace("\n", "\r\n").encode()


def needs_translation(text: str) -> bool:
    stripped = CURLY_TAG.sub("", ANGLE_TAG.sub("", text))
    return any(ch.isalpha() for ch in stripped)


def parse_blocks(text: str) -> dict[str, str]:
    parts = HEADER.split(text)
    return {uid: body.strip("\n") for uid, body in zip(parts[1::2], parts[2::2], strict=True)}


def format_blocks(units: dict[str, str]) -> str:
    return "".join(f"### {uid}\n{text}\n\n" for uid, text in units.items())


def tag_signature(text: str) -> Counter[str]:
    sig: Counter[str] = Counter()
    for tag in CURLY_TAG.findall(text):
        if re.split(r"[|}]", tag[1:])[0] not in GENDERED_HEADS:
            sig[tag] += 1
    sig.update(ANGLE_TAG.findall(text))
    return sig


def split_by_words(units: Iterable[tuple[str, str]], limit: int) -> Iterator[dict[str, str]]:
    chunk: dict[str, str] = {}
    words = 0
    for uid, text in units:
        chunk[uid] = text
        words += len(text.split())
        if words >= limit:
            yield chunk
            chunk, words = {}, 0
    if chunk:
        yield chunk


def prepare() -> None:
    texts = list(dict.fromkeys(v["Text"] for v in load_source()["strings"].values()))
    units = {f"u{i:06d}": t.strip() for i, t in enumerate(texts) if needs_translation(t)}
    CHUNKS.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    UNITS.write_text(json.dumps(units, ensure_ascii=False, indent=1), encoding="utf-8")
    count = 0
    for count, chunk in enumerate(split_by_words(units.items(), CHUNK_WORDS), start=1):
        (CHUNKS / f"c{count:03d}.txt").write_text(format_blocks(chunk), encoding="utf-8")
    print(f"{len(units)} strings to translate, {count} batches in {CHUNKS}")


def compare(name: str, source: dict[str, str], translated: dict[str, str]) -> list[Problem]:
    problems = [Problem(name, uid, "missing") for uid in source if uid not in translated]
    problems += [Problem(name, uid, "id not in batch") for uid in translated if uid not in source]
    for uid, en in source.items():
        it = translated.get(uid)
        if it is None:
            continue
        if not it.strip():
            problems.append(Problem(name, uid, "empty"))
            continue
        expected, got = tag_signature(en), tag_signature(it)
        if expected != got:
            diff = (expected - got) + (got - expected)
            problems.append(Problem(name, uid, f"different tags: {dict(diff)}"))
    return problems


def check_chunk(name: str, out_dir: Path = OUT) -> list[Problem]:
    out_path = out_dir / f"{name}.txt"
    if not out_path.exists():
        return [Problem(name, "-", "missing output")]
    source = parse_blocks((CHUNKS / f"{name}.txt").read_text(encoding="utf-8"))
    return compare(name, source, parse_blocks(out_path.read_text(encoding="utf-8")))


def chunk_names() -> list[str]:
    return sorted(p.stem for p in CHUNKS.glob("c*.txt"))


def check(args: list[str]) -> int:
    out_dir = OUT
    if args[:1] == ["--out"]:
        if len(args) < 2:
            raise ValueError("--out requires a directory")
        out_dir, args = Path(args[1]), args[2:]
    problems = [p for name in args or chunk_names() for p in check_chunk(name, out_dir)]
    for p in problems:
        print(f"{p.chunk} {p.unit}: {p.message}")
    print(f"{len(problems)} problems")
    return 1 if problems else 0


def status() -> None:
    names = chunk_names()
    done = [n for n in names if (OUT / f"{n}.txt").exists()]
    invalid = [n for n in done if check_chunk(n)]
    print(f"batches: {len(names)}  translated: {len(done)}  valid: {len(done) - len(invalid)}")
    if invalid:
        print("with problems:", " ".join(invalid))


def valid_translations() -> dict[str, str]:
    translations: dict[str, str] = {}
    for name in chunk_names():
        out_path = OUT / f"{name}.txt"
        if out_path.exists() and not check_chunk(name):
            translations |= parse_blocks(out_path.read_text(encoding="utf-8"))
    return translations


def merge(output: Path) -> None:
    data = load_source()
    units: dict[str, str] = json.loads(UNITS.read_text(encoding="utf-8"))
    uid_by_text = {text: uid for uid, text in units.items()}
    translations = valid_translations()
    applied = 0
    for entry in data["strings"].values():
        original = entry["Text"]
        core = original.strip()
        translated = translations.get(uid_by_text.get(core, ""))
        if translated is None:
            continue
        # Keep the original's leading/trailing whitespace, which the batches strip.
        start = original.index(core)
        entry["Text"] = original[:start] + translated + original[start + len(core) :]
        applied += 1
    output.write_bytes(dump_like_source(data))
    print(f"{applied}/{len(data['strings'])} strings translated -> {output}")


def pairs(args: list[str]) -> None:
    if not 1 <= len(args) <= 3:
        raise ValueError("usage: pairs CHUNK [START [COUNT]]")
    name = args[0]
    start = int(args[1]) if len(args) > 1 else 1
    source = parse_blocks((CHUNKS / f"{name}.txt").read_text(encoding="utf-8"))
    translated = parse_blocks((OUT / f"{name}.txt").read_text(encoding="utf-8"))
    uids = list(source)[start - 1 :]
    if len(args) > 2:
        uids = uids[: int(args[2])]
    for number, uid in enumerate(uids, start=start):
        it = translated.get(uid, "<missing>")
        print(f"### {uid} [{number}/{len(source)}]\nEN: {source[uid]}\nIT: {it}\n")


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    command, args = argv[0], argv[1:]
    if command == "prepare":
        prepare()
    elif command == "check":
        return check(args)
    elif command == "status":
        status()
    elif command == "merge":
        merge(ROOT / (args[0] if args else "itIT.json"))
    elif command == "pairs":
        pairs(args)
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
