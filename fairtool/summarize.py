# fairtool/summarize.py

"""Handles the generation of human-readable summaries."""

import json
import logging
from pathlib import Path
from typing import Optional, List, Tuple
import re
import pint
import numpy as np
u = pint.UnitRegistry()

log = logging.getLogger("fairtool")
ELEMENTARY_CHARGE_VALUE = 1.602176634e-19  # Elementary charge in Coulombs

# --- Helper Function for SCF Energy Extraction ---

def _extract_energy_lists(scf_iterations: List[dict], energy_key: str) -> Tuple[List[float], List[float]]:
    """
    Helper to safely extract energy lists from scf_iterations.
    
    Args:
        scf_iterations: The list of scf_iteration blocks.
        energy_key: The key of the energy to extract (e.g., "total", "xc").

    Returns:
        A tuple of (energies_in_eV, energies_divided_by_e).
    """
    energies_ev = []
    energies_divided = []
    for iteration in scf_iterations:
        # Safe traversal using .get()
        value = iteration.get('energy', {}).get(energy_key, {}).get('value')
        
        if value is not None:
            energies_ev.append(value)
            try:
                # We assume the value is in Joules if division is happening
                divided_energy = value / ELEMENTARY_CHARGE_VALUE
                energies_divided.append(divided_energy)
            except (ZeroDivisionError, TypeError):
                energies_divided.append(float('nan'))
        else:
            # Append NaN if value is missing for this iteration
            energies_ev.append(float('nan'))
            energies_divided.append(float('nan'))
    return energies_ev, energies_divided

# --- Unit Conversion Helper Functions (Unchanged) ---
# These functions are well-structured and remain the same.

def _scalar(x):
    """Unwrap 1-item list/tuple -> value; otherwise return as-is."""
    if isinstance(x, (list, tuple)) and len(x) == 1:
        return x[0]
    return x

def _as_qty(v, unit):
    """Attach a unit if v is numeric; return None for missing/sentinel."""
    v = _scalar(v)
    if v is None or v == "unavailable":
        return None
    try:
        return float(v) * unit
    except (TypeError, ValueError):
        return None

FIELD_UNITS = {
    "a": (u.m, u.angstrom, "Å", ".3f"),
    "b": (u.m, u.angstrom, "Å", ".3f"),
    "c": (u.m, u.angstrom, "Å", ".3f"),
    "alpha": (u.radian, u.degree, "°", ".0f"),
    "beta":  (u.radian, u.degree, "°", ".0f"),
    "gamma": (u.radian, u.degree, "°", ".0f"),
    "volume":          (u.m**3, u.angstrom**3, "Å^3", ".3f"),
    "atomic_density":  (1/u.m**3, 1/u.angstrom**3, "Å^-3", ".3f"),
    "mass_density":    (u.kg/u.m**3, u.kg/u.angstrom**3, "kg/Å^3", ".3e"),
}

def _convert_field(value, field, default=None, return_numeric=False):
    """
    Convert a raw value for a known field to its display unit and format.
    """
    spec = FIELD_UNITS.get(field)
    if not spec:
        raise KeyError(f"Unknown field '{field}'. Known: {sorted(FIELD_UNITS)}")
    from_u, to_u, symbol, fmt = spec
    q = _as_qty(value, from_u)
    if q is None:
        return default
    num = q.to(to_u).magnitude
    return num if return_numeric else f"{format(num, fmt)} {symbol}"

def _strip_parens(s: object, default: str = "unavailable") -> str:
    """Return the string with any parenthetical "( ... )" removed."""
    if s is None:
        return default
    s = str(s)
    if s == "":
        return default
    cleaned = re.sub(r"\s*\(.*?\)", "", s)
    return cleaned.strip() or default

def _format_field_numeric(value, field, default: str = "unavailable"):
    """Return a string formatted according to FIELD_UNITS for the given field."""
    try:
        num = _convert_field(value, field, default=None, return_numeric=True)
    except KeyError:
        return default
    if num is None:
        return default
    fmt = FIELD_UNITS.get(field, (None, None, None, ".3f"))[3]
    try:
        return format(num, fmt)
    except Exception:
        return default


# --- Main Summarization Function ---

def run_summarization(input_path: Path, output_dir: Path, template_path: Optional[str] = None):
    """
    Generates summary reports (e.g., Markdown) from parsed or analyzed data.

    Args:
        input_path: Path to input data (e.g., analysis_summary.csv, directory).
        output_dir: Directory to save the summary report.
        template_path: Optional path to a custom Jinja2 template file.
    """
    
    # --- Load Data ---
    try:
        log.info(f"Loading parsed data from: {input_path}")
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            log.info("Successfully loaded JSON data.")
    except Exception as e:
        log.error(f"Failed to load JSON: {e}")
        data = {} # Ensure data is a dict so .get() works
        
    # --- Markdown Summary Data Preparation ---
    if not data or not isinstance(data, dict):
        log.warning("No valid data loaded, cannot generate summary.")
        return

    # --- Safe Data Extraction ---
    # Use .get() and default to empty dicts/lists to prevent crashes
    run_list = data.get("run", [])
    run = run_list[0] if run_list else {}
    metadata = data.get("metadata", {})
    results = data.get("results", {})

    method = results.get("method", {})
    simulation = method.get("simulation", {})
    material = results.get("material", {})
    topology = material.get("topology", [])


    # **BUG FIX:** Initialize dictionaries to {} to prevent NameError/AttributeError
    sim_first_nested_data = {}
    sim_second_nested_data = {}
    t_original_data = {}
    t_cell_data = {}
    t_cell_data_sym = {}
    original_cell = {}
    cell_type_data = {}
    system_data = {}
    
    # Safely get sim data
    nested_dicts = [v for v in simulation.values() if isinstance(v, dict)]
    if len(nested_dicts) > 0:
        sim_first_nested_data = nested_dicts[0]
    if len(nested_dicts) > 1:
        sim_second_nested_data = nested_dicts[1]
    
    # Safely get topology data
    for obj in topology:
        if not isinstance(obj, dict):
            continue
        label = (obj.get("label") or "").strip().lower()
        if label == "original":
            t_original_data = obj
        elif label in ("primitive cell", "conventional cell"):
            t_cell_data = obj
            
    # Safely get sub-data *after* loops, from (potentially empty) dicts
    original_cell = t_original_data.get("cell", {})
    cell_type_data = t_cell_data.get("cell", {})
    t_cell_data_sym = t_cell_data.get("symmetry", {})

    # Safely get calculation data
    calculation = run.get("calculation", [])
    scf_iterations = calculation[0].get("scf_iteration", []) if calculation else []

    # Safely get k_mesh data
    runmethod = run.get("method", [])
    k_mesh = runmethod[0].get("k_mesh", {}) if runmethod else {}
    k_points = k_mesh.get("points", {})
    k_weights = k_mesh.get("weights", [])

    # --- **REFACTOR:** Simplified K-point table generation ---
    # table_md = ""
    # try:
    #     # k_points["re"] often has shape (3, N_points_total) or (3, Nk1, Nk2, Nk3)
    #     points_raw = np.array(k_points.get("re", []))
    #     k_weights_raw = np.array(k_weights).flatten()

    #     if points_raw.ndim > 0 and points_raw.shape[0] == 3:
    #         # Flatten all dimensions except the first (the xyz component)
    #         n_points = points_raw[0].size
    #         kx = points_raw[0].flatten()
    #         ky = points_raw[1].flatten()
    #         kz = points_raw[2].flatten()
            
    #         if len(k_weights_raw) == n_points:
    #             # Zip them together
    #             table_data = zip(kx, ky, kz, k_weights_raw)
    #             table_rows_str = []
    #             for row in table_data:
    #                 # Format: | 0.000 | 0.000 | 0.000 | 0.037 |
    #                 formatted_row = "|" + "|".join(f"{v:.2f}" for v in row) + "|"
    #                 table_rows_str.append(formatted_row)
    #                 # print (formatted_row)  # Debug print
    #             table_md = "\n".join(table_rows_str)
    #             log.info(f"Successfully processed {n_points} k-points for summary.")
    #         else:
    #             log.warning(f"K-point coordinate count ({n_points}) != weight count ({len(k_weights_raw)}). Skipping k-point table.")
    #     elif points_raw.size == 0:
    #          log.info("No k-point coordinates found in 're' key.")
    #     else:
    #         log.warning(f"Unexpected k-point 're' shape: {points_raw.shape}. Expected (3, ...). Skipping k-point table.")
    # except Exception as e:
    #     log.error(f"Failed to process k-points: {e}", exc_info=False)
    #     table_md = "    | Error processing k-points. |"

    # --- **REFACTOR:** Simplified SCF Energy Extraction using helper ---
    log.info("Extracting SCF energy data.")
    total_energies_ev, total_energies = _extract_energy_lists(scf_iterations, "total")
    xc_energies_ev, xc_energies = _extract_energy_lists(scf_iterations, "xc")
    free_energies_ev, free_energies = _extract_energy_lists(scf_iterations, "free")
    total_t0_energies_ev, total_t0_energies = _extract_energy_lists(scf_iterations, "total_t0")
    correction_hartree_energies_ev, correction_hartree_energies = _extract_energy_lists(scf_iterations, "correction_hartree")

    # --- Markdown Report Generation ---
    # The f-string is now safe because all data-access
    # keys (e.g., t_original_data) are guaranteed to be dicts.
    markdown_content = f"""
{f"# {metadata.get('entry_name', 'FAIR Parsed Report')}"}

<div class="grid cards" markdown>

{{{{ structure_viewer("fair-structure.json") }}}}

- ## Material Composition - {t_original_data.get("label", "unavailable")}

    | Property                     | Value                       |
    |------------------------------|-----------------------------|
    | Chemical formula (IUPAC)     | **{t_original_data.get("chemical_formula_iupac", "unavailable")}** |
    | Chemical formula (Reduced)   | **{t_original_data.get("chemical_formula_reduced", "unavailable")}** |
    | Label                       | **{t_original_data.get("label", "unavailable")}** |
    | Elements                    | {', '.join(t_original_data.get("elements", [])) or "unavailable"} |
    | Number of elements          | {len(t_original_data.get("elements", []))} |
    | Number of atoms             | {t_original_data.get("n_atoms", "unavailable")} |
    | Dimensionality              | **{t_original_data.get("dimensionality", "unavailable")}** |


</div>
    
<div class="grid cards" markdown>

- ## Lattice ({t_original_data.get("label", "unavailable")})

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a                | **{_format_field_numeric(original_cell.get("a"), "a")}** | Angstrom |
    | b                | **{_format_field_numeric(original_cell.get("b"), "b")}** | Angstrom |
    | c                | **{_format_field_numeric(original_cell.get("c"), "c")}** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha            | **{_format_field_numeric(original_cell.get("alpha"), "alpha")}** | Degrees |
    | Beta             | **{_format_field_numeric(original_cell.get("beta"), "beta")}** | Degrees |
    | Gamma            | **{_format_field_numeric(original_cell.get("gamma"), "gamma")}** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume           | **{_format_field_numeric(original_cell.get("volume"), "volume")}** | Å³ |
    | Mass density     | **{_format_field_numeric(original_cell.get("mass_density"), "mass_density")}** | kg / Å³ |
    | Atomic density   | **{_format_field_numeric(original_cell.get("atomic_density"), "atomic_density")}** | Å⁻³ |


- ## Lattice ({t_cell_data.get("label", "unavailable")})

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a                | **{_format_field_numeric(cell_type_data.get("a"), "a")}** | Angstrom |
    | b                | **{_format_field_numeric(cell_type_data.get("b"), "b")}** | Angstrom |
    | c                | **{_format_field_numeric(cell_type_data.get("c"), "c")}** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha            | **{_format_field_numeric(cell_type_data.get("alpha"), "alpha")}** | Degrees |
    | Beta             | **{_format_field_numeric(cell_type_data.get("beta"), "beta")}** | Degrees |
    | Gamma            | **{_format_field_numeric(cell_type_data.get("gamma"), "gamma")}** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume           | **{_format_field_numeric(cell_type_data.get("volume"), "volume")}** | Å³ |
    | Mass density     | **{_format_field_numeric(cell_type_data.get("mass_density"), "mass_density")}** | kg / Å³ |
    | Atomic density   | **{_format_field_numeric(cell_type_data.get("atomic_density"), "atomic_density")}** | Å⁻³ |

- ## Symmetry ({t_cell_data.get("label", "unavailable")})

    | Property                       | Value            |
    |---------------------------------|------------------|
    | Crystal system                  | **{t_cell_data_sym.get("crystal_system", "unavailable")}** |
    | Bravais lattice                 | **{t_cell_data_sym.get("bravais_lattice", "unavailable")}** |
    | Strukturbericht designation     | *{t_cell_data_sym.get("strukturbericht_designation", "unavailable")}* |
    | Space group symbol              | **{t_cell_data_sym.get("space_group_symbol", "unavailable")}** |
    | Space group number              | **{t_cell_data_sym.get("space_group_number", "unavailable")}** |
    | Point group                     | **{t_cell_data_sym.get("point_group", "unavailable")}** |
    | Hall number                     | **{t_cell_data_sym.get("hall_number", "unavailable")}** |
    | Hall symbol                     | **{t_cell_data_sym.get("hall_symbol", "unavailable")}** |
    | Prototype name                  | **{t_cell_data_sym.get("prototype_name", "unavailable")}** |
    | Prototype label aflow           | **{t_cell_data_sym.get("prototype_label_aflow", "unavailable")}** |

- ## K points information

    | Property               | Value |
    |------------------------|--------|
    | Dimensionality         | **{k_mesh.get("dimensionality", "unavailable")}** |
    | Sampling method        | **{k_mesh.get("sampling_method", "unavailable")}** |
    | Number of points       | **{k_mesh.get("n_points", "unavailable")}** |
    | Grid                   | **{k_mesh.get("grid", "unavailable")}** |
    
- ## Calculation Metadata

    | Property                   | Value                                                      |
    |----------------------------|------------------------------------------------------------|
    | **Method name** | {method.get('method_name', 'unavailable')}                 |
    | **Workflow name** | {method.get('workflow_name', 'unavailable')}               |
    | **Program name** | {simulation.get('program_name', 'unavailable')}            |
    | **Program version** | {_strip_parens(simulation.get('program_version', 'unavailable'))}         |
    | **Basis set type** | {sim_first_nested_data.get('basis_set_type', 'unavailable')}|
    | **Core electron treatment**| {sim_first_nested_data.get('core_electron_treatment', 'unavailable')}|
    | **Jacob's ladder** | {sim_first_nested_data.get('jacobs_ladder', 'unavailable')}|
    | **XC functional names** | {', '.join(sim_first_nested_data.get('xc_functional_names', [])) or 'unavailable'}|
    | **Code-specific tier** | {sim_second_nested_data.get('native_tier', 'unavailable')} |
    | **Basis set** | {sim_second_nested_data.get('basis_set', 'unavailable')}   |
    | **Entry type** | {metadata.get('entry_type', 'unavailable')}                |
    | **Entry name** | {metadata.get('entry_name', 'unavailable')}                |
    | **Mainfile** | {Path(metadata.get('mainfile', 'unavailable')).name}                 |

</div>
"""

# - ## k-points and weights

#     | kx | ky | kz | Weight |
#     |---|---|---|---|
# {table_md}


    # --- Save the markdown report ---
    # The output name is based on the *input* JSON file name
    base_name = input_path.stem # e.g., "fair_parsed_my_calc"
    summary_base_name = base_name.replace("fair_parsed_", "fair_summarized_")
    output_path = output_dir / f"{summary_base_name}.md"

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        log.info(f"Successfully generated markdown summary at: {output_path}")
    except Exception as e:
        log.error(f"Failed to write summary file: {e}")

    log.info("Summarization process completed.")