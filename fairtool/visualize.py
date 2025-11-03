# fairtool/visualize.py

"""Handles generation of data for visualizations."""

import json
import logging
from pathlib import Path
from typing import Optional
import tempfile
import shutil
import subprocess
import re
import sys

log = logging.getLogger(__name__)

# Essential: pymatgen for structure/band/DOS objects
try:
    from pymatgen.core import Structure
    from pymatgen.io.ase import AseAtomsAdaptor # If parser gives ASE Atoms
    # Import other relevant pymatgen modules (BandStructureSymmLine, CompleteDos, etc.)
    # from pymatgen.electronic_structure.bandstructure import BandStructureSymmLine
    # from pymatgen.electronic_structure.dos import CompleteDos
except ImportError:
    # log.warning("Pymatgen not found. Visualization capabilities will be limited. Install with `pip install pymatgen`")
    Structure = None # Define as None to allow checks later
    AseAtomsAdaptor = None

log = logging.getLogger("fairtool")

# --- Data Preparation Functions ---

def get_structure_data(parsed_data: dict) -> Optional[dict]:
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


def get_band_structure_data(parsed_data: dict) -> Optional[dict]:
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

def get_dos_data(parsed_data: dict) -> Optional[dict]:
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


def serve_docs(docs_path: Path, port: int = 8000):
    """
    Launch an mkdocs server that uses the package's documentation styling (mkdocs.yml,
    macros.py, theme overrides) while scanning `docs_path` for the markdown files.

    This function creates a temporary mkdocs config that points `docs_dir` to the
    provided `docs_path` while keeping the rest of the packaged `mkdocs.yml` and
    ensuring `macros.py` is placed next to the config file as required by the
    macros plugin.
    """
    docs_path = Path(docs_path).resolve()
    if not docs_path.exists():
        log.error(f"Docs path does not exist: {docs_path}")
        raise SystemExit(1)

    # Locate the package's top-level documentation directory relative to this file
    package_root = Path(__file__).resolve().parent.parent
    packaged_docs = package_root / "documentation"
    packaged_mkdocs = packaged_docs / "mkdocs.yml"
    packaged_macros = packaged_docs / "macros.py"

    if not packaged_mkdocs.exists():
        log.error(f"Packaged mkdocs.yml not found at expected location: {packaged_mkdocs}")
        raise SystemExit(1)

    # Create a temporary directory to host the modified mkdocs config (and macros)
    temp_dir = Path(tempfile.mkdtemp(prefix="fairtool-mkdocs-"))
    try:
        temp_mkdocs = temp_dir / "mkdocs.yml"

        # Read packaged mkdocs.yml and ensure docs_dir is set to the user-provided path.
        content = packaged_mkdocs.read_text(encoding="utf-8")

        # Create a temporary docs directory that merges user docs and packaged static assets.
        temp_docs = temp_dir / "docs"
        temp_docs.mkdir(parents=True, exist_ok=True)

        # Copy user-provided docs into temp_docs (do not modify original)
        try:
            if docs_path.is_dir():
                for src in docs_path.rglob("*"):
                    rel = src.relative_to(docs_path)
                    dest = temp_docs / rel
                    if src.is_dir():
                        dest.mkdir(parents=True, exist_ok=True)
                    else:
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src, dest)
            else:
                # single file -> copy into temp_docs
                shutil.copy2(docs_path, temp_docs / docs_path.name)
        except Exception:
            log.warning("Failed to copy user docs into temporary docs directory; continuing with limited content.")

        # Copy packaged static assets (stylesheets, js, assets) into temp_docs.
        # Some projects place these under `documentation/` and others under `documentation/docs/`.
        # Try both locations so files like stylesheets/extra.css, js/structure.js and assets/logo.png
        # are available to the dev server and avoid 404s.
        candidate_roots = [packaged_docs, packaged_docs / "docs"]
        for static_name in ("stylesheets", "js", "assets"):
            copied = False
            for root in candidate_roots:
                src = root / static_name
                if src.exists() and src.is_dir():
                    try:
                        shutil.copytree(src, temp_docs / static_name, dirs_exist_ok=True)
                        log.debug(f"Copied static folder {src} -> {temp_docs / static_name}")
                        copied = True
                        break
                    except Exception as e:
                        log.debug(f"Could not copy packaged static folder {src}: {e}")
            if not copied:
                log.debug(f"No packaged static folder found for '{static_name}' in {candidate_roots}")

        # Copy any `includes/` used by snippets (mkdocs docs/ often have an includes folder)
        packaged_includes = packaged_docs / "docs" / "includes"
        if packaged_includes.exists() and packaged_includes.is_dir():
            try:
                shutil.copytree(packaged_includes, temp_docs / "includes", dirs_exist_ok=True)
                log.debug(f"Copied includes folder {packaged_includes} -> {temp_docs / 'includes'}")
            except Exception as e:
                log.debug(f"Could not copy includes folder {packaged_includes}: {e}")

        # Ensure there's an index.md so the site root renders instead of 404
        try:
            index_file = temp_docs / "index.md"
            if not index_file.exists():
                # Build a simple index listing Markdown files found
                md_files = [p for p in temp_docs.rglob("*.md")]
                with open(index_file, 'w', encoding='utf-8') as idx:
                    idx.write("# FAIR Tool - Local Preview\n\n")
                    idx.write("This is a local preview generated by `fair visualize`.\n\n")
                    if md_files:
                        idx.write("## Available pages\n\n")
                        for p in sorted(md_files):
                            rel = p.relative_to(temp_docs)
                            idx.write(f"- [{rel}]({rel})\n")
                    else:
                        idx.write("No markdown pages were found in the provided path.\n")
        except Exception:
            log.debug("Failed to create temporary index.md")

        # Try to replace an existing docs_dir entry in the packaged config; point to temp_docs instead.
        if re.search(r"^\s*docs_dir\s*:\s*.+$", content, flags=re.MULTILINE):
            content = re.sub(r"^\s*docs_dir\s*:\s*.+$", f"docs_dir: '{str(temp_docs)}'", content, flags=re.MULTILINE)
        else:
            # Insert at top
            content = f"docs_dir: '{str(temp_docs)}'\n" + content

        # Override site_url and directory URL handling to ensure dev server serves assets from root
        # and doesn't prepend the packaged site_url (which was set to /fairtool/).
        # Insert or replace site_url and use_directory_urls settings.
        if re.search(r"^\s*site_url\s*:\s*.+$", content, flags=re.MULTILINE):
            content = re.sub(r"^\s*site_url\s*:\s*.+$", f"site_url: 'http://127.0.0.1:{int(port)}'", content, flags=re.MULTILINE)
        else:
            # insert after docs_dir line
            content = content.replace(f"docs_dir: '{str(temp_docs)}'\n", f"docs_dir: '{str(temp_docs)}'\nsite_url: 'http://127.0.0.1:{int(port)}'\n")

        if re.search(r"^\s*use_directory_urls\s*:\s*.+$", content, flags=re.MULTILINE):
            content = re.sub(r"^\s*use_directory_urls\s*:\s*.+$", "use_directory_urls: false", content, flags=re.MULTILINE)
        else:
            content = content.replace(f"site_url: 'http://127.0.0.1:{int(port)}'\n", f"site_url: 'http://127.0.0.1:{int(port)}'\nuse_directory_urls: false\n")

        # Some mkdocs plugins referenced in the packaged mkdocs.yml may not be
        # installed in the user's environment (for example: include_dir_to_nav).
        # If 'include_dir_to_nav' is referenced we try to import it — if it's
        # available we keep it so mkdocs can auto-generate directory-based nav;
        # otherwise we remove it to avoid a hard failure.
        if 'include_dir_to_nav' in content:
            try:
                import importlib
                importlib.import_module('include_dir_to_nav')
                log.info("'include_dir_to_nav' plugin is available in the environment; keeping it in temporary mkdocs config.")
            except Exception:
                log.warning("Detected 'include_dir_to_nav' plugin in packaged mkdocs.yml; plugin not importable in this environment — removing it for live serve. Consider installing the plugin if you need its behavior.")
                # Remove lines like '- include_dir_to_nav' or '  include_dir_to_nav: ...'
                content = re.sub(r"(?m)^[ \t]*-?[ \t]*include_dir_to_nav(?::.*)?$\n(?:^[ \t]+[^\n]*$\n)*", "", content)

        # Build a nav that keeps the top-level horizontal navigation small while
        # exposing directory names in the vertical sidebar. We create a single
        # parent -> root grouping (so horizontal nav shows only Home + parent)
        # and then list directories under that root. For page labels we try to
        # extract the first H1 heading from the markdown; fall back to a
        # humanized filename if none is found. This avoids showing raw filenames
        # like 'vasprun' in the nav.
        try:
            def humanize(stem: str) -> str:
                stem = re.sub(r'^(fair_summarized_|fair_parsed_|fair-)', '', stem)
                stem = stem.replace('_', ' ').replace('-', ' ')
                return stem.strip().replace('.md','').title()

            def first_h1_title(p: Path) -> str:
                try:
                    with open(p, 'r', encoding='utf-8') as fh:
                        for line in fh:
                            line = line.strip()
                            if line.startswith('#'):
                                # remove leading hashes and whitespace
                                return line.lstrip('#').strip()
                except Exception:
                    pass
                return humanize(p.stem)

            nav_lines = []
            nav_lines.append("nav:")
            # Ensure single Home entry
            nav_lines.append("  - Home: index.md")

            parent_label = Path(docs_path).parent.name or Path(docs_path).name or 'Docs'
            root_label = Path(docs_path).name or 'Docs'
            nav_lines.append(f"  - {parent_label}:")
            nav_lines.append(f"    - {root_label}:")

            # helper: find if a directory contains any markdown in its subtree
            def has_markdown(dirpath: Path) -> bool:
                for _ in dirpath.rglob('*.md'):
                    return True
                return False

            # helper: get first markdown in subtree (excluding index.md)
            def first_markdown_in_subtree(dirpath: Path) -> Path:
                for p in sorted(dirpath.rglob('*.md')):
                    if p.name == 'index.md':
                        continue
                    return p
                return None

            # ensure index only for dirs that have markdown in subtree
            def ensure_index_for_dir(dirpath: Path) -> str:
                # skip if no markdown anywhere under dir
                if not has_markdown(dirpath):
                    return ''
                idx = dirpath / 'index.md'
                if idx.exists():
                    return str(idx.relative_to(temp_docs))

                # create index.md summarizing pages and subfolders
                md_files = sorted([p for p in dirpath.glob('*.md') if p.name != 'index.md'])
                subdirs = sorted([sd for sd in dirpath.iterdir() if sd.is_dir() and has_markdown(sd)])
                try:
                    with open(idx, 'w', encoding='utf-8') as fh:
                        fh.write(f"# {dirpath.name}\n\n")
                        fh.write(f"This page is the index for the `{dirpath.name}` folder.\n\n")
                        if md_files:
                            fh.write("## Pages in this folder\n\n")
                            for p in md_files:
                                title = first_h1_title(p)
                                rel = p.relative_to(temp_docs)
                                fh.write(f"- [{title}]({rel})\n")
                            fh.write("\n")
                        if subdirs:
                            fh.write("## Subfolders\n\n")
                            for sd in subdirs:
                                rel = (sd / 'index.md').relative_to(temp_docs)
                                fh.write(f"- [{sd.name}]({rel})\n")
                except Exception:
                    # fallback: if create failed, try linking first md
                    f = first_markdown_in_subtree(dirpath)
                    return str(f.relative_to(temp_docs)) if f else ''
                return str(idx.relative_to(temp_docs))

            # recursive nav builder
            def build_dir_nav(dirpath: Path, indent: int = 6):
                lines = []
                if not has_markdown(dirpath):
                    return lines

                # count markdown in subtree excluding index.md
                md_in_subtree = [p for p in dirpath.rglob('*.md') if p.name != 'index.md']
                # find immediate child dirs that have markdown
                child_dirs = sorted([sd for sd in dirpath.iterdir() if sd.is_dir() and has_markdown(sd)])

                # if exactly one md in entire subtree and no child dirs with markdown -> link directly
                if len(md_in_subtree) == 1 and not child_dirs:
                    only = md_in_subtree[0]
                    rel = str(only.relative_to(temp_docs))
                    lines.append(' ' * indent + f"- {dirpath.name}: {rel}")
                    return lines

                # otherwise create a directory node linking to index (overview)
                idx_rel = ensure_index_for_dir(dirpath)
                lines.append(' ' * indent + f"- {dirpath.name}:")
                if idx_rel:
                    lines.append(' ' * (indent + 2) + f"- {dirpath.name}: {idx_rel}")

                # add direct pages
                direct_pages = sorted([p for p in dirpath.glob('*.md') if p.name != 'index.md'])
                for p in direct_pages:
                    rel = str(p.relative_to(temp_docs))
                    title = first_h1_title(p)
                    lines.append(' ' * (indent + 2) + f"- {title}: {rel}")

                # recurse into child dirs
                for sd in child_dirs:
                    sub_lines = build_dir_nav(sd, indent=indent + 2)
                    # indent and convert leading '-' lines to mkdocs style with proper spaces
                    for l in sub_lines:
                        # ensure lines already include '-' and proper spacing
                        lines.append(l)
                return lines

            # build nav lines for each top-level directory under temp_docs
            top_dirs = sorted([p for p in temp_docs.iterdir() if p.is_dir() and has_markdown(p)])
            for d in top_dirs:
                if d.name in ("assets","stylesheets","js","includes","material"):
                    continue
                dir_nav_lines = build_dir_nav(d, indent=6)
                for ln in dir_nav_lines:
                    # strip leading '-' style and convert to mkdocs YAML list style
                    # our lines already match "      - Name: path" pattern
                    nav_lines.append('  ' + ln)

            generated_nav = "\n".join(nav_lines) + "\n"

            # Replace existing nav block entirely with our generated nav
            nav_match = re.search(r"(?m)^nav:\s*$", content)
            if nav_match:
                remainder = content[nav_match.end():]
                m = re.search(r"(?m)^[^ \t-][^:]*:\s*", remainder)
                if m:
                    nav_end = nav_match.end() + m.start()
                else:
                    nav_end = len(content)
                content = content[:nav_match.start()] + generated_nav + content[nav_end:]
            else:
                content = generated_nav + content
        except Exception:
            log.debug("Failed to auto-generate per-directory nav block; continuing without it.")

        temp_mkdocs.write_text(content, encoding="utf-8")

        # Copy macros.py next to temp mkdocs.yml if it exists in packaged docs
        if packaged_macros.exists():
            shutil.copy(packaged_macros, temp_dir / "macros.py")
        else:
            log.debug("No packaged macros.py found; continuing without copying macros.")

        # Also copy any overrides or theme folders that might be referenced relatively
        # (e.g., material customizations in `documentation/material`)
        packaged_material = packaged_docs / "material"
        if packaged_material.exists() and packaged_material.is_dir():
            dst_material = temp_dir / "material"
            try:
                shutil.copytree(packaged_material, dst_material)
            except Exception:
                # Don't fail if copying fails; warn instead
                log.warning("Failed to copy packaged material overrides; theme customization may be missing.")

        # Build the mkdocs serve command
        cmd = [
            sys.executable, "-m", "mkdocs", "serve",
            "-f", str(temp_mkdocs),
            "--dev-addr", f"127.0.0.1:{int(port)}"
        ]

        log.info(f"Starting mkdocs server on http://127.0.0.1:{port}")
        log.info(f"Using packaged mkdocs config from {packaged_mkdocs} with docs_dir={docs_path}")
        log.info("Press Ctrl+C to stop the server.")

        # Launch mkdocs serve. This will block until the server is stopped.
        try:
            process = subprocess.run(cmd, check=False)
            if process.returncode != 0:
                log.error(f"mkdocs exited with return code {process.returncode}")
                raise SystemExit(process.returncode)
        except FileNotFoundError:
            log.error("`mkdocs` command not found. Is mkdocs installed in the active Python environment? Try `pip install mkdocs mkdocs-material mkdocs-macros-plugin`.")
            raise SystemExit(1)
        except KeyboardInterrupt:
            log.info("mkdocs server stopped by user.")
    finally:
        # Clean up the temporary directory
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass

