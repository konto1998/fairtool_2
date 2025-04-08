# fairtool/parse.py

"""Handles the parsing of calculation files."""

import json
import logging
from pathlib import Path
# from electronic_parsers import auto

log = logging.getLogger("fairtool")

def run_parser(input_file: Path, output_dir: Path, force: bool):
    """
    Parses a single calculation file using electronic-parsers.

    Args:
        input_file: Path to the calculation output file.
        output_dir: Directory to save the parsed JSON and Markdown.
        force: Whether to overwrite existing output files.
    """
    # Define output file paths
    base_name = input_file.stem # Or create a more robust naming scheme
    json_output_path = output_dir / f"{base_name}_parsed.json"
    md_output_path = output_dir / f"{base_name}_report.md"

    # Check if output exists and if force is not set
    if not force and (json_output_path.exists() or md_output_path.exists()):
        log.warning(f"Output files for {input_file.name} already exist in {output_dir}. Use --force to overwrite.")
        return # Skip processing

    log.info(f"Attempting to parse {input_file.name}...")

    try:
        # Use electronic_parsers.auto.parse
        # This function attempts to automatically detect the code and parse the file.
        # It typically returns a dictionary (or a list of dictionaries for multi-entry files).
        # Note: The exact return format and capabilities depend on the electronic-parsers version
        # and the specific parser used. You might need to adjust based on its API.
        # parsed_data = auto.parse(str(input_file))
        parsed_data = str(input_file)

        if not parsed_data:
             log.warning(f"Parser returned no data for {input_file.name}.")
             return

        # --- Save as JSON ---
        log.debug(f"Saving parsed data to {json_output_path}")
        try:
            with open(json_output_path, 'w', encoding='utf-8') as f:
                # Use default=str to handle non-serializable types like numpy arrays if they appear
                json.dump(parsed_data, f, indent=2, default=str)
            log.info(f"Successfully saved JSON: {json_output_path.name}")
        except Exception as json_err:
            log.error(f"Failed to save JSON for {input_file.name}: {json_err}")
            # Clean up potentially broken file
            if json_output_path.exists():
                json_output_path.unlink()
            raise # Re-raise the exception

        # --- Generate and Save Markdown ---
        log.debug(f"Generating Markdown report for {input_file.name}")
        try:
            # TODO: Implement Markdown generation logic.
            # This could involve iterating through parsed_data and formatting key information.
            # You might use Jinja2 templates for more complex reports.
            md_content = generate_markdown_report(parsed_data, input_file.name)
            with open(md_output_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            log.info(f"Successfully saved Markdown: {md_output_path.name}")
        except Exception as md_err:
            log.error(f"Failed to generate or save Markdown for {input_file.name}: {md_err}")
            # Clean up potentially broken file
            if md_output_path.exists():
                md_output_path.unlink()
            # Decide if failure here should stop JSON saving (if MD is critical)

    except ImportError:
         log.error("`electronic-parsers` not found. Please install it (`pip install electronic-parsers`)")
         raise
    except FileNotFoundError:
        log.error(f"Input file not found during parsing: {input_file}")
        raise
    except Exception as e:
        log.error(f"An unexpected error occurred while parsing {input_file.name}: {e}")
        # Clean up any partial files created before the error
        if json_output_path.exists(): json_output_path.unlink(missing_ok=True)
        if md_output_path.exists(): md_output_path.unlink(missing_ok=True)
        raise # Re-raise the exception to be caught by the CLI


def generate_markdown_report(data: dict, filename: str) -> str:
    """
    Generates a simple Markdown report from parsed data. (Placeholder)

    Args:
        data: The dictionary returned by the parser.
        filename: The original name of the parsed file.

    Returns:
        A string containing the Markdown report.
    """
    # --- Placeholder Implementation ---
    # Customize this extensively based on the actual structure of `data`
    # from electronic-parsers and the information you want to highlight.
    report_lines = [
        f"# Parsing Report for `{filename}`",
        "",
        "## Summary",
        "- **Parser Used**: (Detect or specify based on `data` if available)",
        "- **Calculation Status**: (Extract completion status if available)",
        "",
        "## Key Data Extracted",
        "(Add details here, e.g., total energy, number of atoms, lattice parameters)",
        "```json",
        json.dumps(data, indent=2, default=str), # Dump subset or all data for reference
        "```",
        "",
        "---",
        "*Generated by FAIR Tool*",
    ]
    return "\n".join(report_lines)

