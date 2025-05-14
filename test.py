import sys
import json
import logging
from datetime import datetime, timezone
import click
import os
from nomad.client import parse
from nomad.utils import configure_logging
from nomad.datamodel import EntryArchive
from electronicparsers.vasp import VASPParser

configure_logging(console_log_level=logging.DEBUG)

archive = EntryArchive()
VASPParser().parse(sys.argv[1], archive, logging)
archive_dict = archive.m_to_dict()


program = archive_dict['run'][0]['program']

# Extract values with defaults
name = program.get("name", "Unknown Program")
version = program.get("version", "Unknown Version")
timestamp = program.get("compilation_datetime", None)

if isinstance(timestamp, (int, float)):
    compiled_dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    compiled_str = compiled_dt.strftime("%B %d, %Y at %H:%M UTC")
    timestamp_str = f"{compiled_str} (timestamp `{timestamp}`)"
else:
    timestamp_str = "an unknown time"

# Create narrative Markdown
markdown = f"""## Program Information

The calculation was performed using **{name}**, version
`{version}`, a widely used plane-wave DFT code.

The program was compiled on **{timestamp_str}**. This metadata helps trace the exact binary and compilation setup used in the simulation, supporting reproducibility.
"""

# Save to file
with open("run_program_section.md", "w") as f:
    f.write(markdown)

print("Narrative-style program information saved to 'run_program_section.md'")

# Save the archive to a JSON file
with open("archive.json", "w") as f:
    json.dump(archive_dict, f, indent=2)
print("Archive data saved to 'archive.json'")
# Save the archive to a JSON file with metadata
with open("archive_with_meta.json", "w") as f:
    json.dump(archive.m_to_dict(with_meta=True), f, indent=2)
print("Archive data with metadata saved to 'archive_with_meta.json'")