import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "company.json"
TPL_DIR = ROOT / "templates"
TPL_NAME = "README_template.md"
OUT = ROOT / "README.md"

def main():
    with DATA.open(encoding="utf-8") as f:
        data = json.load(f)

    env = Environment(
        loader=FileSystemLoader(str(TPL_DIR)),
        autoescape=select_autoescape(disabled_extensions=("md",)),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    tpl = env.get_template(TPL_NAME)
    rendered = tpl.render(**data)

    OUT.write_text(rendered, encoding="utf-8")
    print(f"README generado -> {OUT}")

if __name__ == "__main__":
    main()
