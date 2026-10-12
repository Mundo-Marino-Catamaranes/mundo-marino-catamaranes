"""Render the public README from the existing root company.json and template."""
import argparse
import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).resolve().parents[1]

def render() -> str:
    data = json.loads((ROOT / "company.json").read_text(encoding="utf-8"))
    env = Environment(loader=FileSystemLoader(ROOT / "templates"),
                      undefined=StrictUndefined, autoescape=False,
                      keep_trailing_newline=True)
    return env.get_template("README_template.md").render(**data)

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    out = ROOT / "README.md"
    if args.check:
        if not out.exists() or out.read_text(encoding="utf-8") != expected:
            raise SystemExit("README drift: run python scripts/generate_readme.py")
        print("README matches company.json and its template.")
    else:
        out.write_text(expected, encoding="utf-8")
        print("README generated.")

if __name__ == "__main__":
    main()
