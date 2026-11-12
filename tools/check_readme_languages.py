#!/usr/bin/env python3
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
FILES=['README.md', 'README_CN.md', 'README.zh-TW.md', 'README.ja.md', 'README.ko.md']
for name in FILES:
    body=(ROOT/name).read_text()
    visible=re.sub(r"```.*?```", "", body, flags=re.S)
    assert len(re.findall(r"^# ",visible,re.M))==1, name
    assert len(body)>1500, name
    for other in FILES:
        assert f"({other})" in body, (name,other)
    for dest in re.findall(r"\]\(([^)]+)\)",body):
        if "://" in dest or dest.startswith("#"): continue
        assert (ROOT/dest.split("#")[0]).exists(), (name,dest)
    assert "[License: MIT]" not in body
print(f"{len(FILES)} localized guides: structure, language routes and relative links passed")
