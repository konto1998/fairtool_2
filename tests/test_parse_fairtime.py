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
    input_file = tmp_path / "input.out"
    input_file.write_text("dummy content")

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    # Prepare a fake nomad JSON output that contains expected fields
    fake_nomad_json = json.dumps({
        "results": {
            "method": {"simulation": {"program_version": "1.0", "program_name": "prog", "precision": {"native_tier": "tier", "basis_set": "bz", "xc_functional_names": ["xc1", "xc2"]}}, "method_name": "m", "workflow_name": "w"},
            "material": {"topology": [
                {"label": "original", "cell": {"a": 1, "b": 1, "c": 1, "alpha": 1, "beta": 1, "gamma": 1, "volume": 1, "atomic_density": 1, "mass_density": 1}, "description": "d", "chemical_formula_hill": "H2O", "elements": ["H","O"], "n_atoms": 3},
                {"label": "primitive cell", "cell": {"a": 1, "b": 1, "c": 1, "alpha": 1, "beta": 1, "gamma": 1, "volume": 1, "atomic_density": 1, "mass_density": 1}, "description": "d2", "chemical_formula_hill": "H2O", "elements": ["H","O"], "n_atoms": 3, "symmetry": {"crystal_system": "c"}}
            ]}
        },
        "run": [{"calculation": [{"scf_iteration": []}]}],
        "metadata": {"entry_type": "type", "entry_name": "name"}
    })

    fake_proc = make_nomad_process(fake_nomad_json)
    monkeypatch.setattr("subprocess.run", lambda *a, **k: fake_proc)

    run_parser(input_file, output_dir, force=True)

    json_file = output_dir / f"fair_parsed_{input_file.stem}.json"
    assert json_file.exists()

    data = json.loads(json_file.read_text(encoding='utf-8'))
    assert "metadata" in data
    assert "fair_parse_time" in data["metadata"]

    # fair_parse_time should be approximately the input file mtime
    mtime = input_file.stat().st_mtime
    assert abs(data["metadata"]["fair_parse_time"] - mtime) < 2.0


@patch('fairtool.parse.run_parser')
def test_cli_skips_when_unchanged(mock_run_parser, tmp_path):
    # Create a dummy input file
    input_file = tmp_path / "input2.out"
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
    input_file = tmp_path / "input3.out"
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
