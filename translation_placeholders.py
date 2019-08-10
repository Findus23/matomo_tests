import json
import re

from config import matomo_path

lang_dirs = [matomo_path / "lang"]

pluginspath = matomo_path / "plugins"

regex = re.compile(r"%[sducoxXbgGeEfF]")
typo_regex = re.compile(r"%%[sducoxXbgGeEfF]")
fail = False
for plugindir in pluginspath.iterdir():
    if not plugindir.is_dir():
        continue
    if "UptimeRobotMonitor" in str(plugindir):
        continue
    langdir = plugindir / "lang"
    if langdir.exists():
        lang_dirs.append(langdir)

for langdir in lang_dirs:
    with open(langdir / "en.json") as f:
        data = json.load(f)
    placeholders = {}
    master_translations = list(data.values())[0]
    for key, translation in master_translations.items():
        typos = typo_regex.findall(translation)
        if typos:
            print(typos)
        num_placeholders = len(regex.findall(translation))
        placeholders[key] = num_placeholders

    for transfile in langdir.glob("*.json"):
        if transfile == langdir / "en.json":
            continue
        lang = transfile.stem
        with open(transfile) as f:
            data = json.load(f)
        translations = list(data.values())[0]
        for key, translation in translations.items():
            typos = typo_regex.findall(translation)
            if typos:
                print(transfile)
                print(typos, translation)
                print()
                fail = True
            num_placeholders = len(regex.findall(translation))
            try:
                if placeholders[key] != num_placeholders:
                    print(transfile)
                    print(placeholders[key], num_placeholders)
                    print(master_translations[key])
                    print(translations[key])
                    print()
                    fail = True
            except KeyError:
                print(transfile)
                print(f"Key '{key}' is only in {lang}")
                print()
                fail = True

if fail:
    exit(1)
