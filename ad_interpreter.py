import sys
import re
from pathlib import Path
from html import escape

AD_PATTERN = re.compile(
    r'<<AD>>==([^\s(]+)\(([^)]*)\)"([^"]+)"'
)

def create_ad(url, name, file):
    extension = Path(file).suffix.lower()

    if extension in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"]:
        media = f'<img src="{escape(file)}" alt="" style="max-width:100%; cursor:pointer;">'

    elif extension in [".mp4", ".webm", ".ogg"]:
        media = f'<video src="{escape(file)}" controls autoplay muted loop style="max-width:100%; cursor:pointer;"></video>'

    else:
        return ""

    return f'''
<div data-ad="true" style="display:inline-block;">
    <a href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer">
        {media}
    </a>
</div>
'''

def interpret(html):
    found = False

    def replace(match):
        nonlocal found
        found = True

        url = match.group(1)
        name = match.group(2)
        file = match.group(3)

        return create_ad(url, name, file)

    result = AD_PATTERN.sub(replace, html)

    return result, found

def main():
    if len(sys.argv) != 2:
        print("  ")
        return

    source = Path(sys.argv[1])

    if not source.exists():
        print(" ")
        return

    if source.suffix.lower() != ".html":
        print(" ")
        return

    html = source.read_text(encoding="utf-8")

    result, found = interpret(html)

    if not found:
        print(" ")
        return

    output = source.with_name(source.stem + "_ad.html")
    output.write_text(result, encoding="utf-8")

    print(" ")
    print(f" ")

if __name__ == "__main__":
    main()