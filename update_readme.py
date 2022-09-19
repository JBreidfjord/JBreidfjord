import json

base_pin = '<a href="https://github.com/{username}/{repo}"><img align="center" src="https://github-readme-stats.vercel.app/api/pin/?username={username}&repo={repo}&theme={theme}" /></a>'
base_stats = "![GitHub stats](https://github-readme-stats.vercel.app/api?username={username}&theme={theme}&include_all_commits=1&count_private=1)]"
base_lang_stats = "![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username={username}&langs_count={count}&theme={theme}&layout=compact)"
base_wakatime = "[![Wakatime Stats](https://github-readme-stats.vercel.app/api/wakatime?username={username}&theme={theme}&langs_count={count}&layout=compact)](https://wakatime.com/@{username})"


def replace_chunk(readme: str, content: str, marker: str) -> str:
    """Replace the chunk of text between two markers with new content"""
    marker = f"<!-- {marker} -->"
    start = readme.find(marker) + len(marker)
    end = readme.find(marker, start)
    return readme[:start] + "\n" + content + "\n" + readme[end:]


def format_pins(pins: list, theme: str) -> str:
    """Format the pinned repositories"""
    return "".join(
        base_pin.format(username=pin["username"], repo=pin["repo"], theme=theme)
        for pin in pins
    )


if __name__ == "__main__":
    with open("README.md", "r") as file:
        readme = file.read()

    with open("content.json", "r") as file:
        json_content = json.load(file)

    theme = json_content["theme"]

    # Update the pinned repositories
    pins: list = json_content["pins"]
    readme = replace_chunk(readme, format_pins(pins, theme), "pins")

    # Update the stats
    stats = base_stats.format(username=json_content["stats"]["username"], theme=theme)
    lang_stats = base_lang_stats.format(
        username=json_content["languages"]["username"],
        count=json_content["languages"]["count"],
        theme=theme,
    )
    wakatime = base_wakatime.format(
        username=json_content["wakatime"]["username"],
        count=json_content["wakatime"]["count"],
        theme=theme,
    )

    stats_chunk = wakatime + "\n" + lang_stats + "\n" + stats

    readme = replace_chunk(readme, stats_chunk, "stats")

    with open("README.md", "w") as file:
        file.write(readme)