def html_page(title: str, body_content: str, depth: int = 0) -> str:
    """A modern HTML wrapper with dark mode styling."""
    home_href = "./" + ("../" * depth) + "index.html"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>{title}</title>
    <style>
        :root {{
            --bg-primary: #1a1b1e;
            --bg-secondary: #2c2e33;
            --text-primary: #e4e5e7;
            --text-secondary: #a1a3a7;
            --accent: #4f6df5;
            --accent-hover: #6981f7;
            --border: #404347;
            --success: #48a565;
            --card-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        header {{
            background: var(--bg-secondary);
            padding: 1rem 2rem;
            margin-bottom: 2rem;
            border-radius: 8px;
            box-shadow: var(--card-shadow);
        }}

        nav a {{
            color: var(--accent);
            text-decoration: none;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            transition: all 0.2s;
        }}

        nav a:hover {{
            background: var(--accent);
            color: var(--bg-primary);
        }}

        h1, h2, h3 {{
            color: var (--text-primary);
            margin: 1.5rem 0 1rem 0;
        }}

        h1 {{
            font-size: 2.2rem;
            border-bottom: 2px solid var(--border);
            padding-bottom: 0.5rem;
        }}

        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 1rem 0;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: var(--card-shadow);
        }}

        th, td {{
            padding: 1rem;
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border);
        }}

        th {{
            background: var(--bg-secondary);
            color: var(--accent);
            font-weight: 600;
            text-align: left;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        .facts {{
            background: var(--bg-secondary);
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: var(--card-shadow);
        }}

        .facts li {{
            margin: 0.8rem 0;
            list-style-type: none;
        }}

        .facts li::before {{
            content: "•";
            color: var(--accent);
            font-weight: bold;
            margin-right: 0.5rem;
        }}

        .facts ul {{
            margin-left: 1.5rem;
            border-left: 2px solid var(--border);
            padding-left: 1rem;
        }}

        a {{
            color: var(--accent);
            text-decoration: none;
            transition: color 0.2s;
        }}

        a:hover {{
            color: var(--accent-hover);
        }}

        .panel {{
            background: var(--bg-secondary);
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: var(--card-shadow);
        }}

        .info-panel {{
            background: var(--bg-secondary);
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: var(--card-shadow);
        }}

        .info-content {{
            display: flex;
            gap: 2rem;
            align-items: start;
            margin-top: 1rem;
        }}

        .info-table {{
            flex: 1;
        }}

        @media (max-width: 768px) {{
            .info-content {{
                flex-direction: column;
            }}
        }}

        img {{
            border-radius: 8px;
            box-shadow: var(--card-shadow);
        }}

        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1rem 0;
        }}

        .gallery img {{
            width: 100%;
            height: auto;
            object-fit: cover;
            transition: transform 0.2s;
        }}

        .gallery img:hover {{
            transform: scale(1.05);
        }}

        .info-card {{
            background: var(--bg-secondary);
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
            box-shadow: var(--card-shadow);
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 1rem;
            }}

            header {{
                padding: 1rem;
            }}

            table {{
                display: block;
                overflow-x: auto;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="{home_href}">← Home</a>
        </nav>
    </header>
    <main>
        {body_content}
    </main>
</body>
</html>
"""
