# fairtool/visualize.py
"""
Handles generation of data for visualizations.

This module provides:

- A persistent MkDocs-based visualization app, initialized once under:
      ~/.fairtool/visualize_app/
  and served via `fair visualize` (see `visualize_cli`).

- Discovery of "calculation folders" on the filesystem that contain:
    * parsed JSON files,
    * summarized Markdown files,
    * structure JSON files,

  which are then exposed as pages under the MkDocs site.

- Helper functions (get_structure_data, get_band_structure_data, get_dos_data)
  that can be used later to extract visualization data directly from parsed JSON.
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

log = logging.getLogger("fairtool")

# Essential: pymatgen for structure/band/DOS objects
try:
    from pymatgen.core import Structure
    from pymatgen.io.ase import AseAtomsAdaptor  # If parser gives ASE Atoms
    # from pymatgen.electronic_structure.bandstructure import BandStructureSymmLine
    # from pymatgen.electronic_structure.dos import CompleteDos
except ImportError:
    # Pymatgen is optional: visualization will be limited if missing.
    Structure = None
    AseAtomsAdaptor = None

# Persistent app root for the visualization site
APP_ROOT = Path.home() / ".fairtool" / "visualize_app"


# ---------------------------------------------------------------------------
# Data structures & basic helpers
# ---------------------------------------------------------------------------

@dataclass
class CalculationFolder:
    """
    Represents a folder that contains a complete FAIR calculation set.

    Attributes
    ----------
    folder : Path
        Path to the calculation folder.
    parsed_json : list[Path]
        List of parsed JSON files belonging to the calculation.
    summarized_md : list[Path]
        List of summarized Markdown files belonging to the calculation.
    structure_json : Path
        Path to a structure JSON file used by the viewer.
    """
    folder: Path
    parsed_json: List[Path]
    summarized_md: List[Path]
    structure_json: Path

    @property
    def name(self) -> str:
        """Folder name (last path component)."""
        return self.folder.name

    @property
    def rel_to_home(self) -> Path:
        """
        Folder path relative to the user's home directory, if possible.
        Falls back to the absolute path if not under HOME.
        """
        try:
            return self.folder.relative_to(Path.home())
        except Exception:
            return self.folder

from datetime import datetime

def _hr_size(n: int) -> str:
    """Human-readable file size."""
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(n)
    for u in units:
        if size < 1024:
            return f"{size:.1f} {u}"
        size /= 1024
    return f"{size:.1f} PB"

def _extract_title(path: Path) -> str:
    """Extract first markdown/HTML heading."""
    try:
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.startswith("#"):
                return line.lstrip("#").strip()
    except:
        pass
    return "(no title)"


def is_parsed_json(name: str) -> bool:
    """
    Check whether a filename corresponds to a parsed vasprun JSON.

    Rules:
      - endswith '.json'
      - contains 'vasprun'
      - contains 'parsed'
    """
    name = name.lower()
    return name.endswith(".json") and "vasprun" in name and "parsed" in name


def is_summarized_md(name: str) -> bool:
    """
    Check whether a filename corresponds to a summarized vasprun Markdown.

    Rules:
      - endswith '.md'
      - contains 'vasprun'
      - contains 'summarized'
    """
    name = name.lower()
    return name.endswith(".md") and "vasprun" in name and "summarized" in name


def is_structure_json(name: str) -> bool:
    """
    Check whether a filename corresponds to a structure JSON file.

    Rule:
      - endswith '.json'
      - contains 'structure'
    """
    name = name.lower()
    return name.endswith(".json") and "structure" in name


def slugify(name: str, idx: int) -> str:
    """
    Convert a folder name into a filesystem- and URL-safe slug.

    The slug is made unique by appending a zero-padded index.

    Examples
    --------
    >>> slugify("SrTiO3-relaxed", 1)
    'SrTiO3-relaxed-001'
    """
    base = re.sub(r"[^a-zA-Z0-9_-]+", "-", name) or "calc"
    return f"{base}-{idx:03d}"


# ---------------------------------------------------------------------------
# (Future) data extraction helpers from parsed JSON
# ---------------------------------------------------------------------------

def get_structure_data(parsed_data: dict) -> Optional[dict]:
    """
    Extract structure data from parsed output and format it for visualization.

    This function is designed to work with electronic-parsers style output,
    but is written defensively so that missing keys simply result in None.

    Parameters
    ----------
    parsed_data : dict
        Dictionary loaded from the parser's JSON output.

    Returns
    -------
    dict or None
        A dictionary containing structure information (e.g., pymatgen Structure
        as dict), or None if no usable structure was found or pymatgen is not
        available.
    """
    if not Structure:
        log.warning("Pymatgen not available, cannot process structure data.")
        return None

    log.debug("Attempting to extract structure data from parsed JSON...")
    structure = None
    try:
        # Strategy 1: direct pymatgen structure dict
        pmg_structure_dict = (
            parsed_data.get("results", {})
            .get("properties", {})
            .get("structure", {})
            .get("pymatgen_structure")
        )
        if pmg_structure_dict:
            structure = Structure.from_dict(pmg_structure_dict)
            log.debug("Found structure data (pymatgen format).")

        # Strategy 2: ASE atoms reconstruction or basic lattice/species/coords
        elif AseAtomsAdaptor:
            ase_atoms_dict = (
                parsed_data.get("results", {})
                .get("properties", {})
                .get("structure", {})
                .get("ase_atoms")
            )
            if ase_atoms_dict and hasattr(AseAtomsAdaptor, "get_atoms"):
                # NOTE: Actual ASE reconstruction depends on how it was serialized
                # and is left as a placeholder here.
                log.warning(
                    "ASE Atoms reconstruction from JSON not fully implemented; "
                    "structure extraction via ASE is currently a placeholder."
                )
            else:
                lattice_vectors = (
                    parsed_data.get("results", {})
                    .get("properties", {})
                    .get("structure", {})
                    .get("lattice_vectors")
                )
                species = (
                    parsed_data.get("results", {})
                    .get("properties", {})
                    .get("structure", {})
                    .get("species_at_sites")
                )
                coords = (
                    parsed_data.get("results", {})
                    .get("properties", {})
                    .get("structure", {})
                    .get("cartesian_site_positions")
                )
                coords_are_cartesian = True

                if lattice_vectors and species and coords:
                    log.debug(
                        "Found basic structure data (lattice vectors, species, coords)."
                    )
                    structure = Structure(
                        lattice=lattice_vectors,
                        species=species,
                        coords=coords,
                        coords_are_cartesian=coords_are_cartesian,
                    )
                else:
                    log.warning(
                        "Could not find sufficient structure data in parsed output."
                    )
                    return None

        if structure:
            return structure.as_dict()
        return None

    except Exception as exc:  # pragma: no cover - defensive
        log.error("Error processing structure data: %s", exc, exc_info=True)
        return None


def get_band_structure_data(parsed_data: dict) -> Optional[dict]:
    """
    Extract band structure data from parsed JSON.

    Currently implemented as a placeholder that returns any nested dictionary
    stored under 'pymatgen_bandstructure'.
    """
    log.debug("Attempting to extract band structure data from parsed JSON...")
    try:
        bs_dict = (
            parsed_data.get("results", {})
            .get("properties", {})
            .get("electronic", {})
            .get("band_structure", {})
            .get("pymatgen_bandstructure")
        )
        if bs_dict:
            log.debug("Found band structure data (pymatgen format).")
            # In future, you may reconstruct a BandStructureSymmLine and
            # return bs.as_dict() or a custom representation here.
            return bs_dict
        log.warning("Band structure data not found or format not recognized.")
        return None

    except Exception as exc:  # pragma: no cover - defensive
        log.error("Error processing band structure data: %s", exc, exc_info=True)
        return None


def get_dos_data(parsed_data: dict) -> Optional[dict]:
    """
    Extract density of states (DOS) data from parsed JSON.

    Currently implemented as a placeholder that returns any nested dictionary
    stored under 'pymatgen_dos'.
    """
    log.debug("Attempting to extract DOS data from parsed JSON...")
    try:
        dos_dict = (
            parsed_data.get("results", {})
            .get("properties", {})
            .get("electronic", {})
            .get("dos", {})
            .get("pymatgen_dos")
        )
        if dos_dict:
            log.debug("Found DOS data (pymatgen format).")
            # In future, you may reconstruct a CompleteDos and return
            # dos.as_dict() or a custom representation here.
            return dos_dict
        log.warning("DOS data not found or format not recognized.")
        return None

    except Exception as exc:  # pragma: no cover - defensive
        log.error("Error processing DOS data: %s", exc, exc_info=True)
        return None


def generate_markdown_embedding(data_file_path: Path, viz_type: str, component_id: str) -> str:
    """
    Generate a Markdown snippet to embed a visualization (React-based).

    This helper assumes your MkDocs site has JavaScript that scans for
    <div> elements with class 'react-viz-mount' and uses data attributes
    to mount the appropriate React component.

    Parameters
    ----------
    data_file_path : Path
        Path to the JSON data file (relative or absolute).
    viz_type : str
        Type of visualization (e.g. 'structure', 'bands', 'dos').
    component_id : str
        A unique HTML id for the mount point.

    Returns
    -------
    str
        Markdown string containing an HTML block.
    """
    relative_data_path = data_file_path.name

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


# ---------------------------------------------------------------------------
# Discover calculation folders
# ---------------------------------------------------------------------------

def discover_calculations(root: Path) -> List[CalculationFolder]:
    """
    Recursively scan `root` for folders containing a complete FAIR set.

    A folder is considered a valid FAIR calculation if it contains:

      - >= 1 parsed JSON  (filename: contains 'vasprun' and 'parsed', endswith '.json')
      - >= 1 summarized MD (filename: contains 'vasprun' and 'summarized', endswith '.md')
      - >= 1 structure JSON (filename: contains 'structure', endswith '.json')
      - len(parsed_json) == len(summarized_md)

    Only the first structure JSON is used for now.

    Parameters
    ----------
    root : Path
        Root directory to scan.

    Returns
    -------
    list[CalculationFolder]
        List of discovered calculation folders.
    """
    log.info("Scanning for calculation folders under: %s", root)
    results: List[CalculationFolder] = []

    for dirpath, _, files in os.walk(root):
        folder = Path(dirpath)

        parsed = [folder / f for f in files if is_parsed_json(f)]
        summarized = [folder / f for f in files if is_summarized_md(f)]
        structures = [folder / f for f in files if is_structure_json(f)]

        if not parsed or not summarized or not structures:
            continue
        if len(parsed) != len(summarized):
            continue

        parsed.sort()
        summarized.sort()

        structure_json = structures[0]

        results.append(
            CalculationFolder(
                folder=folder,
                parsed_json=parsed,
                summarized_md=summarized,
                structure_json=structure_json,
            )
        )

    log.info("Found %d valid calculation folder(s).", len(results))
    return results


# ---------------------------------------------------------------------------
# Build MkDocs nav tree from CalculationFolders
# ---------------------------------------------------------------------------

def build_nav_tree(calcs: List[CalculationFolder]) -> List[dict]:
    """
    Build a nested folder tree from CalculationFolder paths and convert it to
    a MkDocs 'nav' structure.

    Grouping is based on folder paths relative to the user's home directory.
    """
    home = Path.home()
    tree: dict = {}

    # Build a nested dictionary representing the folder structure
    for idx, calc in enumerate(calcs, start=1):
        slug = slugify(calc.name, idx)
        page_ref = f"calculations/{slug}.md"

        try:
            rel = calc.folder.relative_to(home)
        except ValueError:
            rel = calc.folder

        parts = list(rel.parts)
        node = tree
        for part in parts:
            node = node.setdefault(part, {})

        # mark leaf node
        node["__page__"] = page_ref

    def convert(node: dict) -> List[dict]:
        """
        Convert an internal tree node into a MkDocs nav list.

        Leaf nodes with only a page entry become {label: page}.
        Intermediate nodes become {label: [children...]}, optionally with
        an extra "(root)" entry if both a page and children exist.
        """
        nav_list: List[dict] = []

        for key, sub in sorted(node.items()):
            if key == "__page__":
                continue

            if "__page__" in sub and len(sub) == 1:
                nav_list.append({key: sub["__page__"]})
            else:
                nav_list.append({key: convert(sub)})

        if "__page__" in node and len(node) > 1:
            nav_list.append({"(root)": node["__page__"]})

        return nav_list

    return convert(tree)


# ---------------------------------------------------------------------------
# App base: copy documentation & styling once
# ---------------------------------------------------------------------------

def initialize_app_root(app_root: Path) -> None:
    """
    Initialize the persistent visualization application directory.

    On first run, the packaged documentation (mkdocs.yml, docs/, material/,
    macros.py, etc.) is copied into `app_root`. Subsequent runs reuse it.
    """
    if app_root.exists():
        return

    log.info("Initializing visualization application at: %s", app_root)
    app_root.parent.mkdir(parents=True, exist_ok=True)

    package_root = Path(__file__).resolve().parent.parent
    doc_root = package_root / "documentation"

    if not doc_root.exists():
        raise RuntimeError(f"Packaged documentation not found at {doc_root}")
    
    shutil.copytree(doc_root, app_root, dirs_exist_ok=True)
    log.info("Copied documentation from %s to %s", doc_root, app_root)


# ---------------------------------------------------------------------------
# Calculation pages & structure JSON copying
# ---------------------------------------------------------------------------

def write_calculation_pages(app_root: Path, calcs: List[CalculationFolder]) -> None:
    """
    Create Markdown pages for each CalculationFolder inside the app.

    For each calculation:
      - Copy a summarized Markdown file into docs/calculations/<slug>.md
      - Copy the structure JSON into docs/_structures/<slug>/<name>.json
      - Rewrite any structure_viewer("...") calls inside the summary so they
        point to the copied structure JSON path: /_structures/<slug>/<name>.json
      - Add a light metadata and structure info section based on parsed JSON
        and the structure JSON.
    """
    docs_dir = app_root / "docs"
    calc_dir = docs_dir / "calculations"
    struct_root = docs_dir / "_structures"

    # Reset calculations and structures folders
    if calc_dir.exists():
        shutil.rmtree(calc_dir)
    calc_dir.mkdir(parents=True, exist_ok=True)

    if struct_root.exists():
        shutil.rmtree(struct_root)
    struct_root.mkdir(parents=True, exist_ok=True)

    index_lines = [
        "# Calculations",
        "",
        "Detected FAIR calculation folders:",
        "",
        "| Name | Folder |",
        "|------|--------|",
    ]

    def fix_structure_macro(
        summary_text: str,
        struct_site_path: str,
        calc: CalculationFolder,
    ) -> str:
        """
        Replace structure_viewer(\"...\") calls with a path into docs/_structures.

        Parameters
        ----------
        summary_text : str
            Original summary Markdown.
        struct_site_path : str
            Root-relative path to the structure JSON, e.g.
            '/_structures/<slug>/structure.json'.
        calc : CalculationFolder
            The calculation this summary belongs to.
        """
        pattern = r'structure_viewer\(\s*[\'"][^\'"]+[\'"]\s*\)'
        replacement = f'structure_viewer("{struct_site_path}")'

        new_text = re.sub(pattern, replacement, summary_text)

        if new_text == summary_text:
            log.warning(
                "[fix_structure_macro] No structure_viewer() macro updated for %s",
                calc.folder,
            )
        else:
            log.info(
                "[fix_structure_macro] structure_viewer() macro updated for %s -> %s",
                calc.folder,
                struct_site_path,
            )

        return new_text

    # Generate pages
    for idx, calc in enumerate(calcs, start=1):
        slug = slugify(calc.name, idx)
        page_path = calc_dir / f"{slug}.md"

        index_lines.append(
            f"| [{calc.name}](./{slug}.md) | `{calc.rel_to_home}` |"
        )

        struct_target_dir = struct_root / slug
        struct_target_dir.mkdir(parents=True, exist_ok=True)

        struct_target = struct_target_dir / calc.structure_json.name
        try:
            shutil.copy2(calc.structure_json, struct_target)
            log.info(
                "Copied structure JSON for %s -> %s",
                calc.folder,
                struct_target,
            )
        except Exception as exc:
            log.error(
                "Failed to copy structure JSON for %s: %s",
                calc.folder,
                exc,
            )
            struct_target = None

        struct_site_path: Optional[str] = None
        if struct_target is not None:
            struct_site_path = f"/_structures/{slug}/{calc.structure_json.name}"

        lines: List[str] = []
        lines.append(f"# {calc.name}\n")
        lines.append(f"**Folder:** `{calc.rel_to_home}`\n")

        # Summary section
        lines.append("\n## Summary (from fair_summarized_vasprun.md)\n")

        try:
            summary_text = calc.summarized_md[0].read_text(encoding="utf-8")
            if struct_site_path:
                summary_text = fix_structure_macro(summary_text, struct_site_path, calc)
            lines.append(summary_text.strip() + "\n")
        except Exception as exc:
            lines.append(f"*Unable to read summary Markdown: {exc}*\n")

        # Parsed JSON metadata (lightweight)
        lines.append("\n## Calculation Metadata (parsed JSON)\n")

        parsed_obj = None
        try:
            parsed_obj = json.loads(
                calc.parsed_json[0].read_text(encoding="utf-8")
            )
        except Exception as exc:
            log.warning(
                "Unable to parse parsed JSON for %s: %s", calc.folder, exc
            )
            lines.append("*Unable to parse parsed JSON.*\n")

        if parsed_obj:
            code = parsed_obj.get("program", parsed_obj.get("code_name", ""))
            version = parsed_obj.get("program_version", parsed_obj.get("version", ""))
            entry = parsed_obj.get("entry_name", parsed_obj.get("entry", ""))
            workflow = parsed_obj.get("workflow_name", parsed_obj.get("workflow", ""))
            method = parsed_obj.get("method_name", parsed_obj.get("method", ""))

            lines.append("| Property | Value |")
            lines.append("|----------|-------|")
            if method:
                lines.append(f"| Method | {method} |")
            if workflow:
                lines.append(f"| Workflow | {workflow} |")
            if code:
                lines.append(f"| Program | {code} |")
            if version:
                lines.append(f"| Version | {version} |")
            if entry:
                lines.append(f"| Entry Name | {entry} |")
            lines.append("")

        # Basic structure info (optional, not a full viewer)
        lines.append("## Structure Info\n")

        struct_js = None
        if struct_target and struct_target.exists():
            try:
                struct_js = json.loads(struct_target.read_text(encoding="utf-8"))
            except Exception as exc:
                log.warning(
                    "Unable to parse copied structure JSON for %s: %s",
                    calc.folder,
                    exc,
                )

        formula = struct_js.get("formula", "N/A") if struct_js else "N/A"
        n_atoms = len(struct_js.get("sites", [])) if struct_js else "N/A"

        try:
            mat = struct_js["lattice"]["matrix"] if struct_js else None
            a, b, c = mat[0][0], mat[1][1], mat[2][2]
            lattice_str = f"{a:.3f}, {b:.3f}, {c:.3f}"
        except Exception:
            lattice_str = "N/A"

        lines.append("| Property | Value |")
        lines.append("|----------|-------|")
        lines.append(f"| Formula | {formula} |")
        lines.append(f"| Number of Atoms | {n_atoms} |")
        lines.append(f"| Lattice (a,b,c) | {lattice_str} |")
        lines.append("")

        page_path.write_text("\n".join(lines), encoding="utf-8")

    # ----------------------------------------------------------------------
    # SMART OVERVIEW PAGE — replaces simple table version
    # ----------------------------------------------------------------------
    overview = calc_dir / "index.md"

    with open(overview, "w", encoding="utf-8") as fh:
        fh.write("# Calculations Overview\n\n")
        fh.write("This page provides an overview of all discovered FAIR calculation folders.\n\n")

        for calc in calcs:
            fh.write(f"## {calc.name}\n")
            fh.write(f"**Folder:** `{calc.rel_to_home}`\n\n")

            folder = calc.folder

            # Collect all files
            all_md = list(folder.rglob("*.md"))
            all_html = list(folder.rglob("*.html"))
            struct_files = [p for p in folder.rglob("structure*.json")]
            other_json = [p for p in folder.rglob("*.json") if "structure" not in p.name]
            graphics = [p for p in folder.rglob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".svg")]

            # --- Markdown & HTML ---
            if all_md or all_html:
                fh.write("### Summary Pages\n\n")
                fh.write("| Path | Type | Size | Modified | Title |\n")
                fh.write("|------|------|------|-----------|--------|\n")
                for f in sorted(all_md + all_html):
                    rel = f.relative_to(folder).as_posix()
                    size = _hr_size(f.stat().st_size)
                    mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    ftype = "Markdown" if f.suffix.lower() == ".md" else "HTML"
                    title = _extract_title(f)
                    fh.write(f"| `{rel}` | {ftype} | {size} | {mtime} | {title} |\n")
                fh.write("\n")

            # --- Structure JSON ---
            if struct_files:
                fh.write("### Structure Data Files\n\n")
                fh.write("| Path | Size | Modified |\n")
                fh.write("|------|------|-----------|\n")
                for sf in sorted(struct_files):
                    rel = sf.relative_to(folder).as_posix()
                    size = _hr_size(sf.stat().st_size)
                    mtime = datetime.fromtimestamp(sf.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    fh.write(f"| `{rel}` | {size} | {mtime} |\n")
                fh.write("\n")

            # --- Other JSON ---
            if other_json:
                fh.write("### Data Files\n\n")
                fh.write("| Path | Size | Modified |\n")
                fh.write("|------|------|-----------|\n")
                for df in sorted(other_json):
                    rel = df.relative_to(folder).as_posix()
                    size = _hr_size(df.stat().st_size)
                    mtime = datetime.fromtimestamp(df.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    fh.write(f"| `{rel}` | {size} | {mtime} |\n")
                fh.write("\n")

            # --- Images ---
            if graphics:
                fh.write("### Graphics Files\n\n")
                fh.write("| Path | Size | Modified |\n")
                fh.write("|------|------|-----------|\n")
                for im in sorted(graphics):
                    rel = im.relative_to(folder).as_posix()
                    size = _hr_size(im.stat().st_size)
                    mtime = datetime.fromtimestamp(im.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                    fh.write(f"| `{rel}` | {size} | {mtime} |\n")
                fh.write("\n")

            fh.write("\n---\n\n")



# ---------------------------------------------------------------------------
# Update mkdocs.yml nav (ensure macros plugin + calculations section)
# ---------------------------------------------------------------------------

def update_mkdocs_nav(app_root: Path, calcs: List[CalculationFolder]) -> None:
    """
    Completely rebuild mkdocs.yml navigation:

      nav:
        - Home: index.md
        - calculations:
            - Overview: calculations/index.md
            - <dynamic tree>

    All previous nav entries are removed.
    """
    cfg_path = app_root / "mkdocs.yml"
    if not cfg_path.exists():
        raise RuntimeError(f"mkdocs.yml not found in {app_root}")

    import yaml

    raw = cfg_path.read_text(encoding="utf-8")
    cfg = yaml.safe_load(raw) or {}

    # =====================================================
    # 1. Ensure macros plugin exists
    # =====================================================
    plugins = cfg.get("plugins", [])
    new_plugins = []
    seen_macros = False

    for p in plugins:
        if isinstance(p, str) and p == "macros":
            new_plugins.append({"macros": {"modules": ["macros"]}})
            seen_macros = True
        elif isinstance(p, dict) and "macros" in p:
            entry = p["macros"] or {}
            mods = entry.get("modules", [])
            if "macros" not in mods:
                mods.append("macros")
            entry["modules"] = mods
            new_plugins.append({"macros": entry})
            seen_macros = True
        else:
            new_plugins.append(p)

    if not seen_macros:
        new_plugins.append({"macros": {"modules": ["macros"]}})

    cfg["plugins"] = new_plugins

    # =====================================================
    # 2. ERASE ENTIRE NAV → Replace with our custom nav
    # =====================================================
    new_nav = []

    # Home page always exists
    # Use index.md OR README.md depending on site
    if (app_root / "docs" / "README.md").exists():
        new_nav.append({"Home": "README.md"})
    elif (app_root / "docs" / "index.md").exists():
        new_nav.append({"Home": "index.md"})
    else:
        # Fallback — MkDocs will build but warn
        new_nav.append({"Home": "index.md"})

    # =====================================================
    # 3. Insert dynamic calculations section
    # =====================================================
    if calcs:
        dynamic_tree = build_nav_tree(calcs)
        new_nav.append({
            "calculations": [
                {"Overview": "calculations/index.md"},
                *dynamic_tree
            ]
        })

    cfg["nav"] = new_nav

    # Write yaml
    cfg_path.write_text(
        yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True),
        encoding="utf-8"
    )

    log.info("[update_mkdocs_nav] Replaced mkdocs.yml nav with fresh dynamic nav.")


# ---------------------------------------------------------------------------
# User prompt: rebuild vs reuse
# ---------------------------------------------------------------------------

def ask_rebuild_or_reuse(app_root: Path) -> bool:
    """
    Ask user whether to rescan and rebuild pages or reuse existing ones.

    Returns
    -------
    bool
        True  -> recalculate (rescan and regenerate)
        False -> reuse existing (no rescan)
    """
    print(f"\nA visualization application already exists at: {app_root}")
    print("What would you like to do?\n")
    print("  1) Recalculate everything (rescan home and rebuild calculation pages)")
    print("  2) Reuse existing pages (do NOT rescan)\n")

    try:
        choice = input("Select 1 or 2 : ").strip()
    except EOFError:
        # Non-interactive environment: default to rebuild
        return True

    if choice == "2":
        return False
    return True


# ---------------------------------------------------------------------------
# Public entry point called by CLI
# ---------------------------------------------------------------------------

def run_visualizer(root_scan: Optional[Path] = None, port: int = 8000) -> None:
    """
    Main entry point for the visualization app.

    Workflow
    --------
    1. Ensure persistent app root at ~/.fairtool/visualize_app.
    2. If it doesn't exist: create and initialize from packaged docs.
    3. If it exists: ask whether to rebuild (rescan) or reuse.
    4. If rebuilding:
         - Scan root_scan (default: HOME) for calculation folders.
         - Regenerate calculation pages.
         - Update MkDocs navigation.
    5. Start `mkdocs serve` from the app root and block until stopped.
    """
    app_root = APP_ROOT

    if not app_root.exists():
        initialize_app_root(app_root)
        rebuild = True
    else:
        rebuild = ask_rebuild_or_reuse(app_root)

    if rebuild:
        if root_scan is None:
            root_scan = Path.home()
        root_scan = root_scan.expanduser().resolve()

        log.info("[run_visualizer] Scanning root: %s", root_scan)
        calcs = discover_calculations(root_scan)
        if not calcs:
            log.warning("No valid calculation folders found under: %s", root_scan)

        write_calculation_pages(app_root, calcs)
        update_mkdocs_nav(app_root, calcs)

    mkdocs_cfg = app_root / "mkdocs.yml"
    log.info("[run_visualizer] mkdocs.yml path: %s", mkdocs_cfg)
    log.info(
        "[run_visualizer] Checking if macros.py exists: %s",
        (app_root / "macros.py").exists(),
    )
    log.info("[run_visualizer] Running mkdocs serve with cwd=%s", app_root)

    cmd = [
        sys.executable,
        "-m",
        "mkdocs",
        "serve",
        "-f",
        str(mkdocs_cfg),
        "--dev-addr",
        f"127.0.0.1:{port}",
    ]

    log.info("Launching MkDocs server at http://127.0.0.1:%d", port)
    log.info("Press Ctrl+C to stop the server.")
    try:
        subprocess.run(cmd, cwd=str(app_root), check=False)
    except KeyboardInterrupt:
        log.info("Visualization server stopped by user.")


def visualize_cli(port: int = 8000) -> None:
    """
    Thin wrapper for the Typer CLI.

    The `fair visualize` command should call this function.
    """
    run_visualizer(root_scan=None, port=port)
