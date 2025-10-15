# fairtool_project/tests/test_cli.py

import pytest
from typer.testing import CliRunner
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the main Typer application from your cli.py
from fairtool.cli import app, _find_calc_files #

# Initialize the CliRunner
runner = CliRunner()

# --- Fixtures for common test setup ---

@pytest.fixture
def mock_parse_run_parser():
    """
    Mocks parse_module.run_parser to prevent actual parsing during CLI tests.
    """
    with patch('fairtool.parse.run_parser') as mock:
        yield mock

# --- Tests for _find_calc_files helper function ---

# def test_find_calc_files_single_file(tmp_path):
#     """Test finding a single file."""
#     test_file = tmp_path / "OUTCAR"
#     test_file.touch()
#     files = _find_calc_files(test_file) #
#     assert files == [test_file]

# def test_find_calc_files_directory_with_files(tmp_path):
#     """Test finding files within a directory."""
#     sub_dir = tmp_path / "calc_data"
#     sub_dir.mkdir()
#     file1 = sub_dir / "OUTCAR"
#     file1.touch()
#     file2 = sub_dir / "subdir" / "my_calc.out"
#     file2.parent.mkdir()
#     file2.touch()
#     irrelevant_file = sub_dir / "temp.txt"
#     irrelevant_file.touch()

#     files = _find_calc_files(sub_dir) #
#     # Ensure all found files are Path objects and the list contains expected files
#     assert all(isinstance(f, Path) for f in files)
#     assert file1 in files
#     assert file2 in files
#     assert irrelevant_file not in files # Only OUTCAR and .out files

# def test_find_calc_files_non_existent_path(caplog):
#     """Test handling of a non-existent input path."""
#     non_existent_path = Path("/non/existent/path/to/file.xml")
#     with pytest.raises(SystemExit) as excinfo:
#         _find_calc_files(non_existent_path) #
#     assert excinfo.value.code == 1
#     assert "Error: Input path does not exist" in caplog.text

# def test_find_calc_files_empty_directory(tmp_path, caplog):
#     """Test handling of an empty directory."""
#     empty_dir = tmp_path / "empty_dir"
#     empty_dir.mkdir()
#     files = _find_calc_files(empty_dir) #
#     assert files == []
#     assert "No potential calculation files found" in caplog.text


# # --- Tests for CLI Commands ---

# def test_parse_command_success(mock_parse_run_parser, tmp_path):
#     """
#     Test the 'parse' command with a single file and successful parsing.
#     """
#     input_file = tmp_path / "test_vasp.xml"
#     input_file.write_text("<some_xml_content/>") # Create a dummy input file

#     output_dir = tmp_path / "parsed_output"

#     result = runner.invoke(app, ["parse", str(input_file), "-o", str(output_dir)]) #

#     assert result.exit_code == 0
#     assert "Starting parsing process" in result.stdout
#     assert f"Output will be saved to: {output_dir}" in result.stdout
#     assert f"Parsing file: {input_file}" in result.stdout
#     assert "Parsing finished." in result.stdout
#     mock_parse_run_parser.assert_called_once_with(input_file, output_dir, True)

#     assert output_dir.exists() # Ensure output directory was created

# def test_parse_command_directory_success(mock_parse_run_parser, tmp_path):
#     """
#     Test the 'parse' command with a directory input.
#     """
#     input_dir = tmp_path / "calc_data"
#     input_dir.mkdir()
#     file1 = input_dir / "OUTCAR"
#     file1.touch()
#     file2 = input_dir / "job.out"
#     file2.touch()

#     output_dir = tmp_path / "parsed_output_dir"

#     result = runner.invoke(app, ["parse", str(input_dir), "-o", str(output_dir)]) #

#     assert result.exit_code == 0
#     assert f"Output will be saved to: {output_dir}" in result.stdout
#     assert f"Parsing file: {file1}" in result.stdout
#     assert f"Parsing file: {file2}" in result.stdout
#     assert "Parsing finished." in result.stdout
#     assert mock_parse_run_parser.call_count == 2 # Called for each file
#     mock_parse_run_parser.assert_any_call(file1, output_dir, True)
#     mock_parse_run_parser.assert_any_call(file2, output_dir, True)


# def test_parse_command_force_flag(mock_parse_run_parser, tmp_path):
#     """
#     Test the 'parse' command with --force flag.
#     """
#     input_file = tmp_path / "another_vasp.xml"
#     input_file.write_text("<content/>")
#     output_dir = tmp_path / "forced_output"
#     output_dir.mkdir()

#     # Default force is True, so this tests explicit --force is handled.
#     result = runner.invoke(app, ["parse", str(input_file), "-o", str(output_dir), "--force"]) #

#     assert result.exit_code == 0
#     mock_parse_run_parser.assert_called_once_with(input_file, output_dir, True)

# def test_parse_command_no_force_flag_and_existing_files(mock_parse_run_parser, tmp_path):
#     """
#     Test 'parse' command without --force and existing output files.
#     This should lead to the parser being skipped for existing files within parse_module.
#     The cli should still call parse_module.run_parser, and parse_module handles the skipping.
#     """
#     input_file = tmp_path / "existing_file.xml"
#     input_file.write_text("<content/>")
#     output_dir = tmp_path / "existing_output"
#     output_dir.mkdir()

#     # The parse_module.run_parser itself handles the "no force" logic,
#     # so we still expect it to be called by the CLI.
#     # We can simulate its internal behavior for this test by checking if mock_parse_run_parser
#     # was called with 'force=False'.
#     result = runner.invoke(app, ["parse", str(input_file), "-o", str(output_dir), "--force", "False"]) #

#     assert result.exit_code == 0
#     # The CLI calls `run_parser` with the provided `force` value
#     mock_parse_run_parser.assert_called_once_with(input_file, output_dir, False)


# def test_parse_command_parse_module_failure(mock_parse_run_parser, tmp_path):
#     """
#     Test that the 'parse' command handles exceptions from parse_module.run_parser.
#     """
#     input_file = tmp_path / "bad_file.xml"
#     input_file.write_text("<invalid_content/>")
#     output_dir = tmp_path / "error_output"
#     output_dir.mkdir()

#     # Simulate an exception from parse_module.run_parser
#     mock_parse_run_parser.side_effect = Exception("Simulated parsing error")

#     result = runner.invoke(app, ["parse", str(input_file), "-o", str(output_dir)]) #

#     # The CLI currently logs the error and continues, it does not raise typer.Exit
#     assert result.exit_code == 0 # Or 1 if you choose to exit on first error
#     assert "Failed to parse" in result.stdout
#     assert "Simulated parsing error" in result.stdout
#     mock_parse_run_parser.assert_called_once()


def test_version_command():
    """
    Test the --version/-v flag.
    """
    result = runner.invoke(app, ["--version"]) #
    assert result.exit_code == 0
    assert "FAIR Tool Version:" in result.stdout

    result = runner.invoke(app, ["-v"]) #
    assert result.exit_code == 0
    assert "FAIR Tool Version:" in result.stdout


def test_author(capsys):
    """
    Test if the author information is displayed correctly.
    """
    result = runner.invoke(app, ["about"]) #
    assert result.exit_code == 0
    print ("whole stdout", result.stdout)  # For debugging purposes
    assert "Dr. Ravindra Shinde" in result.stdout

    result = runner.invoke(app, ["about"]) #
    assert result.exit_code == 0
    assert "r.l.shinde@utwente.nl" in result.stdout



def test_about_callback(capsys):
    """
    Test that the about message is displayed on initial call without subcommand.
    This is implicitly tested by `no_args_is_help=True` and `callback=about()`.
    """
    result = runner.invoke(app) # Invoking without arguments should show help and about
    print (result.stdout)
    assert result.exit_code == 0
    assert "Options" in result.stdout
    assert "Commands" in result.stdout
#    assert "Usage: fair [OPTIONS] COMMAND [ARGS]" in result.stdout

# --- Tests for other commands (placeholders, as they are not implemented yet) ---

# def test_analyze_command_placeholder():
#     """
#     Test the 'analyze' command (placeholder for future implementation).
#     """
#     result = runner.invoke(app, ["analyze", "dummy_input.json"]) #
#     assert result.exit_code == 0
#     assert "Starting analysis process" in result.stdout
#     assert "Analysis finished." in result.stdout

# def test_summarize_command_placeholder():
#     """
#     Test the 'summarize' command (placeholder for future implementation).
#     """
#     result = runner.invoke(app, ["summarize", "dummy_input.json"]) #
#     assert result.exit_code == 0
#     assert "Starting summarization process" in result.stdout
#     assert "Summarization finished." in result.stdout

# def test_visualize_command_placeholder():
#     """
#     Test the 'visualize' command (placeholder for future implementation).
#     """
#     result = runner.invoke(app, ["visualize", "dummy_input.json"]) #
#     assert result.exit_code == 0
#     assert "Starting visualization data generation" in result.stdout
#     assert "Visualization data generation finished." in result.stdout

# def test_export_command_placeholder():
#     """
#     Test the 'export' command (placeholder for future implementation).
#     """
#     result = runner.invoke(app, ["export", "dummy_input.json"]) #
#     assert result.exit_code == 0
#     assert "Starting export process" in result.stdout
#     assert "Export finished." in result.stdout
