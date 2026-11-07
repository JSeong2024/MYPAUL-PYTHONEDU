from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "data" / "notes.txt"
output = ROOT / "output" / "notes_copy.txt"

lines = source.read_text(encoding="utf-8").splitlines()
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("Lines:", len(lines))
print("First:", lines[0])
print("Saved:", output.name)
