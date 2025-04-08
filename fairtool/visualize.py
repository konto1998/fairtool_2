# fairtool/visualize.py

"""Handles generation of data for visualizations."""

import json
import logging
from pathlib import Path

# Essential: pymatgen for structure/band/DOS objects
try:
    from pymatgen.core import Structure
    from pymatgen.io.ase import AseAtomsAdaptor # If parser gives ASE Atoms
    # Import other relevant pymatgen modules (BandStructureSymmLine, CompleteDos, etc.)
    # from pymatgen.electronic_structure.bandstructure import BandStructureSymmLine
    # from pymatgen.electronic_structure.dos import CompleteDos
except ImportError:
    log.warning("Pymatgen not found. Visualization capabilities will be limited. Install with `pip install pymatgen`")
    Structure = None # Define as None to allow checks later
    AseAtomsAdaptor = None

log = logging.getLogger("fairtool")

# --- Data Preparation Functions ---

def get_structure_data(parsed_data: dict) -> dict | None:
    """
    Extracts structure data from parsed output and formats it for visualization
    (e.g., in a format compatible with Materials Project React components or pymatgen).

    Args:
        parsed_data: The dictionary loaded from the parser's JSON output.

    Returns:
        A dictionary containing structure information (e.g., pymatgen Structure as dict,
        or a custom format suitable for your React components), or None if not found.
    """
    if not Structure:
        log.warning("Pymatgen not available, cannot process structure data.")
        return None

    log.debug("Attempting to extract structure data...")
    structure = None
    try:
        # --- Strategy 1: Look for pymatgen structure directly (ideal if parser provides it) ---
        # This depends heavily on electronic-parsers output format. Check its documentation.
        # Example hypothetical path:
        pmg_structure_dict = parsed_data.get("results", {}).get("properties", {}).get("structure", {}).get("pymatgen_structure")
        if pmg_structure_dict:
            structure = Structure.from_dict(pmg_structure_dict)
            log.debug("Found structure data (pymatgen format).")

        # --- Strategy 2: Look for primitive structure / ASE atoms ---
        # Example hypothetical path for ASE Atoms object (needs AseAtomsAdaptor)
        elif AseAtomsAdaptor:
             ase_atoms_dict = parsed_data.get("results", {}).get("properties", {}).get("structure", {}).get("ase_atoms")
             if ase_atoms_dict and hasattr(AseAtomsAdaptor, 'get_atoms'): # Check method exists
                 # Need to reconstruct ASE Atoms object first if stored as dict
                 # This part is complex and depends on how ASE atoms are serialized
                 # atoms = ase.io.jsonio.read_json(io.StringIO(json.dumps(ase_atoms_dict))) # Hypothetical
                 # structure = AseAtomsAdaptor.get_structure(atoms)
                 log.warning("ASE Atoms reconstruction from JSON not fully implemented.") # Placeholder
             else:
                 # Look for basic lattice vectors and atomic positions
                 # Example path (adjust based on parser output):
                 lattice_vectors = parsed_data.get("results", {}).get("properties", {}).get("structure", {}).get("lattice_vectors")
                 species = parsed_data.get("results", {}).get("properties", {}).get("structure", {}).get("species_at_sites")
                 coords = parsed_data.get("results", {}).get("properties", {}).get("structure", {}).get("cartesian_site_positions") # Or fractional
                 coords_are_cartesian = True # Assume cartesian, adjust if fractional

                 if lattice_vectors and species and coords:
                     log.debug("Found basic structure data (lattice, species, coords).")
                     structure = Structure(
                         lattice=lattice_vectors,
                         species=species,
                         coords=coords,
                         coords_are_cartesian=coords_are_cartesian
                     )
                 else:
                    log.warning("Could not find sufficient structure data in parsed output.")
                    return None

        if structure:
             # Convert pymatgen Structure to a dictionary suitable for JSON serialization
             # This is often needed for passing data to JavaScript/React
             return structure.as_dict()
        else:
            return None

    except Exception as e:
        log.error(f"Error processing structure data: {e}", exc_info=True)
        return None


def get_band_structure_data(parsed_data: dict) -> dict | None:
    """ Extracts and formats band structure data. (Placeholder) """
    log.debug("Attempting to extract band structure data...")
    # TODO: Implement logic similar to get_structure_data
    # - Look for BandStructureSymmLine object (ideal)
    # - Look for raw k-points, eigenvalues, labels
    # - Format into a dictionary suitable for plotting (e.g., segments, energies)
    #   compatible with your React component.
    try:
        # Example hypothetical path for pymatgen BS object
        bs_dict = parsed_data.get("results", {}).get("properties", {}).get("electronic", {}).get("band_structure", {}).get("pymatgen_bandstructure")
        if bs_dict:
             # Potentially needs further processing or just return the dict
             log.debug("Found band structure data (pymatgen format).")
             # from pymatgen.electronic_structure.bandstructure import BandStructureSymmLine
             # bs = BandStructureSymmLine.from_dict(bs_dict)
             # return bs.as_dict() # Or a custom format
             return bs_dict # Return as is for now
        else:
            log.warning("Band structure data not found or format not recognized.")
            return None
    except Exception as e:
        log.error(f"Error processing band structure data: {e}", exc_info=True)
        return None

def get_dos_data(parsed_data: dict) -> dict | None:
    """ Extracts and formats Density of States (DOS) data. (Placeholder) """
    log.debug("Attempting to extract DOS data...")
    # TODO: Implement logic similar to get_structure_data
    # - Look for CompleteDos object (ideal)
    # - Look for raw energy levels and DOS values
    # - Format into a dictionary suitable for plotting
    try:
        # Example hypothetical path for pymatgen DOS object
        dos_dict = parsed_data.get("results", {}).get("properties", {}).get("electronic", {}).get("dos", {}).get("pymatgen_dos")
        if dos_dict:
             log.debug("Found DOS data (pymatgen format).")
             # from pymatgen.electronic_structure.dos import CompleteDos
             # dos = CompleteDos.from_dict(dos_dict)
             # return dos.as_dict() # Or a custom format
             return dos_dict # Return as is for now
        else:
            log.warning("DOS data not found or format not recognized.")
            return None
    except Exception as e:
        log.error(f"Error processing DOS data: {e}", exc_info=True)
        return None


# --- Markdown Embedding ---

def generate_markdown_embedding(data_file_path: Path, viz_type: str, component_id: str) -> str:
    """
    Generates a Markdown snippet to embed a visualization using a hypothetical React component.

    Args:
        data_file_path: Path to the JSON data file for the visualization (relative path preferred).
        viz_type: Type of visualization ('structure', 'bands', 'dos').
        component_id: A unique ID for the HTML element where the component will mount.

    Returns:
        A Markdown string containing HTML/JS to load the component.
    """
    # IMPORTANT: This is highly dependent on how your mkdocs site is set up
    # and how the React components are loaded and used.
    # This example assumes:
    # 1. You have JavaScript on your mkdocs site that looks for divs with a specific class (e.g., 'react-viz-mount').
    # 2. This script reads data attributes (data-viz-type, data-src, data-id).
    # 3. It then dynamically loads and renders the appropriate React component into the div.

    # Use relative path for embedding in mkdocs if possible
    relative_data_path = data_file_path.name # Simplistic, might need better relative path logic

    # Customize the HTML structure and data attributes based on your actual JS implementation
    snippet = f"""
<div
  id="{component_id}"
  class="react-viz-mount"
  data-viz-type="{viz_type}"
  data-src="{relative_data_path}"
  style="width: 100%; height: 400px; border: 1px solid #ccc; margin-bottom: 1em; border-radius: 8px;"
>
  Loading {viz_type} visualization...
  </div>

"""
    return snippet

# --- Main Execution Logic ---

def run_visualization(input_path: Path, output_dir: Path, embed: bool):
    """
    Generates visualization data (JSON) and optionally Markdown embedding snippets.

    Args:
        input_path: Path to parsed JSON file or directory.
        output_dir: Directory to save visualization JSON files and Markdown snippets.
        embed: Whether to generate Markdown embedding snippets.
    """
    # --- Find input files ---
    if input_path.is_file() and input_path.suffix == '.json':
        files_to_process = [input_path]
    elif input_path.is_dir():
        log.info(f"Searching for parsed JSON files (*_parsed.json) in: {input_path}")
        files_to_process = sorted(list(input_path.rglob("*_parsed.json")))
        if not files_to_process:
             log.warning(f"No '*_parsed.json' files found in {input_path}")
             return
    else:
        log.error(f"Input path must be a JSON file or a directory containing them: {input_path}")
        return

    log.info(f"Found {len(files_to_process)} JSON file(s) to process for visualization.")

    md_snippets = [] # Collect markdown snippets if embed is True

    for file in files_to_process:
        log.info(f"Processing for visualization: {file.name}")
        base_name = file.stem.replace("_parsed", "") # Get cleaner base name
        viz_data_found = False

        try:
            with open(file, 'r') as f:
                parsed_data = json.load(f)

            # --- Generate Structure Visualization Data ---
            structure_viz_data = get_structure_data(parsed_data)
            if structure_viz_data:
                viz_data_found = True
                output_file = output_dir / f"{base_name}_structure.json"
                log.info(f"Saving structure visualization data to: {output_file.name}")
                with open(output_file, 'w') as f:
                    json.dump(structure_viz_data, f, indent=2)
                if embed:
                    component_id = f"viz-struct-{base_name}"
                    md_snippets.append(f"### Structure: `{base_name}`\n")
                    md_snippets.append(generate_markdown_embedding(output_file, "structure", component_id))
                    md_snippets.append("\n")


            # --- Generate Band Structure Visualization Data ---
            bands_viz_data = get_band_structure_data(parsed_data)
            if bands_viz_data:
                viz_data_found = True
                output_file = output_dir / f"{base_name}_bands.json"
                log.info(f"Saving band structure visualization data to: {output_file.name}")
                with open(output_file, 'w') as f:
                    json.dump(bands_viz_data, f, indent=2)
                if embed:
                    component_id = f"viz-bands-{base_name}"
                    md_snippets.append(f"### Band Structure: `{base_name}`\n")
                    md_snippets.append(generate_markdown_embedding(output_file, "bands", component_id))
                    md_snippets.append("\n")

            # --- Generate DOS Visualization Data ---
            dos_viz_data = get_dos_data(parsed_data)
            if dos_viz_data:
                viz_data_found = True
                output_file = output_dir / f"{base_name}_dos.json"
                log.info(f"Saving DOS visualization data to: {output_file.name}")
                with open(output_file, 'w') as f:
                    json.dump(dos_viz_data, f, indent=2)
                if embed:
                    component_id = f"viz-dos-{base_name}"
                    md_snippets.append(f"### Density of States: `{base_name}`\n")
                    md_snippets.append(generate_markdown_embedding(output_file, "dos", component_id))
                    md_snippets.append("\n")

            if not viz_data_found:
                 log.warning(f"No suitable visualization data (structure, bands, DOS) found in {file.name}")


        except json.JSONDecodeError:
            log.error(f"Failed to decode JSON from {file.name}. Skipping.")
            continue
        except Exception as e:
            log.error(f"Error processing {file.name} for visualization: {e}", exc_info=True)
            # Decide whether to continue or stop

    # --- Save Markdown Snippets File ---
    if embed and md_snippets:
        md_output_file = output_dir / "visualization_embeds.md"
        log.info(f"Saving all Markdown embedding snippets to: {md_output_file}")
        try:
            with open(md_output_file, 'w', encoding='utf-8') as f:
                f.write(f"# Visualization Embeddings\n\n")
                f.write(f"Place the generated JSON files (e.g., `{base_name}_structure.json`) in a location accessible by your mkdocs site (e.g., within the `docs/assets/viz_data/` directory).\n\n")
                f.write(f"Ensure your mkdocs site has the necessary JavaScript to find `div.react-viz-mount` elements and render the appropriate React components using the `data-src` attribute.\n\n")
                f.write("---\n\n")
                f.write("\n".join(md_snippets))
        except Exception as e:
            log.error(f"Failed to save Markdown snippets file: {e}")

    log.info("Visualization data generation process completed.")

