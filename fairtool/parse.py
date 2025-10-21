# fairtool/parse.py

"""Handles the parsing of calculation files."""

import json
import logging
import pint
from pathlib import Path
import subprocess
import time
# from electronic_parsers import auto
ELEMENTARY_CHARGE_VALUE = 1.602176634e-19  # Elementary charge in Coulombs, used for energy conversion if needed


log = logging.getLogger(__name__)
u = pint.UnitRegistry()

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
    json_output_path = output_dir / f"fair_parsed_{base_name}.json"
    md_output_path = output_dir / f"fair_parsed_{base_name}.md"

    # If not forcing, check existing parsed JSON metadata to decide whether to skip
    if not force:
        if json_output_path.exists():
            try:
                with open(json_output_path, 'r', encoding='utf-8') as jf:
                    existing = json.load(jf)
                fair_time = None
                if isinstance(existing, dict):
                    md = existing.get('metadata')
                    if isinstance(md, dict):
                        fair_time = md.get('fair_parse_time')
                try:
                    file_mtime = input_file.stat().st_mtime
                except Exception:
                    file_mtime = None

                if fair_time is not None and file_mtime is not None:
                    try:
                        if float(fair_time) >= float(file_mtime):
                            log.info(f"Skipping parse for {input_file.name} — unchanged since last parse (fair_parse_time={fair_time}).")
                            return
                    except Exception:
                        # If conversion/comparison fails, fall back to parsing
                        log.debug(f"Could not compare fair_parse_time ({fair_time}) with file mtime; will re-parse.")
            except Exception:
                # If reading the existing JSON fails, fall back to parsing
                log.debug(f"Could not read existing parsed JSON {json_output_path}; will re-parse.")
        elif md_output_path.exists():
            # If only a markdown output exists but not JSON, proceed with parsing
            log.debug(f"Found markdown output {md_output_path} but no JSON; will run parser to regenerate JSON.")

    log.info(f"Attempting to parse {input_file.name} ...")

    # The command to run, broken into a list for subprocess
    command = [
        "nomad", "parse",
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
        results_data = full_data.get("results",{})
        metadata_data = full_data.get("metadata",{})
        # calculation = run[0].get("calculation", {})
        # properties = full_data.get("metadata", {})

        # METHOD NAME
        method_data = results_data.get("method",{})
        method_name = method_data.get("method_name")

        # WORKFLOW NAME
        workflow_name = method_data.get("workflow_name")

        # PROGRAM VERSION
        simulation_data = method_data.get("simulation")
        program_version = simulation_data.get("program_version")

        # PROGRAM NAME
        program_name = simulation_data.get("program_name")
        
        # BASIS SET TYPE
        sim_first_nested_data = next(
            (v for v in simulation_data.values() if isinstance(v, dict)),
            None
        )
        basis_set_type = sim_first_nested_data.get("basis_set_type")

        # CORE ELECTRON TREATMENT
        core_electron_treatment = sim_first_nested_data.get("core_electron_treatment")

        # JACOBS LADDER
        jacobs_ladder = sim_first_nested_data.get("jacobs_ladder")

        # XC FUNCTIONAL NAMES
        xc_functional_names = sim_first_nested_data.get("xc_functional_names",[])
        # JACOBS LADDER
        jacobs_ladder_2 = sim_first_nested_data.get("jacobs_ladder")
        # CODE-SPECIFIC TIER
        precision_data = simulation_data.get("precision")
        code_specific_tier=precision_data.get("native_tier")
        # BASIS SET
        basis_set=precision_data.get("basis_set")

        # ENTRY TYPE
        entry_type = metadata_data.get("entry_type")
        # ENTRY NAME
        entry_name = metadata_data.get("entry_name")

        # MATERIAL

        material_data = results_data.get("material",{})
        topology_data = material_data.get("topology",[])

        # Separate objects by label
        t_original_data = None
        t_cell_data = None  # This will hold either primitive or conventional

        for obj in topology_data:
            if not isinstance(obj, dict):
                continue

            label = (obj.get("label") or "").strip().lower()

            if label == "original":
                t_original_data = obj

            elif label in ("primitive cell", "conventional cell"):
                t_cell_data = obj  # whichever exists, only one expected

        #log.info(f"T_CELL_DATA :   {t_cell_data}")
        #log.info(f"T_ORIGINAL_DATA :   {t_original_data}")

        #t_o_elements = len(t_original_data.get("elements",[]))
        #t_c_elements = t_cell_data.get("elements",[])
        
        #log.info(f"t_o_elements :   {t_o_elements}, len:{t_o_elements}")
        #log.info(f"t_c_elements :   {t_c_elements}, len:{len(t_c_elements)}")

        t_original_data_c = t_original_data.get("cell")
        t_cell_data_c = t_cell_data.get("cell")

        t_cell_data_sym = t_cell_data.get("symmetry")


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
            "metadata": {
                "method_name": method_name,
                "workflow_name": workflow_name,
                "program_version": program_version,
                "program_name": program_name,
                "basis_set_type": basis_set_type,
                "core_electron_treatment": core_electron_treatment,
                "jacobs_ladder": jacobs_ladder,
                # Safely format xc functional names: join whatever is available
                # (could be a list with 0,1, or many entries) or coerce to string.
                "xc_functional_names": (
                    ",".join([str(x) for x in xc_functional_names])
                    if isinstance(xc_functional_names, (list, tuple))
                    else (str(xc_functional_names) if xc_functional_names is not None else "")
                ),
                "jacobs_ladder": jacobs_ladder_2,
                "code_specific_tier": code_specific_tier,
                "basis_set": basis_set,
                "entry_type": entry_type,
                "entry_name": entry_name
            },
            "material": {
                "original":{
                    "description": t_original_data.get("description","unavailable"),
                    "composition":{
                        "chemical_formula_hill": t_original_data.get("chemical_formula_hill","unavailable"),
                        "chemical_formula_iupac": t_original_data.get("chemical_formula_iupac","unavailable"),
                        "structural_type": t_original_data.get("structural_type","unavailable"),
                        "label": t_original_data.get("label","unavailable"),
                        "material_id": t_original_data.get("material_id","unavailable"),
                        "elements": t_original_data.get("elements",[]),
                        "n_elements": len(t_original_data.get("elements",[])),
                        "n_atoms": t_original_data.get("n_atoms","unavailable"),
                    },
                    "cell": {
                        "a": convert_field(t_original_data_c.get("a","unavailable"),"a"),
                        "b": convert_field(t_original_data_c.get("b","unavailable"),"b"),
                        "c": convert_field(t_original_data_c.get("c","unavailable"),"c"),
                        "alpha": convert_field(t_original_data_c.get("alpha","unavailable"),"alpha"),
                        "beta": convert_field(t_original_data_c.get("beta","unavailable"),"beta"),
                        "gamma": convert_field(t_original_data_c.get("gamma","unavailable"),"gamma"),
                        "volume": convert_field(t_original_data_c.get("volume","unavailable"),"volume"),
                        "atomic_density": convert_field(t_original_data_c.get("atomic_density","unavailable"),"atomic_density"),
                        "mass_density": convert_field(t_original_data_c.get("mass_density","unavailable"),"mass_density")
                    }
                },
                f'{t_cell_data.get("label")}':{
                   "description": t_cell_data.get("description","unavailable"),
                    "composition":{
                        "chemical_formula_hill": t_cell_data.get("chemical_formula_hill","unavailable"),
                        "chemical_formula_iupac": t_cell_data.get("chemical_formula_iupac","unavailable"),
                        "structural_type": t_cell_data.get("structural_type","unavailable"),
                        "label": t_cell_data.get("label","unavailable"),
                        "material_id": t_cell_data.get("material_id","unavailable"),
                        "elements": t_cell_data.get("elements",[]),
                        "n_elements": len(t_cell_data.get("elements",[])),
                        "n_atoms": t_cell_data.get("n_atoms","unavailable"),
                    },
                    "cell": {
                        "a": convert_field(t_cell_data_c.get("a","unavailable"),"a"),
                        "b": convert_field(t_cell_data_c.get("b","unavailable"),"b"),
                        "c": convert_field(t_cell_data_c.get("c","unavailable"),"c"),
                        "alpha": convert_field(t_cell_data_c.get("alpha","unavailable"),"alpha"),
                        "beta": convert_field(t_cell_data_c.get("beta","unavailable"),"beta"),
                        "gamma": convert_field(t_cell_data_c.get("gamma","unavailable"),"gamma"),
                        "volume": convert_field(t_cell_data_c.get("volume","unavailable"),"volume"),
                        "atomic_density": convert_field(t_cell_data_c.get("atomic_density","unavailable"),"atomic_density"),
                        "mass_density": convert_field(t_cell_data_c.get("mass_density","unavailable"),"mass_density")

                    },
                    "symmetry": {
                        "crystal_system" : t_cell_data_sym.get("crystal_system","unavailable"),
                        "hall_number" : t_cell_data_sym.get("hall_number","unavailable"),
                        "strukturbericht_designation" : t_cell_data_sym.get("strukturbericht_designation","unavailable"),
                        "space_group_symbol" : t_cell_data_sym.get("space_group_symbol","unavailable"),
                        "space_group_number" : t_cell_data_sym.get("space_group_number","unavailable"),
                        "point_group" : t_cell_data_sym.get("point_group","unavailable"),
                        "hall_number" : t_cell_data_sym.get("hall_number","unavailable"),
                        "hall_symbol" : t_cell_data_sym.get("hall_symbol","unavailable"),
                        "prototype_name" : t_cell_data_sym.get("prototype_name","unavailable"),
                        "prorotype_label_aflow" : t_cell_data_sym.get("prorotype_label_aflow","unavailable")
                    }
                }
            } ,
            #"method": cleaned_method_data, #method information parameters
            "domain": full_data.get("metadata", {}).get("domain"),
            "scf_total_energies_ev": total_energies_ev, # Add the extracted energies here
            "unit": "eV" # Explicitly state the unit

        }


        # Remove keys with None values for a cleaner output
        filtered_data = {k: v for k, v in filtered_data.items() if v is not None}

        # Record the input file's modification time so subsequent CLI calls
        # can decide whether re-parsing is necessary.
        try:
            parse_mtime = input_file.stat().st_mtime
        except Exception:
            parse_mtime = time.time()

        # --- Save as JSON ---
        # Attach the parse timestamp (epoch seconds) under metadata so the CLI
        # can skip parsing when the original file is unchanged.
        if "metadata" not in filtered_data or not isinstance(filtered_data["metadata"], dict):
            filtered_data["metadata"] = {}
        filtered_data["metadata"]["fair_parse_time"] = parse_mtime

        log.info(f"Saving filtered parsed data to {json_output_path}")
        try:
            with open(json_output_path, 'w', encoding='utf-8') as f:
                json.dump(filtered_data, f, indent=2,ensure_ascii=False)
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

