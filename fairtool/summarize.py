# fairtool/summarize.py

"""Handles the generation of human-readable summaries."""

import json
import logging
from pathlib import Path
from typing import Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import re
import pint
import numpy as np
u = pint.UnitRegistry()

log = logging.getLogger("fairtool")
ELEMENTARY_CHARGE_VALUE = 1.602176634e-19  # Elementary charge in Coulombs, used for energy conversion if needed
def run_summarization(input_path: Path, output_dir: Path, template_path: Optional[str] = None):
    """
    Generates summary reports (e.g., Markdown) from parsed or analyzed data.

    Args:
        input_path: Path to input data (e.g., analysis_summary.csv, directory).
        output_dir: Directory to save the summary report.
        template_path: Optional path to a custom Jinja2 template file.
    """
    
    # --- Load Data for Summarization Markdown (JSON only) ---
    try:
        log.info(f"Loading parsed data from: {input_path}")
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            log.info("Successfully loaded JSON data.")

        
    except Exception as e:
        log.error(f"Failed to load JSON: {e}")
        items = []

   
    # --- Markdown Summary Data Preparation ---

    
    # Prepare sections for the markdown report
    if data and isinstance(data, dict):
        #log.info("Data is valid and of type dict.")
        # main tree sections

        run = data.get("run", {})
        metadata = data.get("metadata", {})
        results = data.get("results", {})

        # getting into results
        method = results.get("method", {})
        simulation = method.get("simulation", {})

        # getting into simulation data
        nested_dicts = [v for v in simulation.values() if isinstance(v, dict)]
        sim_first_nested_data = nested_dicts[0] if len(nested_dicts) > 0 else None
        sim_second_nested_data = nested_dicts[1] if len(nested_dicts) > 1 else None
        
        #log.info(f"{sim_second_nested_data.keys()}")
        
        # material topology data
        material = results.get("material", {})
        topology = material.get("topology", {})

        for obj in topology:
            if not isinstance(obj, dict):
                continue

            label = (obj.get("label") or "").strip().lower()

            if label == "original":
                t_original_data = obj

            elif label in ("primitive cell", "conventional cell"):
                t_cell_data = obj  # whichever exists, only one expected
         

        #log.info(f"{t_original_data}")
        #log.info(f"{t_cell_data}")

        original_cell = t_original_data.get("cell")
        #log.info(f"Original cell data extracted: {original_cell}")
        cell_type_data = t_cell_data.get("cell")
        #log.info(f"Cell type data extracted: {cell_type_data}")

        t_cell_data_sym = t_cell_data.get("symmetry")
        #log.info(f"Symmetry data extracted: {t_cell_data_sym}")

        # getting into calculation data
        calculation = run[0].get("calculation", {})
        #log.info(f"Calculation data extracted: {calculation}")
        scf_iterations = calculation[0].get("scf_iteration", {})
        #log.info(f"SCF iteration data extracted: {scf_iterations}")

        # Extract k_mesh  points xyz and weights
        runmethod = run[0].get("method", {})
        k_mesh = runmethod[0].get("k_mesh", {})
        k_points = k_mesh.get("points", {})
        k_weights = k_mesh.get("weights", [])

                
        #log.info(f"k_mesh extracted: {k_mesh}")
        #log.info(f"K-points extracted: {k_points}")
        #log.info(f"K-weights extracted: {len(k_weights)}")


        points_raw = np.array(k_points.get("re", []))
        #log.info(f"Raw k_points array: {points_raw}")
        #log.info(f"Raw k_points shape: {np.array(k_points.get('re', [])).shape}")

        #log.info(f"specific k-point: {(points_raw[1][1][1][1])}")
        #log.info(f"k-point: {(points_raw)}")
        # Helper function to extract k-point data and format for markdown
        def extract_kpoints(points_raw, k_weights):
            """
            Extracts k-point coordinates and weights from nested arrays.
            Returns a list of formatted markdown table rows.
            """
            index = 0
            table = []
            table_x = []
            table_y = []
            table_z = []
            n_kx_layers = len(points_raw)
            #log.info(f"k_mesh has {n_kx_layers} kx layers (first dimension).")

            for i, kx_layer in enumerate(points_raw):  # 1st level: kx
                n_ky_rows = len(kx_layer)
                #log.info(f"  kx layer {i} has {n_ky_rows} ky rows.")

                for j, ky_row in enumerate(kx_layer):  # 2nd level: ky
                    n_kz_points = len(ky_row)
                    #log.info(f"    ky row {j} in kx layer {i} has {n_kz_points} kz points.")

                    for k, kz_points in enumerate(ky_row):  # 3rd level: kz
                        n_components = len(kz_points)
                        # Each k value corresponds to a coordinate or weight
                        for l in range(n_components):
                            value = kz_points[l]
                            # Format value to at most 6 decimals
                            try:
                                value_fmt = float(f"{float(value):.6f}")
                            except (TypeError, ValueError):
                                value_fmt = value
                            #log.info(f"      Component {l} of k-point at ({i},{j},{k}): {value_fmt}")
                            if i == 0:
                                table_x.append(value_fmt)
                            elif i == 1:
                                table_y.append(value_fmt)
                            elif i == 2:
                                table_z.append(value_fmt)
                            index += 1
            
            table.append(table_x)
            table.append(table_y)
            table.append(table_z)
            table.append(k_weights)

            return table

        def revert_kpoints(points_raw):
            """
            Converts a list of 4 lists [kx[], ky[], kz[], w[]]
            into a list of [kx, ky, kz, w] rows.
            """
            if len(points_raw) != 4:
                raise ValueError("Expected 4 lists: [kx, ky, kz, w]")

            kx, ky, kz, w = points_raw

            n_points = len(kx)
            if not (len(ky) == len(kz) == len(w) == n_points):
                raise ValueError("All sublists must have the same length.")

            combined = []
            for i in range(n_points):
                combined.append([kx[i], ky[i], kz[i], w[i]])

            return combined

        # Extract and format k-point table rows
        table_rows = extract_kpoints(points_raw, k_weights)
        #log.info(f"Extracted k-point table rows: {table_rows}")

        # Revert the k-point table rows back to the original format
        table_md = revert_kpoints(table_rows)

        # Convert each row (list of floats) into a formatted markdown string
        
        table_md = "\n".join(["    | " + " | ".join(map(str, row)) + " |" for row in table_md])



        # Wrap the table in a markdown container
        #table_md = f"```\n{table_md}\n```"

        # Extract SCF energy data on 5 different lists which will be used to create markdown scatter plots
        # These lists will hold energy values in eV and converted values if needed with ELEMENTARY_CHARGE_VALUE
        total_energies = []
        total_energies_ev = []
        xc_energies = []
        xc_energies_ev = []
        free_energies = []
        free_energies_ev = []
        total_t0_energies = []
        total_t0_energies_ev = []
        correction_hartree_energies = []
        correction_hartree_energies_ev = []
        for iteration in scf_iterations:
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
            else:
                total_energies_ev.append(float('nan'))
                total_energies.append(float('nan'))
            if 'energy' in iteration and 'xc' in iteration['energy'] and 'value' in iteration['energy']['xc']:
                xc_energies_ev.append(iteration['energy']['xc']['value'])
                try:
                    divided_energy = iteration['energy']['xc']['value'] / ELEMENTARY_CHARGE_VALUE
                    xc_energies.append(divided_energy)
                except ZeroDivisionError:
                    log.warning(f"Skipping division by zero for energy value: {iteration['energy']['xc']['value']}")
                    xc_energies.append(float('nan')) # Append NaN for invalid division
            else:
                xc_energies_ev.append(float('nan'))
                xc_energies.append(float('nan'))
            if 'energy' in iteration and 'free' in iteration['energy'] and 'value' in iteration['energy']['free']:
                free_energies_ev.append(iteration['energy']['free']['value'])
                try:
                    divided_energy = iteration['energy']['free']['value'] / ELEMENTARY_CHARGE_VALUE
                    free_energies.append(divided_energy)
                except ZeroDivisionError:
                    log.warning(f"Skipping division by zero for energy value: {iteration['energy']['free']['value']}")
                    free_energies.append(float('nan')) # Append NaN for invalid division
            else:
                free_energies_ev.append(float('nan'))
                free_energies.append(float('nan'))
            if 'energy' in iteration and 'total_t0' in iteration['energy'] and 'value' in iteration['energy']['total_t0']:
                total_t0_energies_ev.append(iteration['energy']['total_t0']['value'])
                try:
                    divided_energy = iteration['energy']['total_t0']['value'] / ELEMENTARY_CHARGE_VALUE
                    total_t0_energies.append(divided_energy)
                except ZeroDivisionError:
                    log.warning(f"Skipping division by zero for energy value: {iteration['energy']['total_t0']['value']}")
                    total_t0_energies.append(float('nan')) # Append NaN for invalid division
            else:
                total_t0_energies_ev.append(float('nan'))
                total_t0_energies.append(float('nan'))
            if 'energy' in iteration and 'correction_hartree' in iteration['energy'] and 'value' in iteration['energy']['correction_hartree']:
                correction_hartree_energies_ev.append(iteration['energy']['correction_hartree']['value'])
                try:
                    divided_energy = iteration['energy']['correction_hartree']['value'] / ELEMENTARY_CHARGE_VALUE
                    correction_hartree_energies.append(divided_energy)
                except ZeroDivisionError:
                    log.warning(f"Skipping division by zero for energy value: {iteration['energy']['correction_hartree']['value']}")
                    correction_hartree_energies.append(float('nan')) # Append NaN for invalid division
            else:
                correction_hartree_energies_ev.append(float('nan'))
                correction_hartree_energies.append(float('nan'))

        #log.info("Successfully extracted SCF energy data.")
        #log.info(f"Total Energies (eV): {total_energies_ev}")
        #log.info(f"Free Energies (eV): {free_energies_ev}")
        #log.info(f"Total_t0 Energies (eV): {total_t0_energies_ev}")

         ##CONVERSION OF CELL DATA UNITS

        # --- cleans the value from lists or tuples
        def scalar(x):
            """Unwrap 1-item list/tuple -> value; otherwise return as-is."""
            if isinstance(x, (list, tuple)) and len(x) == 1:
                return x[0]
            return x
        # --- converts a numeric value to a pint quantity
        def as_qty(v, unit):
            """Attach a unit if v is numeric; return None for missing/sentinel."""
            v = scalar(v)
            if v is None or v == "unavailable":
                return None
            try:
                return float(v) * unit
            except (TypeError, ValueError):
                return None

        # --- field-specific spec (SI -> display units)
        FIELD_UNITS = {
            # lattice lengths
            "a": (u.m, u.angstrom, "Å", ".3f"),
            "b": (u.m, u.angstrom, "Å", ".3f"),
            "c": (u.m, u.angstrom, "Å", ".3f"),
            # angles
            "alpha": (u.radian, u.degree, "°", ".0f"),
            "beta":  (u.radian, u.degree, "°", ".0f"),
            "gamma": (u.radian, u.degree, "°", ".0f"),
            # bulk properties
            "volume":          (u.m**3, u.angstrom**3, "Å^3", ".3f"),
            "atomic_density":  (1/u.m**3, 1/u.angstrom**3, "Å^-3", ".3f"),
            "mass_density":    (u.kg/u.m**3, u.kg/u.angstrom**3, "kg/Å^3", ".3e"),
        }
        # --- convert Lattice field values
        def convert_field(value, field, default=None, return_numeric=False):
            """
            Convert a raw value for a known field to its display unit and format.
            Returns a formatted string like '7.311 Å' by default,
            or the numeric value if return_numeric=True.
            """
            spec = FIELD_UNITS.get(field)
            if not spec:
                raise KeyError(f"Unknown field '{field}'. Known: {sorted(FIELD_UNITS)}")
            from_u, to_u, symbol, fmt = spec
            q = as_qty(value, from_u)
            if q is None:
                return default
            num = q.to(to_u).magnitude
            return num if return_numeric else f"{format(num, fmt)} {symbol}"
        

        # --- utility: strip parenthetical content
        def strip_parens(s: object, default: str = "unavailable") -> str:
            """Return the string with any parenthetical "( ... )" removed.

            If s is None or equals the sentinel, return default.
            """
            if s is None:
                return default
            s = str(s)
            if s == "":
                return default
            # remove any parenthetical group and surrounding whitespace
            cleaned = re.sub(r"\s*\(.*?\)", "", s)
            return cleaned.strip() or default

        # --- utility: format numeric field according to FIELD_UNITS
        def format_field_numeric(value, field, default: str = "unavailable"):
            """Return a string formatted according to FIELD_UNITS for the given field.

            If the value is missing or can't be converted, return `default`.
            """
            try:
                num = convert_field(value, field, default=None, return_numeric=True) ## we return numeric only in the function
            except KeyError:
                return default
            if num is None:
                return default
            fmt = FIELD_UNITS.get(field, (None, None, None, ".3f"))[3]
            try:
                return format(num, fmt)
            except Exception:
                return default




        
        # Find the conventional/primitive cell data
        #cell_type_data = next((v for k, v in material.items() if "cell" in k.lower()), {})
        #symmetry_data = cell_type_data.get("symmetry", {}) if cell_type_data else {}
        #log.info("Successfully extracted data sections.")

        # Create markdown content
        markdown_content = f"""
{f"# {metadata.get('entry_name', 'FAIR Parsed Report')}"}

<div class="grid cards" markdown>

- ## Calculation Metadata

    | Property                   | Value                                                      |
    |----------------------------|------------------------------------------------------------|
    | **Method name**            | {method.get('method_name', 'unavailable')}                 |
    | **Workflow name**          | {method.get('workflow_name', 'unavailable')}               |
    | **Program name**           | {simulation.get('program_name', 'unavailable')}            |
    | **Program version**        | {strip_parens(simulation.get('program_version', 'unavailable'))}         |
    | **Basis set type**         | {sim_first_nested_data.get('basis_set_type', 'unavailable')}|
    | **Core electron treatment**| {sim_first_nested_data.get('core_electron_treatment', 'unavailable')}|
    | **Jacob's ladder**         | {sim_first_nested_data.get('jacobs_ladder', 'unavailable')}|
    | **XC functional names**    | {', '.join(sim_first_nested_data.get('xc_functional_names', [])) or 'unavailable'}|
    | **Code-specific tier**     | {sim_second_nested_data.get('native_tier', 'unavailable')} |
    | **Basis set**              | {sim_second_nested_data.get('basis_set', 'unavailable')}   |
    | **Entry type**             | {metadata.get('entry_type', 'unavailable')}                |
    | **Entry name**             | {metadata.get('entry_name', 'unavailable')}                |
    | **Authors**                | Ravindra Shinde                                            |
    | **Mainfile**               | {Path(metadata.get('mainfile', 'unavailable')).name}                 |
    | **Last processing time**   | {datetime.fromisoformat(metadata.get('compilation_datetime', 'unavailable')).strftime('%m/%d/%Y, %I:%M:%S %p') if metadata.get('compilation_datetime') else 'unavailable'}     |
    | **Processing version**     | 1.0.0                                                       |
</div>

<div class="grid cards" markdown>

- ## Material Composition - {t_original_data.get("label")}

    | Property                     | Value                       |
    |------------------------------|-----------------------------|
    | Chemical formula (Hill)      | {t_original_data.get("chemical_formula_hill", "unavailable")} |
    | Chemical formula (IUPAC)     | {t_original_data.get("chemical_formula_iupac", "unavailable")} |
    | Structural type             | **{t_original_data.get("structural_type", "unavailable")}** |
    | Label                       | **{t_original_data.get("label", "unavailable")}** |
    | Material ID                 | {t_original_data.get("material_id", "unavailable")} |
    | Elements                    | {', '.join(t_original_data.get("elements", [])) or "unavailable"} |
    | Number of elements          | {len(t_original_data.get("elements", []))} |
    | Number of atoms             | {t_original_data.get("n_atoms", "unavailable")} |

- ## Lattice ({t_original_data.get("label")})

    | Lattice vectors   | Value     | Units |
    |------------------|-----------|-------|
    | a                | **{format_field_numeric(original_cell.get("a", "unavailable"), "a")}** | Angstrom |
    | b                | **{format_field_numeric(original_cell.get("b", "unavailable"), "b")}** | Angstrom |
    | c                | **{format_field_numeric(original_cell.get("c", "unavailable"), "c")}** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha            | **{format_field_numeric(original_cell.get("alpha", "unavailable"), "alpha")}** | Degrees |
    | Beta             | **{format_field_numeric(original_cell.get("beta", "unavailable"), "beta")}**  | Degrees |
    | Gamma            | **{format_field_numeric(original_cell.get("gamma", "unavailable"), "gamma")}** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume           | **{format_field_numeric(original_cell.get("volume", "unavailable"), "volume")}** | Å³ |
    | Mass density     | **{format_field_numeric(original_cell.get("mass_density","unavailable"), "mass_density")}** | kg / Å³ |
    | Atomic density   | **{format_field_numeric(original_cell.get("atomic_density", "unavailable"), "atomic_density")}** | Å⁻³ |

- ## Material Composition - {t_cell_data.get("label")}
    
    | Property                     | Value                       |
    |------------------------------|-----------------------------|
    | Chemical formula (Hill)      | {t_cell_data.get("chemical_formula_hill", "unavailable")} |
    | Chemical formula (IUPAC)     | {t_cell_data.get("chemical_formula_iupac", "unavailable")} |
    | Structural type             | **{t_cell_data.get("structural_type", "unavailable")}** |
    | Label                       | **{t_cell_data.get("label", "unavailable")}** |
    | Material ID                 | {t_cell_data.get("material_id", "unavailable")} |
    | Elements                    | {', '.join(t_cell_data.get("elements", [])) or "unavailable"} |
    | Number of elements          | {len(t_cell_data.get("elements", []))} |
    | Number of atoms             | {t_cell_data.get("n_atoms", "unavailable")} |

- ## Lattice ({t_cell_data.get("label")})

    | Lattice vectors   | Value     | Units |
    |------------------|-----------|-------|
    | a                | **{format_field_numeric(cell_type_data.get("a", "unavailable"), "a")}** | Angstrom |
    | b                | **{format_field_numeric(cell_type_data.get("b", "unavailable"), "b")}** | Angstrom |
    | c                | **{format_field_numeric(cell_type_data.get("c", "unavailable"), "c")}** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha            | **{format_field_numeric(cell_type_data.get("alpha", "unavailable"), "alpha")}** | Degrees |
    | Beta             | **{format_field_numeric(cell_type_data.get("beta", "unavailable"), "beta")}**  | Degrees |
    | Gamma            | **{format_field_numeric(cell_type_data.get("gamma", "unavailable"), "gamma")}** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume           | **{format_field_numeric(cell_type_data.get("volume", "unavailable"), "volume")}** | Å³ |
    | Mass density     | **{format_field_numeric(cell_type_data.get("mass_density", "unavailable"), "mass_density")}** | kg / Å³ |
    | Atomic density   | **{format_field_numeric(cell_type_data.get("atomic_density", "unavailable"), "atomic_density")}** | Å⁻³ |

- ## Symmetry({t_cell_data.get("label")})

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
</div>
<div class="grid cards" markdown>

- ## K points information

    | Property               | Value |
    |------------------------|--------|
    | Dimensionality         | **{k_mesh.get("type", "unavailable")}** |
    | Sampling method        | **{k_mesh.get("sampling_method", "unavailable")}** |
    | Number of points       | **{k_mesh.get("n_points", "unavailable")}** |
    | Grid                   | **{k_mesh.get("grid", "unavailable")}** |

- ## K points and Weights

    | kx | ky | kz | Weight |
    |----|----|----|--------|
{table_md}

</div>
"""
        


        # Determine output file path (Formulation IUPAC if available)
        #if t_original_data.get("chemical_formula_iupac"):
        #    output_path = output_dir / f"{t_original_data.get('chemical_formula_iupac')}_summary.md"
        #else:
        #    output_path = output_dir / f"{input_path.stem}_summary.md"
        #

        # Save the markdown report
        output_path = output_dir / f"{input_path.stem}_summary.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        log.info(f"Successfully generated markdown summary at: {output_path}")
    else:
        log.warning("No data available to generate markdown summary")
        program_version = simulation_data.get("program_version")

  
    log.info("Summarization process completed.")




