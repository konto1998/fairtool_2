import sys
import json
import logging
from nomad.client import parse
from nomad.utils import configure_logging
from nomad.datamodel import EntryArchive
from electronicparsers.vasp import VASPParser

configure_logging(console_log_level=logging.DEBUG)

archive = EntryArchive()
VASPParser().parse(sys.argv[1], archive, logging)
archive_dict = archive.m_to_dict()


def dict_to_markdown(d, level=1, path=""):
    """Recursively walk through the dict and output a markdown breakdown."""
    md = ""
    indent = "  " * (level - 1)

    if isinstance(d, dict):
        for key, value in d.items():
            full_path = f"{path}.{key}" if path else key
            if isinstance(value, dict):
                md += f"{indent}- **{key}** (dict)\n"
                md += dict_to_markdown(value, level + 1, full_path)
            elif isinstance(value, list):
                md += f"{indent}- **{key}** (list[{len(value)}])\n"
                # Optionally explore the first item if it's a dict
                if value and isinstance(value[0], dict):
                    md += dict_to_markdown(value[0], level + 1, f"{full_path}[0]")
            else:
                # Show sample value if it's simple
                sample = str(value)
                if len(sample) > 60:
                    sample = sample[:57] + "..."
                md += f"{indent}- **{key}**: `{sample}`\n"
    elif isinstance(d, list):
        md += f"{indent}- list[{len(d)}]\n"
        if d and isinstance(d[0], dict):
            md += dict_to_markdown(d[0], level + 1, path + "[0]")
    else:
        sample = str(d)
        if len(sample) > 60:
            sample = sample[:57] + "..."
        md += f"{indent}- `{sample}`\n"

    return md


# Generate Markdown content
markdown_output = "# NOMAD Archive Structure\n\n"
markdown_output += dict_to_markdown(archive_dict)

# Save to file
with open("archive_structure.md", "w") as f:
    f.write(markdown_output)

print("Saved structured archive breakdown to 'archive_structure.md'")
