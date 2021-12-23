from pathlib import Path, PurePath

print(Path(__file__).resolve().parent)
print(PurePath.joinpath(Path(__file__).resolve().parent, 'config'))