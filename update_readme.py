import json

base_pin = "<a href='https://github.com/{username}/{repo}'><img align='center' src='https://github-readme-stats.vercel.app/api/pin/?username={username}&repo={repo}&theme={theme}&border_color=30363d' /></a>"
base_stats = "<img align='center' src='https://github-readme-stats.vercel.app/api?username={username}&theme={theme}&include_all_commits=1&count_private=1&border_color=30363d&hide_rank=1' />"
base_lang_stats = "<img align='center' height='152' src='https://github-readme-stats.vercel.app/api/top-langs/?username={username}&langs_count={count}&theme={theme}&layout=compact&border_color=30363d' />"
base_wakatime = "<a href='https://wakatime.com/@{username}'><img align='center' height='152' src='https://github-readme-stats.vercel.app/api/wakatime?username={username}&theme={theme}&langs_count={count}&layout=compact&border_color=30363d' /></a>"


def replace_chunk(readme: str, content: str, marker: str) -> str:
    """Replace the chunk of text between two markers with new content"""
    marker = f"<!-- {marker} -->"
    start = readme.find(marker) + len(marker)
    end = readme.find(marker, start)
    return readme[:start] + "\n" + content + "\n" + readme[end:]


if __name__ == "__main__":
    with open("README.md", "r") as file:
        readme = file.read()

    with open("content.json", "r") as file:
        json_content = json.load(file)

    theme = json_content["theme"]

    # Update the pinned repositories
    if json_content["pins"]["enabled"]:
        pins: list = json_content["pins"]["content"]
        joined_pins = "".join(
            base_pin.format(username=pin["username"], repo=pin["repo"], theme=theme)
            for pin in pins
        )
        pins_chunk = "<div>" + joined_pins + "</div>"
        readme = replace_chunk(readme, pins_chunk, "pins")
    else:
        readme = replace_chunk(readme, "", "pins")

    # Update the stats
    stats = base_stats.format(username=json_content["stats"]["username"], theme=theme) if json_content["stats"]["enabled"] else ""
    lang_stats = base_lang_stats.format(
        username=json_content["languages"]["username"],
        count=json_content["languages"]["count"],
        theme=theme,
    ) if json_content["languages"]["enabled"] else ""
    wakatime = base_wakatime.format(
        username=json_content["wakatime"]["username"],
        count=json_content["wakatime"]["count"],
        theme=theme,
    ) if json_content["wakatime"]["enabled"] else ""

    stats_chunk = "<div>" + wakatime + lang_stats + "</div>" + stats
    readme = replace_chunk(readme, stats_chunk, "stats")

    with open("README.md", "w") as file:
        file.write(readme)
