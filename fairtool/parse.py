# fairtool/parse.py

"""Handles the parsing of calculation files."""

import json
import logging
from pathlib import Path
import subprocess
# from electronic_parsers import auto
ELEMENTARY_CHARGE_VALUE = 1.602176634e-19  # Elementary charge in Coulombs, used for energy conversion if needed


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


        # log.info(f"Parsed data for {input_file.name}: {full_data}")

        # --- Filter for necessary fields ---
        # As requested, we select only a subset of the fields.
        # This part should be customized based on what data is truly needed.
        run_data = full_data.get("run", {})
        # calculation = run[0].get("calculation", {})
        # properties = full_data.get("metadata", {})
        scf_iterations_data = []
        total_energies = []

        # Assuming 'run' is a list and 'calculation' is a list within each run entry
        # and 'scf_iteration' is a list within the first calculation entry
        if run_data and isinstance(run_data, list):
            for run_entry in run_data:
                calculation_data = run_entry.get("calculation", [])
                if calculation_data and isinstance(calculation_data, list):
                    # We are interested in the 'scf_iteration' from the *first* calculation entry
                    # If there can be multiple calculations and you need all scf_iterations,
                    # you'll need to loop through calculation_data as well.
                    # For now, let's target the first one as per your log.
                    first_calculation = calculation_data[0] if calculation_data else {}
                    scf_iterations_data = first_calculation.get("scf_iteration", [])
                    if scf_iterations_data:
                        break # Found scf_iteration, no need to check other runs

        log.debug(f"Extracted scf results for {input_file.name}: {scf_iterations_data}")

        # Extract only the 'total' energy values from each SCF iteration
        total_energies_ev = []
        for iteration in scf_iterations_data:
            if 'energy' in iteration and 'total' in iteration['energy'] and 'value' in iteration['energy']['total']:
                # The log shows values like 1.120151826584347e-16, which are likely already in eV based on typical NOMAD output.
                # If they were in Joules, a conversion (e.g., / 1.60218e-19) would be needed here.
                # Given your note "energy values are in eV", we'll assume direct use.
                total_energies_ev.append(iteration['energy']['total']['value'])
                try:
                    divided_energy = iteration['energy']['total']['value'] / ELEMENTARY_CHARGE_VALUE
                    total_energies.append(divided_energy)
                except ZeroDivisionError:
                    log.warning(f"Skipping division by zero for energy value: {iteration['energy']['total']['value']}")
                    total_energies.append(float('nan')) # Append NaN for invalid division

        filtered_data = {
            "domain": full_data.get("metadata", {}).get("domain"),
            "scf_total_energies_ev": total_energies_ev, # Add the extracted energies here
            "unit": "eV" # Explicitly state the unit
        }

        # Remove keys with None values for a cleaner output
        filtered_data = {k: v for k, v in filtered_data.items() if v is not None}

        # --- Save as JSON ---
        log.info(f"Saving filtered parsed data to {json_output_path}")
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
            # log the stderr from the failed command for better debugging
            log.error(f"NOMAD parsing command failed with exit code {e.returncode}: {e.stderr}", exc_info=True)
            raise
    except json.JSONDecodeError as e:
        log.error(f"Failed to decode JSON output from NOMAD parser for {input_file.name}: {e}")
        log.error(f"Problematic output snippet: {raw_json_output[e.pos:e.pos+200]}...")
        raise
    except Exception as e:
        log.error(f"An unexpected error occurred during parsing of {input_file.name}: {e}", exc_info=True)
        raise

