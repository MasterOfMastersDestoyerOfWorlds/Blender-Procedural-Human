import runpy
from pathlib import Path


def main():
    script = Path(__file__).resolve().parent.parent / "ixdar-tickets" / "generate_board.py"
    runpy.run_path(str(script), run_name="__main__")
