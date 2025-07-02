# fairtool/parse.py

"""Handles the parsing of calculation files."""

import json
import logging
from pathlib import Path
import subprocess
# from electronic_parsers import auto

log = logging.getLogger(__name__)

def run_parser(input_file: Path, output_dir: Path, force: bool):
    """
    Parses a single calculation file using electronic-parsers.

    Args:
        input_file: Path to the calculation output file.
        output_dir: Directory to save the parsed JSON and Markdown.
        force: Whether to overwrite existing output files.
    """
    # Define output file paths
    base_name = input_file.stem
    json_output_path = output_dir / f"{base_name}_parsed.json"
    md_output_path = output_dir / f"{base_name}_report.md"

    if not force and (json_output_path.exists() or md_output_path.exists()):
        log.warning(f"Output files for {input_file.name} already exist in {output_dir}. Use --force to overwrite.")
        return

    log.info(f"Attempting to parse {input_file.name} ...")

    # The command to run, broken into a list for subprocess
    command = [
        "nomad", "parse",
        "--skip-normalizers",
        "--show-archive",
        "--show-metadata",
        str(input_file)
    ]

    try:
        # We need to import the subprocess module

        # Run the NOMAD parser command
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,  # To get stdout/stderr as strings
            check=True, # To raise CalledProcessError on non-zero exit codes
            encoding='utf-8'
        )

        # The JSON output is in stdout
        raw_json_output = process.stdout
        if not raw_json_output:
            log.warning(f"Parser returned no data for {input_file.name}.")
            return

        # Parse the full JSON output into a Python dictionary
        # The output might contain multiple JSON objects. We need to parse all of them
        # and merge them.
        decoder = json.JSONDecoder()
        pos = 0
        full_data = {}
        raw_json_output = raw_json_output.strip()
        while pos < len(raw_json_output):
            obj, pos = decoder.raw_decode(raw_json_output, pos)
            full_data.update(obj)
            pos = len(raw_json_output[:pos].strip())


        log.debug(f"Parsed data for {input_file.name}: {full_data}")

        # --- Filter for necessary fields ---
        # As requested, we select only a subset of the fields.
        # This part should be customized based on what data is truly needed.
        run = full_data.get("run", {})
        calculation = run[0].get("calculation", {})
        properties = full_data.get("metadata", {})

        results = calculation[0].get("scf_iteration", {})

        log.debug(f"Extracted scf results for {input_file.name}: {results}")

        filtered_data = {
            "domain": full_data.get("metadata", {}).get("domain"),
            # "mainfile": full_data.get("metadata", {}).get("mainfile"),
            # "entry_id": full_data.get("metadata", {}).get("entry_id"),
            # "upload_id": full_data.get("metadata", {}).get("upload_id"),
            # "material": results.get("material"),
            # "method": results.get("method"),
            # "total_energy": properties.get("energy_total"), # Example path
        }
        # Remove keys with None values for a cleaner output
        filtered_data = {k: v for k, v in filtered_data.items() if v is not None}


        # --- Save as JSON ---
        log.debug(f"Saving filtered parsed data to {json_output_path}")
        try:
            with open(json_output_path, 'w', encoding='utf-8') as f:
                json.dump(filtered_data, f, indent=2)
            log.info(f"Successfully saved JSON: {json_output_path.name}")
        except Exception as json_err:
            log.error(f"Failed to save JSON for {input_file.name}: {json_err}")
            if json_output_path.exists():
                json_output_path.unlink()
            raise

    except FileNotFoundError:
        log.error("`nomad` command not found. Is NOMAD installed and in your system's PATH?")
        raise
    except subprocess.CalledProcessError as e:
            raise
