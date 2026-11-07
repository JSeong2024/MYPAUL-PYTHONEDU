from pathlib import Path

HERE = Path(__file__).resolve().parent
CHAPTER = HERE.parent
source = CHAPTER / "data" / "orders.csv"

print("Chapter:", CHAPTER.name)
print("Name:", source.name)
print("Suffix:", source.suffix)
print("Exists:", source.is_file())
