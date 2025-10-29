# fairtool/cli.py

"""Main CLI entry point for the FAIR tool."""
import os
import typer
from typing_extensions import Annotated
from pathlib import Path
from typing import Optional
import logging
import rich
import sys
from rich.logging import RichHandler
# Import subcommand functions
from . import parse as parse_module
from . import analyze as analyze_module
from . import summarize as summarize_module
from . import visualize as visualize_module
from . import export as export_module
from . import __version__

console = rich.console.Console()

# Configure logging
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(show_path=False, rich_tracebacks=True, markup=True, keywords=["error", "failed", "success", "warning"], tracebacks_suppress=[typer])]
)
log = logging.getLogger("fairtool")

# Create the Typer application
app = typer.Typer(
    name="fair",
    help="Process, Analyze, Visualize, and Export Computational Materials Data.",
    add_completion=True,
    no_args_is_help=True,
    callback=None,
)

# --- Typer Command Definitions ---
@app.command()
def about():
    """
    Information about the FAIR Tool and its creators.
    """
    console.print("")
    console.print("")
    console.rule()
    console.print("FAIR Tool - Computational Materials Data Processing made FAIR", style="bold magenta")
    console.print(r"""
  █████▒ ▄▄▄       ██▓ ██▀███  ▄▄▄█████▓ ▒█████   ▒█████   ██▓
▓██   ▒ ▒████▄    ▓██▒▓██ ▒ ██▒▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒
▒████ ░ ▒██  ▀█▄  ▒██▒▓██ ░▄█ ▒▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░
░▓█▒  ░ ░██▄▄▄▄██ ░██░▒██▀▀█▄  ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░
░▒█░     ▓█   ▓██▒░██░░██▓ ▒██▒  ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒
 ▒ ░     ▒▒   ▓▒█░░▓  ░ ▒▓ ░▒▓░  ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░
 ░        ▒   ▒▒ ░ ▒ ░  ░▒ ░ ▒░    ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░
 ░ ░      ░   ▒    ▒ ░  ░░   ░   ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░
              ░  ░ ░     ░                  ░ ░      ░ ░      ░  ░
    """, style="dark_orange")
    console.print("FAIR Tool is a command-line interface for processing, analyzing, and visualizing computational materials data.", style="cyan")
    console.print("It is designed to work with various calculation output files and provides a streamlined workflow.", style="cyan")
    console.print("The tool is built on top of electronic-parsers and other libraries to facilitate data handling.", style="cyan")
    console.print("")
    console.print("Version: " + str(__version__), style="orange1")
    console.print("")
    console.print("Project Lead: Dr. Ravindra Shinde", style="orange1")
    console.print("Email : r.l.shinde@utwente.nl", style="orange1")
    console.print("")
    console.print("Contributor: Konstantinos Kontogiannis", style="orange1")
    console.print("Email : k.kontogiannis@student.utwente.nl", style="orange1")
    console.print("")
    console.print("Funding: " + "4TU Research Data Fund 4th Edition", style="orange1")
    console.print("")
    console.rule()
    console.print("")



# --- Helper Functions ---

def _find_calc_files(path: Path, recursive: bool = True) -> list[Path]:
    """
    Finds relevant calculation files for parsing.

    Args:
        path (Path): The root path or file to inspect.
        recursive (bool): If True, search all subdirectories. If False, only the given directory.

    Returns:
        list[Path]: List of calculation files to process.
    """
    files_to_process = []
    if not path.exists():
        log.error(f"Error: Input path does not exist: {path}")
        raise typer.Exit(code=1)

    if path.is_file():
        # TODO: Add more sophisticated file type checking if needed
        files_to_process.append(path)
        #ask user to confirm processing this file
        confirm =input(f"Proceed to process the file {path}? (y/n): ")
        if confirm.lower() != 'y':
            log.info("Aborting file processing as per user request.")
            raise typer.Exit(code=0)

    elif path.is_dir():
        # TODO: Implement logic to find relevant files (e.g., VASP OUTCAR, QE output)
        # This is a placeholder - customize based on expected file names/extensions
        #log.info(f"Searching for calculation files in: {path}")
        #log.info(f"Recursive search: {recursive}")

        # Pick search strategy
        search_method = path.rglob if recursive else path.glob

        # Typical calculation file types
        potential_files = (
            list(search_method("vasprun.xml"))+
            #list(search_method("OUTCAR")) +
            #list(search_method("*.out")) +
            list(search_method("*.xml"))
        )


        if not potential_files:
             log.warning(f"No potential calculation files found in {path}")
        else:
            log.info(f"Found {len(potential_files)} potential calculation files.")
            #for f in potential_files:
            #    log.info(f" - {f}")
            
            # show which directories they were found in
            unique_dirs = sorted(set(f.parent for f in potential_files))
            log.info("\n Detected directories with calculation files:")
            
            for d in unique_dirs:
                log.info(f" - {d}")
                #highlight files in this directory
                for f in potential_files:
                    if f.parent == d:
                        log.info(f"    - {f.name}")

            #ask user to confirm processing all found files
            confirm =input(f"Proceed to process all {len(potential_files)} files? (y/n): ")
            if confirm.lower() != 'y':
                log.info("Aborting file processing as per user request.")
                raise typer.Exit(code=0)
        
            files_to_process.extend(potential_files)
        

        # Add more specific file finding logic here based on electronic-parsers capabilities
    else:
        log.error(f"Error: Input path is neither a file nor a directory: {path}")
        raise typer.Exit(code=1)

    if not files_to_process:
         log.warning(f"No files identified for processing at path: {path}")

    return files_to_process

def version_callback(value: bool):
    """Prints the version and exits."""
    if value:
        rich.print(f"FAIR Tool Version: {__version__}")
        raise typer.Exit()



@app.command()
def parse(
    input_path: Annotated[Optional[Path], typer.Argument(
        help="Path to a calculation output file (single file only).",
        exists=False,     
        file_okay=True,   
        dir_okay=False,   
        resolve_path=True 
    )] = None,

    search_dir: Annotated[Optional[Path], typer.Option(
        "--directory", "-d",
        help="Directory to search for calculation output files (e.g., vasprun.xml, OUTCAR).",
        resolve_path=True,
    )] = None,

    root_directory: Annotated[Optional[Path], typer.Option(
        "--root-directory", "-r",
        help="Root directory to search recursively through (e.g., /home/user/projects).",
        resolve_path=True,
    )] = None,


    output_dir: Annotated[Optional[Path], typer.Option(
        "--output", "-o",
        help="Directory to save parsed JSON files. "
             "If not given, parsed files will be saved next to the originals.",
        resolve_path=True,
    )] = None,

    force: Annotated[bool, typer.Option(
        "--force", "-f",
        help="Overwrite existing output files."
    )] = True,
):
    """
    Parse calculation output files into structured JSON and Markdown.
    """

    log.info("FAIR Tool - Parse Command")
    log.info(f"Input Path: {input_path}")
    log.info(f"Search Directory: {search_dir}")
    log.info(f"Root Directory: {root_directory}")
    log.info(f"Output Directory: {output_dir}")
    log.info(f"Force Overwrite: {force}")

    # --- Determine search path behavior ---
    # so if there is not path provided, we default to home directory based on OS
    if root_directory: # if root_directory is provided after -r, use it
        search_path = root_directory
        deep_search = True
    elif search_dir: # if search_dir is provided after -d, use it
        search_path = search_dir
        deep_search = False
    elif input_path: # if input_path is provided,after parse command, use it
        search_path = input_path
        deep_search = False
    else:
        home = Path.home()
        log.info(f"Home path: {home}.")
        system_name = sys.platform
        log.info(f"System platform: {system_name}.")
        deep_search = True
        
        if "windows" in system_name.lower():
            user_name = home.name
            search_path = Path(f"C:\\users\\{user_name}\\")
            log.info(f"No input path or search directory provided. Defaulting to windows path: C:\\users\\{user_name}\\")
        else:
            search_path = home
            log.info(f"No input path or search directory provided. Defaulting to linux path: {home}")  
  

    #log.info(f"Search path: {search_path}")
    log.info(f"Search depth (recursive): {deep_search}")

    log.info(f"Starting parsing process for: {search_path}")


    files_to_process = _find_calc_files(search_path, recursive=deep_search)
    if not files_to_process:
        log.warning("No files found to parse.")
        return # Exit gracefully

    for file in files_to_process:
        try:

            # If no --output given, use file’s directory
            target_dir = output_dir if output_dir else file.parent
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Check for existing parsed JSON and decide whether to skip parsing
            base_name = file.stem
            json_output_path = target_dir/ f"fair_parsed_{base_name}.json"


            if not force and json_output_path.exists():
                try:
                    with open(json_output_path, 'r', encoding='utf-8') as jf:
                        existing = __import__('json').load(jf)
                    # look in metadata for fair_parse_time
                    fair_time = None
                    if isinstance(existing, dict):
                        md = existing.get('metadata')
                        if isinstance(md, dict):
                            fair_time = md.get('fair_parse_time')
                    file_mtime = file.stat().st_mtime
                    if fair_time is not None and float(fair_time) >= float(file_mtime):
                        log.info(f"Skipping parse for {file} — unchanged since last parse (fair_parse_time={fair_time}).")
                        continue
                except Exception:
                    # If anything goes wrong reading existing JSON, fall back to parsing
                    log.debug(f"Could not read existing parse metadata for {json_output_path}; will re-parse.")

            log.info(f"Parsing file: {file}")
            parse_module.run_parser(file, target_dir, force)
        except Exception as e:
            log.error(f"Failed to parse {file}: {e}", exc_info=True)
            # Optionally continue to next file or exit
            # raise typer.Exit(code=1)

    log.info("Parsing finished.")


@app.command()
def analyze(
    input_path: Annotated[Path, typer.Argument(
        help="Path to a parsed JSON file or a directory containing them (usually from 'fair parse').",
        exists=True,
        file_okay=True,
        dir_okay=True,
        resolve_path=True,
    )],
     output_dir: Annotated[Path, typer.Option(
        "--output", "-o",
        help="Directory to save analysis results (e.g., plots, summary tables).",
        resolve_path=True,
    )] = Path("."),
     config: Annotated[Path, typer.Option(
        "--config", "-c",
        help="Path to an optional analysis configuration file (e.g., YAML).",
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    )] = None,
):
    """
    Perform analysis on parsed calculation data.
    (Example: Calculate band gap, density of states features, etc.)
    """
    log.info(f"Starting analysis process for: {input_path}")
    output_dir.mkdir(parents=True, exist_ok=True)
    log.info(f"Analysis output will be saved to: {output_dir}")
    if config:
        log.info(f"Using analysis configuration: {config}")

    # TODO: Implement logic to find relevant JSON files if input_path is a directory
    # Similar to _find_calc_files but looking for *.json or specific names

    # Placeholder for actual analysis
    try:
        log.info("Analysis started.")
        # analyze_module.run_analysis(input_path, output_dir, config)
    except Exception as e:
        log.error(f"Analysis failed for {input_path}: {e}", exc_info=True)
        raise typer.Exit(code=1)

    log.info("Analysis finished.")


@app.command()
def summarize(
    input_path: Annotated[Path, typer.Argument(
        help="Path to parsed/analyzed data (JSON/directory) to summarize.",
         exists=True,
        file_okay=True,
        dir_okay=True,
        resolve_path=True,
    )],
    output_dir: Annotated[Path, typer.Option(
        "--output", "-o",
        help="Directory to save summary files (e.g., Markdown reports).",
        resolve_path=True,
    )] = Path("."),
    template: Annotated[str, typer.Option(
        "--template", "-t",
        help="Optional template for generating the summary report."
    )] = None,
):
    """
    Generate human-readable summaries from parsed or analyzed data.
    (Example: Create a Markdown report with key findings).
    """
    log.info(f"Starting summarization process for: {input_path}")
    output_dir.mkdir(parents=True, exist_ok=True)
    log.info(f"Summary output will be saved to: {output_dir}")


    # --- Verify file type ---
    if input_path.suffix.lower() != ".json":
        log.error(f"Input must be a JSON file, not: {input_path.suffix}")
        raise typer.Exit(code=1)

    # --- Prepare output path ---
    base_name = input_path.stem
    md_output_path = output_dir / f"fair_summarized_{base_name}.md"

    if md_output_path.exists() and not force:
        log.info(f"Summary already exists at {md_output_path}.")
        raise typer.Exit(code=0)

    
    if template:
        log.info(f"Using summary template: {template}")

    # TODO: Implement logic to find relevant input files if input_path is a directory

    try:
        log.info("Summarization started.")
        summarize_module.run_summarization(input_path, output_dir, template)
    except Exception as e:
        log.error(f"Summarization failed for {input_path}: {e}", exc_info=True)
        raise typer.Exit(code=1)

    log.info("Summarization finished.")

@app.command()
def export(
    input_path: Annotated[Path, typer.Argument(
        help="Path to parsed/analyzed data (JSON/directory) to export.",
         exists=True,
        file_okay=True,
        dir_okay=True,
        resolve_path=True,
    )],
    output_dir: Annotated[Path, typer.Option(
        "--output", "-o",
        help="Directory to save exported files.",
        resolve_path=True,
    )] = Path("."),
    format: Annotated[str, typer.Option(
        "--format", "-fmt",
        help="Export format (e.g., 'csv', 'json_summary', 'yaml').",
    )] = "csv",
):
    """
    Export processed data into different file formats.
    """
    log.info(f"Starting export process for: {input_path}")
    output_dir.mkdir(parents=True, exist_ok=True)
    log.info(f"Exported files will be saved to: {output_dir} in format '{format}'")

    # TODO: Implement logic to find relevant input files if input_path is a directory

    try:
        log.info("Export started.")
        # export_module.run_export(input_path, output_dir, format)
    except Exception as e:
        log.error(f"Export failed for {input_path} (format: {format}): {e}", exc_info=True)
        raise typer.Exit(code=1)

    log.info("Export finished.")


@app.command()
def visualize(
    input_path: Annotated[Path, typer.Argument(
        help="Path to parsed data (JSON/directory) containing structures, BZ, etc.",
         exists=True,
        file_okay=True,
        dir_okay=True,
        resolve_path=True,
    )],
    output_dir: Annotated[Path, typer.Option(
        "--output", "-o",
        help="Directory to save visualization data (e.g., JSON for React components) and potentially Markdown snippets.",
        resolve_path=True,
    )] = Path("."),
    embed: Annotated[bool, typer.Option(
        "--embed", "-e",
        help="Generate Markdown snippets for embedding visualizations in mkdocs.",
    )] = False,
):
    """
    Generate data for visualizations (structures, BZ, DOS, bands).
    Optionally creates Markdown snippets for mkdocs embedding.
    """

    log.info(f"Starting visualization data generation for: {input_path}")
    output_dir.mkdir(parents=True, exist_ok=True)
    log.info(f"Visualization data will be saved to: {output_dir}")
    if embed:
        log.info("Will generate Markdown embedding snippets.")

    # TODO: Implement logic to find relevant input files if input_path is a directory

    try:
        log.info("Visualization data generation started.")
        # visualize_module.run_visualization(input_path, output_dir, embed)
    except Exception as e:
        log.error(f"Visualization data generation failed for {input_path}: {e}", exc_info=True)
        raise typer.Exit(code=1)

    log.info("Visualization data generation finished.")


@app.command()
def all(
    input_path: Annotated[Path, typer.Argument(
        help="Path to a calculation output file or a directory containing them.",
        exists=True,
        file_okay=True,
        dir_okay=True,
        resolve_path=True,
    )],
    output_dir: Annotated[Path, typer.Option(
        "--output", "-o",
        help="Directory to save all generated outputs (parsed, analysis, summaries, visualizations, exports).",
        resolve_path=True,
    )] = Path("./"),
    force: Annotated[bool, typer.Option(
        "--force", "-f",
        help="Force re-generation of outputs where applicable (passed to parse).",
    )] = True,
    config: Annotated[Path, typer.Option(
        "--config", "-c",
        help="Optional analysis configuration file (passed to analyze).",
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    )] = None,
    template: Annotated[str, typer.Option(
        "--template", "-t",
        help="Optional summary template (passed to summarize).",
    )] = None,
    export_format: Annotated[str, typer.Option(
        "--format", "-fmt",
        help="Export format for the export step (e.g., csv, yaml, json_summary).",
    )] = "csv",
    embed: Annotated[bool, typer.Option(
        "--embed", "-e",
        help="Generate Markdown embedding snippets during visualization.",
    )] = False,
):
    """
    Run the full FAIR workflow: parse -> analyze -> summarize -> export -> visualize.

    This command simply invokes the other commands in serial order. Each step will
    write into the provided `output_dir` (which will be created if missing).
    """
    log.info("Starting full FAIR workflow (all steps)")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Parse
    try:
        log.info("STEP 1/5: parse")
        parse_module.run_parser(input_path, output_dir, force)
    except Exception as e:
        log.error(f"Parsing step failed: {e}", exc_info=True)
        raise typer.Exit(code=1)

    # Step 2: Analyze
    try:
        log.info("STEP 2/5: analyze")
        analyze_module.run_analysis(output_dir, output_dir, config)
    except Exception as e:
        log.error(f"Analysis step failed: {e}", exc_info=True)
        raise typer.Exit(code=1)

    # Step 3: Summarize
    try:
        log.info("STEP 3/5: summarize")
        summarize_module.run_summarization(output_dir, output_dir, template)
    except Exception as e:
        log.error(f"Summarization step failed: {e}", exc_info=True)
        raise typer.Exit(code=1)

    # Step 4: Export
    try:
        log.info("STEP 4/5: export")
        export_module.run_export(output_dir, output_dir, export_format)
    except Exception as e:
        log.error(f"Export step failed: {e}", exc_info=True)
        raise typer.Exit(code=1)

    # Step 5: Visualize
    try:
        log.info("STEP 5/5: visualize")
        visualize_module.run_visualization(output_dir, output_dir, embed)
    except Exception as e:
        log.error(f"Visualization step failed: {e}", exc_info=True)
        raise typer.Exit(code=1)

    log.info("Full FAIR workflow completed successfully.")


# --- Version Callback ---

@app.callback()
def main_callback(
    version: Annotated[
        bool, typer.Option("--version", "-v", callback=version_callback, is_eager=True, help="Show version and exit.")
    ] = False,
):
    """
    FAIR Tool main command group.
    """
    # This callback runs before any command.
    # We use it mainly for the --version flag.
    pass


if __name__ == "__main__":
    # This allows running the script directly for debugging,
    # although `python -m fairtool` or the installed `fair` command is preferred.
    app()

