import json
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from typer.testing import CliRunner

from fairtool.cli import app, parse as parse_cmd
from fairtool.parse import run_parser

runner = CliRunner()


def make_nomad_process(stdout_text: str):
    proc = MagicMock()
    proc.stdout = stdout_text
    return proc


def test_run_parser_writes_fair_parse_time(tmp_path, monkeypatch):
    # Create a dummy input file
    # input_file = tmp_path / "input.out"
    input_file = tmp_path / "vasprun.xml"
    input_file.write_text("dummy content")

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    # This mock represents the *final merged* object after the `while` loop in `run_parser`.
    # The real `nomad parse` outputs two JSONs. The first has top-level keys
    # like 'n_quantities'. The second has 'run', 'metadata', etc.
    # The `update` call merges them.
    fake_nomad_json = json.dumps({
        # --- Keys from the *first* JSON object (metadata) ---
        "entry_name": "Test Entry",
        "entry_type": "Test Type",
        "domain": "dft",
        "optimade": {"elements": ["Ag", "Cl", "Cs", "Hg"]},
        "n_quantities": 42,
        "quantities": ["some_quantity"],
        "sections": ["some_section"],
        "section_defs": ["some_def"],

        # --- Keys from the *second* JSON object (archive) ---
        "run": [
            {
                "program": {"name": "VASP", "version": "6.3.0"},
                "method": [
                    {"dft": {"xc_functional": {"name": "GGA_C_PBE+GGA_X_PBE"}}}
                ],
                "system": [
                    {"type": "bulk", "chemical_composition_hill": "AgCl6Cs2Hg"}
                ],
                "calculation": [
                    {"energy": {"total": {"value": -4.8e-18}}}
                ]
            }
        ],
        "metadata": {
            # This metadata block from the *archive* does NOT contain
            # n_quantities, quantities, etc. The parser will now
            # safely .pop() them, preventing the KeyError.
            "entry_name": "Test Entry", # This gets overwritten by the first JSON
            "entry_type": "Test Type",
        },
        "results": {
            "material": {
                "elements": ["Ag", "Cl", "Cs", "Hg"],
                "chemical_formula_hill": "AgCl6Cs2Hg"
            },
            "method": {
                "method_name": "DFT",
                "simulation": {"program_name": "VASP"}
            },
            "properties": {}
        }
    })

    fake_proc = make_nomad_process(fake_nomad_json)
    monkeypatch.setattr("subprocess.run", lambda *a, **k: fake_proc)

    run_parser(input_file, output_dir, force=True)

    json_file = output_dir / f"fair_parsed_{input_file.stem}.json"
    assert json_file.exists()

    data = json.loads(json_file.read_text(encoding='utf-8'))
    assert "metadata" in data
    assert "fair_parse_time" in data["metadata"]
    # We check for a key from the *archive* metadata block
    assert "entry_type" in data["metadata"]
    # We check that top-level keys were successfully removed
    assert "n_quantities" not in data
    assert "optimade" not in data
    # We check that keys were safely removed from the archive metadata
    assert "n_quantities" not in data["metadata"]

    # fair_parse_time should be approximately the input file mtime
    mtime = input_file.stat().st_mtime
    assert abs(data["metadata"]["fair_parse_time"] - mtime) < 2.0


@patch('fairtool.parse.run_parser')
def test_cli_skips_when_unchanged(mock_run_parser, tmp_path):
    # Create a dummy input file
    #input_file = tmp_path / "input2.out"
    input_file = tmp_path / "vasprun2.xml"
    input_file.write_text("content")

    output_dir = tmp_path / "out2"
    output_dir.mkdir()

    # Create an existing parsed JSON with fair_parse_time >= file mtime
    json_file = output_dir / f"fair_parsed_{input_file.stem}.json"
    # ensure file mtime is older than saved fair_parse_time
    file_mtime = input_file.stat().st_mtime
    json_content = {"metadata": {"fair_parse_time": file_mtime + 10}}
    json_file.write_text(json.dumps(json_content), encoding='utf-8')

    # Call the parse command function directly to avoid CLI boolean parsing issues
    parse_cmd(input_file, output_dir, force=False)
    # Since parse_cmd writes to stdout via logging, we check that run_parser was not called
    mock_run_parser.assert_not_called()


@patch('fairtool.parse.run_parser')
def test_cli_runs_when_missing_fair_parse_time(mock_run_parser, tmp_path):
    # Create a dummy input file
    #input_file = tmp_path / "input3.out"
    input_file = tmp_path / "vasprun3.xml"
    input_file.write_text("content")

    output_dir = tmp_path / "out3"
    output_dir.mkdir()

    # Create an existing parsed JSON without fair_parse_time
    json_file = output_dir / f"fair_parsed_{input_file.stem}.json"
    json_content = {"metadata": {"some": "value"}}
    json_file.write_text(json.dumps(json_content), encoding='utf-8')

    # Call the parse command function directly to avoid CLI boolean parsing issues
    parse_cmd(input_file, output_dir, force=False)
    # Should call the parser since fair_parse_time is missing
    mock_run_parser.assert_called_once_with(input_file, output_dir, False)
