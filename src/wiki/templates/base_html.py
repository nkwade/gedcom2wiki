def html_page(title: str, body_content: str, depth: int = 0) -> str:
    """A basic HTML wrapper with correct relative path adjustments."""
    home_href = "./" + ("../" * depth) + "index.html"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>{title}</title>
    <style>
        body {{
            font-family: sans-serif;
            margin: 2em;
        }}
        header {{
            margin-bottom: 2em;
        }}
        nav a {{
            margin-right: 1em;
        }}
        h1, h2, h3 {{
            font-family: sans-serif;
        }}
        table {{
            border-collapse: collapse;
            margin: 1em 0;
        }}
        table, th, td {{
            border: 1px solid #ccc;
            padding: 0.5em;
        }}
        .facts {{
            margin-top: 1em;
        }}
        .facts li {{
            margin-bottom: 0.5em;
        }}
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="{home_href}">Home</a>
        </nav>
    </header>
    {body_content}
</body>
</html>
"""
