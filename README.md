# Generate History/Changelog

It should work on MacOS, Linux and Windows with git >= 2.0 installed.

## Usage
```
pip install track_changes
cd <project_root>
track_changes > HISTORY.md
```

## Details
```
NAME
    track_changes - Render Changelog from template

SYNOPSIS
    track_changes <flags>

DESCRIPTION
    Render Changelog from template

FLAGS
    --version=VERSION
        render changelog for which version. Defaults to None, meaning the latest git tag veresion.
    --previous_version=PREVIOUS_VERSION
        render changelog since which verision. Defaults to None, meaning the one before the latest git tag version.
    --out=OUT
```
