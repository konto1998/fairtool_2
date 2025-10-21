import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from fairtool.parse import run_parser


def test_parse_vasprun_example_matches_reference(tmp_path, monkeypatch):
    """
    Use the real example vasprun.xml in tests/VASP/example01 as input.
    Mock the `nomad parse` subprocess to return the provided reference JSON
    (tests/VASP/example01/fair_parsed_vasprun.json) as stdout, then run the
    parser and compare the produced JSON to the reference (ignoring
    metadata.fair_parse_time which is generated at parse time).
    """
    repo_tests = Path(__file__).parent
    example_dir = repo_tests / "VASP" / "example01"
    input_file = example_dir / "vasprun.xml"
    assert input_file.exists(), f"Expected example file at {input_file}"

    ref_json_file = example_dir / "fair_parsed_vasprun.json"
    reference = None
    if ref_json_file.exists():
        reference = json.loads(ref_json_file.read_text(encoding='utf-8'))

    # Build a NOMAD-like raw JSON that contains the fields run_parser expects
    # Use the reference metadata and scf energies to populate necessary fields if available.
    if reference:
        full_data = {
            "results": {
                "method": {
                    "method_name": reference["metadata"]["method_name"],
                    "workflow_name": reference["metadata"]["workflow_name"],
                    "simulation": {
                        "program_version": reference["metadata"]["program_version"],
                        "program_name": reference["metadata"]["program_name"],
                        # simulation may include a nested dict with details
                        "sim_details": {
                            "basis_set_type": reference["metadata"].get("basis_set_type"),
                            "core_electron_treatment": reference["metadata"].get("core_electron_treatment"),
                            "jacobs_ladder": reference["metadata"].get("jacobs_ladder"),
                            "xc_functional_names": (lambda s: (s.split(",") if s else [])) (reference["metadata"].get("xc_functional_names"))
                        },
                        # precision block expected separately
                        "precision": {
                            "native_tier": reference["metadata"].get("code_specific_tier"),
                            "basis_set": reference["metadata"].get("basis_set")
                        }
                    }
                },
                "material": {
                    "topology": [
                        {"label": "original", "cell": {"a": 7.311e-10, "b": 7.311e-10, "c": 7.311e-10, "alpha": 1.0471975512, "beta": 1.0471975512, "gamma": 1.0471975512, "volume": 276.268e-30, "atomic_density": 0.036 * 1e30, "mass_density": 4.73e-27 * 1e30}, "description": "A representative system chosen from the original simulation.", "chemical_formula_hill": reference["material"]["original"]["composition"]["chemical_formula_hill"], "elements": reference["material"]["original"]["composition"]["elements"], "n_atoms": reference["material"]["original"]["composition"]["n_atoms"]},
                        {"label": "conventional cell", "cell": {"a": 10.339e-10, "b": 10.339e-10, "c": 10.339e-10, "alpha": 1.5707963268, "beta": 1.5707963268, "gamma": 1.5707963268, "volume": 1105.074e-30, "atomic_density": 0.036 * 1e30, "mass_density": 4.73e-27 * 1e30}, "description": reference["material"]["conventional cell"]["description"], "chemical_formula_hill": reference["material"]["conventional cell"]["composition"]["chemical_formula_hill"], "elements": reference["material"]["conventional cell"]["composition"]["elements"], "n_atoms": reference["material"]["conventional cell"]["composition"]["n_atoms"], "symmetry": reference["material"]["conventional cell"].get("symmetry", {})}
                    ]
                }
            },
            "run": [{"calculation": [{"scf_iteration": []}]}],
            "metadata": {"entry_type": reference["metadata"].get("entry_type"), "entry_name": reference["metadata"].get("entry_name"), "domain": reference.get("domain")}
        }
    else:
        # Reference missing: provide a minimal full_data payload with generic values
        full_data = {
            "results": {
                "method": {
                    "method_name": "DFT",
                    "workflow_name": "SinglePoint",
                    "simulation": {
                        "program_version": "unknown",
                        "program_name": "VASP",
                        "precision": {"native_tier": "default", "basis_set": "plane waves"},
                        "sim_details": {"xc_functional_names": ["xc_default_1", "xc_default_2"]}
                    }
                },
                "material": {"topology": [
                    {"label": "original", "cell": {"a": 1.0, "b": 1.0, "c": 1.0, "alpha": 1.0, "beta": 1.0, "gamma": 1.0, "volume": 1.0, "atomic_density": 1.0, "mass_density": 1.0}, "description": "example"},
                    {"label": "conventional cell", "cell": {"a": 1.0, "b": 1.0, "c": 1.0, "alpha": 1.0, "beta": 1.0, "gamma": 1.0, "volume": 1.0, "atomic_density": 1.0, "mass_density": 1.0}, "description": "example conv", "symmetry": {"space_group_symbol": "P1", "space_group_number": 1}}
                ]}
            },
            "run": [{"calculation": [{"scf_iteration": []}]}],
            "metadata": {"entry_type": "VASP DFT SinglePoint", "entry_name": "example", "domain": "dft"}
        }

    # Inject SCF total energies into run -> calculation -> scf_iteration (if reference provided)
    scf_iterations = []
    if reference:
        for val in reference.get("scf_total_energies_ev", []):
            scf_iterations.append({"energy": {"total": {"value": val}}})
    full_data["run"][0]["calculation"][0]["scf_iteration"] = scf_iterations

    fake_proc = MagicMock()
    fake_proc.stdout = json.dumps(full_data)
    monkeypatch.setattr("subprocess.run", lambda *a, **k: fake_proc)

    out_dir = tmp_path / "out"
    out_dir.mkdir()

    # Run parser (will use mocked subprocess.run)
    run_parser(input_file, out_dir, force=True)

    produced_file = out_dir / f"fair_parsed_{input_file.stem}.json"
    assert produced_file.exists()

    produced = json.loads(produced_file.read_text(encoding='utf-8'))

    # Remove generated fair_parse_time if present from produced metadata
    if isinstance(produced.get('metadata'), dict) and 'fair_parse_time' in produced['metadata']:
        produced['metadata'].pop('fair_parse_time')

    if reference:
        # Also remove from reference if present (defensive)
        if isinstance(reference.get('metadata'), dict) and 'fair_parse_time' in reference['metadata']:
            reference['metadata'].pop('fair_parse_time')

        # Compare important fields rather than strict equality
        assert produced.get('domain') == reference.get('domain')
        # metadata should match for key items
        for k in ['method_name', 'workflow_name', 'program_version', 'program_name', 'basis_set_type']:
            assert produced.get('metadata', {}).get(k) == reference.get('metadata', {}).get(k)

        # SCF energies should match
        assert produced.get('scf_total_energies_ev') == reference.get('scf_total_energies_ev')

        # Material composition checks
        assert produced['material']['original']['composition']['chemical_formula_hill'] == reference['material']['original']['composition']['chemical_formula_hill']
        assert produced['material']['original']['composition']['elements'] == reference['material']['original']['composition']['elements']

        conv_prod = produced['material'].get('conventional cell', {})
        conv_ref = reference['material'].get('conventional cell', {})
        assert conv_prod.get('composition', {}).get('chemical_formula_hill') == conv_ref.get('composition', {}).get('chemical_formula_hill')
        assert conv_prod.get('composition', {}).get('elements') == conv_ref.get('composition', {}).get('elements')
        # Symmetry block should be present and match on key fields
        for sk in ['space_group_symbol', 'space_group_number']:
            assert conv_prod.get('symmetry', {}).get(sk) == conv_ref.get('symmetry', {}).get(sk)
    else:
        # Reference missing: at least ensure output contains expected keys
        assert 'metadata' in produced and isinstance(produced['metadata'], dict)
        for k in ['method_name', 'program_name']:
            assert produced['metadata'].get(k)
        assert produced.get('scf_total_energies_ev') is not None
        assert 'material' in produced and 'original' in produced['material']
