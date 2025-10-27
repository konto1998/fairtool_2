import json
import copy
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from fairtool.parse import run_parser

REFERENCE_JSON_DATA = {
  "run": [
    {
      "program": {
        "name": "VASP",
        "version": "6.3.0 20Jan22 (build Feb 17 2022 08:07:03) complex parallel LinuxGNU",
        "compilation_datetime": 1713025724.0
      },
      "method": [
        {
          "dft": {
            "xc_functional": {
              "name": "GGA_C_PBE+GGA_X_PBE",
              "exchange": [
                {
                  "name": "GGA_X_PBE"
                }
              ],
              "correlation": [
                {
                  "name": "GGA_C_PBE"
                }
              ]
            }
          },
          "k_mesh": {
            "dimensionality": 3,
            "sampling_method": "Gamma-centered",
            "n_points": 64,
            "grid": [
              4,
              4,
              4
            ]
            # ... (k_mesh.points and k_mesh.weights truncated for brevity)
          },
          "electronic": {
            "method": "DFT"
          },
          "scf": {
            "threshold_energy_change": 1.602176634e-25
          },
          "atom_parameters": [
            {
              "atom_number": 80,
              "label": "Hg"
            },
            {
              "atom_number": 47,
              "label": "Ag"
            },
            {
              "atom_number": 55,
              "label": "Cs"
            },
            {
              "atom_number": 17,
              "label": "Cl"
            }
          ],
          "electrons_representation": [
            {
              "native_tier": "VASP - normal",
              "type": "plane waves",
              "scope": [
                "wavefunction"
              ],
              "basis_set": [
                {
                  "type": "plane waves",
                  "scope": [
                    "valence"
                  ],
                  "cutoff": 5.607618219e-17
                },
                {
                  "type": "plane waves",
                  "scope": [
                    "augmentation"
                  ],
                  "cutoff": 8.472310040591999e-17
                }
              ]
            }
          ]
        }
      ],
      "system": [
        {
          "type": "bulk",
          "configuration_raw_gid": "scfzvMx_YwTtsZx9zYSDrt20HTjB",
          "is_representative": True,
          "chemical_composition": "HgAgCsCsClClClClClCl",
          "chemical_composition_hill": "AgCl6Cs2Hg",
          "chemical_composition_reduced": "AgCl6Cs2Hg",
          "atoms": {
            "species": [
              80,
              47,
              55,
              55,
              17,
              17,
              17,
              17,
              17,
              17
            ],
            "labels": [
              "Hg",
              "Ag",
              "Cs",
              "Cs",
              "Cl",
              "Cl",
              "Cl",
              "Cl",
              "Cl",
              "Cl"
            ],
            "positions": [
              [
                0.0,
                0.0,
                0.0
              ],
              [
                5.1693238e-10,
                5.1693238e-10,
                5.1693238e-10
              ],
              [
                2.5846619e-10,
                2.5846619e-10,
                2.5846619e-10
              ],
              [
                7.7539857e-10,
                7.7539857e-10,
                7.7539857e-10
              ],
              [
                2.618106804667144e-10,
                5.1693238e-10,
                5.1693238e-10
              ],
              [
                7.720540795332856e-10,
                5.1693238e-10,
                5.1693238e-10
              ],
              [
                5.1693238e-10,
                2.618106804667144e-10,
                5.1693238e-10
              ],
              [
                5.1693238e-10,
                7.720540795332856e-10,
                5.1693238e-10
              ],
              [
                5.1693238e-10,
                5.1693238e-10,
                2.618106804667144e-10
              ],
              [
                5.1693238e-10,
                5.1693238e-10,
                7.720540795332856e-10
              ]
            ],
            "lattice_vectors": [
              [
                0.0,
                5.1693238e-10,
                5.1693238e-10
              ],
              [
                5.1693238e-10,
                0.0,
                5.1693238e-10
              ],
              [
                5.1693238e-10,
                5.1693238e-10,
                0.0
              ]
            ],
            "periodic": [
              True,
              True,
              True
            ]
            # ... (atoms.lattice_vectors_reciprocal truncated)
          },
          "symmetry": [
            {
              "bravais_lattice": "cF",
              "crystal_system": "cubic",
              "hall_number": 523,
              "hall_symbol": "-F 4 2 3",
              "international_short_symbol": "Fm-3m",
              "point_group": "m-3m",
              "space_group_number": 225
              # ... (symmetry.system_* truncated)
            }
          ]
        }
      ],
      "calculation": [
        {
          "system_ref": "#/run/0/system/0",
          "method_ref": "#/run/0/method/0",
          "energy": {
            "fermi": 2.731706979288985e-19,
            "highest_occupied": 2.73171116097e-19,
            "lowest_unoccupied": 2.8924094773601997e-19,
            "total": {
              "value": -4.800089328170749e-18
            },
            "free": {
              "value": -4.800089911363044e-18
            },
            "total_t0": {
              "value": -4.800089619766897e-18
            }
          },
          "forces": {
            "total": {
              "value": [
                [
                  -6.1844018072399995e-15,
                  1.4259372042599997e-15,
                  -8.76390618798e-15
                ]
                # ... (forces truncated)
              ]
            }
          },
          "stress": {
            "total": {
              "value": [
                [
                  2497744542.0,
                  -752187.0,
                  -721797.0
                ],
                [
                  -752196.0,
                  2565666923.0,
                  -775176.0
                ],
                [
                  -721861.0,
                  -775175.0,
                  2492460338.0
                ]
              ]
            }
          },
          "band_gap": [
            {
              "index": 0,
              "value": 1.1576367051303598e-18
              # ... (band_gap truncated)
            }
          ],
          "scf_iteration": [
            {
              "energy": {
                "total": {
                  "value": 1.120151826584347e-16
                }
                # ... (scf_iteration[0] truncated)
              }
            }
            # ... (scf_iteration list truncated, full list is in the reference file)
          ]
        }
      ]
    }
  ],
  "metadata": {
    "entry_name": "Cs2AgHgCl6 VASP DFT SinglePoint simulation",
    "entry_type": "VASP DFT SinglePoint",
    "mainfile": "/home/shinde/sandbox/fairtool/tests/VASP/example01/vasprun.xml",
    "domain": "dft",
    "optimade": {
      "elements": [
        "Ag",
        "Cl",
        "Cs",
        "Hg"
      ],
      "nelements": 4,
      "chemical_formula_reduced": "AgCl6Cs2Hg"
      # ... (metadata.optimade truncated)
    }
  },
  "results": {
    "material": {
      "material_id": "ImNwsjRVt1oPkznR4Fb3xrtS7IgJ",
      "structural_type": "bulk",
      "dimensionality": "3D",
      "elements": [
        "Ag",
        "Cl",
        "Cs",
        "Hg"
      ],
      "chemical_formula_descriptive": "Cs2AgHgCl6",
      "chemical_formula_reduced": "AgCl6Cs2Hg",
      "chemical_formula_hill": "AgCl6Cs2Hg",
      "symmetry": {
        "bravais_lattice": "cF",
        "crystal_system": "cubic",
        "hall_number": 523,
        "hall_symbol": "-F 4 2 3",
        "point_group": "m-3m",
        "space_group_number": 225,
        "space_group_symbol": "Fm-3m"
      },
      "topology": [
        {
          "system_id": "results/material/topology/0",
          "label": "original",
          "n_atoms": 10
          # ... (topology[0] truncated)
        },
        {
          "system_id": "results/material/topology/1",
          "label": "subsystem",
          "n_atoms": 10
          # ... (topology[1] truncated)
        },
        {
          "system_id": "results/material/topology/2",
          "label": "conventional cell",
          "n_atoms": 40,
          "symmetry": {
             "bravais_lattice": "cF",
             "crystal_system": "cubic",
             "space_group_number": 225,
             "space_group_symbol": "Fm-3m"
             # ... (topology[2].symmetry truncated)
          }
          # ... (topology[2] truncated)
        }
      ]
    },
    "method": {
      "method_name": "DFT",
      "workflow_name": "SinglePoint",
      "simulation": {
        "program_name": "VASP",
        "program_version": "6.3.0 20Jan22 (build Feb 17 2022 08:07:03) complex parallel LinuxGNU",
        "dft": {
          "basis_set_type": "plane waves",
          "core_electron_treatment": "pseudopotential",
          "scf_threshold_energy_change": 1.602176634e-25,
          "jacobs_ladder": "GGA",
          "xc_functional_type": "GGA",
          "xc_functional_names": [
            "GGA_C_PBE",
            "GGA_X_PBE"
          ]
        },
        "precision": {
          "native_tier": "VASP - normal",
          "basis_set": "plane waves",
          "planewave_cutoff": 5.607618219e-17
        }
      }
    },
    "properties": {
      "n_calculations": 1,
      "electronic": {
        "band_gap": [
          {
            "index": 0,
            "value": 1.1576367051303598e-18
            # ... (band_gap truncated)
          },
          {
            "index": 1,
            "value": 1.0942065321903e-18
            # ... (band_gap truncated)
          }
        ],
        "dos_electronic": [
          {
            "spin_polarized": True,
            "energy_fermi": 2.731706979288985e-19
            # ... (dos_electronic truncated)
          }
        ]
      }
    }
  }
}


@pytest.fixture
def reference_json_file(tmp_path):
    """
    Creates the 'reference.json' file in the tmp_path directory
    and returns its Path object.
    """
    # We create the reference file in tmp_path to make the test hermetic.
    ref_file = tmp_path / "reference.json"
    
    # We use the full JSON data, but to keep this file readable,
    # we'll use the constant defined above.
    ref_file.write_text(json.dumps(REFERENCE_JSON_DATA), encoding='utf-8')
    return ref_file


def test_parse_vasprun_example_matches_reference(tmp_path, monkeypatch, reference_json_file):
    """
    Mock the `nomad parse` subprocess to return the provided reference JSON
    (now treated as the raw nomad output) and compare the final parsed file
    to this same reference, checking only for the addition of
    metadata.fair_parse_time.
    """
    # 1. Create a dummy input file
    input_file = tmp_path / "vasprun.xml"
    input_file.write_text("<scf>dummy vasprun content</scf>")

    # 2. Load the reference data
    # This is used as the *base* for the mock nomad output
    reference_data = json.loads(reference_json_file.read_text(encoding='utf-8'))
    
    # Create a deep copy to use as the mock output.
    # This mock represents the *final merged* object after the `while` loop in `run_parser`.
    mock_output_data = copy.deepcopy(reference_data)

    # 3. Mock the subprocess.run call to return the merged data structure
    #    that `run_parser` expects *before* it starts deleting keys.
    
    # Add top-level keys that `run_parser` expects to delete:
    mock_output_data['n_quantities'] = 99
    mock_output_data['quantities'] = ['dummy_q']
    mock_output_data['sections'] = ['dummy_s']
    mock_output_data['section_defs'] = ['dummy_sd']
    mock_output_data['workflow2'] = {'name': 'dummy_workflow'}
    # These keys are *also* present in the metadata, so we copy them
    # to the top level to simulate the *first* JSON object from nomad.
    mock_output_data['entry_name'] = reference_data['metadata']['entry_name']
    mock_output_data['entry_type'] = reference_data['metadata']['entry_type']
    mock_output_data['mainfile'] = reference_data['metadata']['mainfile']
    mock_output_data['domain'] = reference_data['metadata']['domain']
    mock_output_data['optimade'] = reference_data['metadata']['optimade']
    
    # Add keys to the *archive* metadata block that `run_parser`
    # expects to delete (to prevent KeyError):
    if 'metadata' not in mock_output_data:
        mock_output_data['metadata'] = {}
    mock_output_data['metadata']['n_quantities'] = 99
    mock_output_data['metadata']['quantities'] = ['dummy_q']
    mock_output_data['metadata']['sections'] = ['dummy_s']
    mock_output_data['metadata']['section_defs'] = ['dummy_sd']


    fake_proc = MagicMock()
    fake_proc.stdout = json.dumps(mock_output_data)
    monkeypatch.setattr("subprocess.run", lambda *a, **k: fake_proc)

    out_dir = tmp_path / "out"
    out_dir.mkdir()

    # 4. Run the parser
    # This will delete the extra keys we added to `mock_output_data`
    # and add `fair_parse_time`.
    run_parser(input_file, out_dir, force=True)

    # 5. Load the file produced by the parser
    produced_file = out_dir / f"fair_parsed_{input_file.stem}.json"
    assert produced_file.exists()
    produced_data = json.loads(produced_file.read_text(encoding='utf-8'))

    # 6. Check that fair_parse_time was added
    assert "metadata" in produced_data
    assert "fair_parse_time" in produced_data["metadata"]
    assert isinstance(produced_data["metadata"]["fair_parse_time"], float)

    # 7. Remove the generated fair_parse_time for comparison
    produced_data["metadata"].pop("fair_parse_time")

    # 8. Perform detailed field comparison
    # The `produced_data` should now match the *original* `reference_data`
    # since all the extra keys were removed by `run_parser`.
    
    # --- Check Metadata ---
    # The parser keeps the metadata block from the archive, but
    # `parse.py` *also* deletes keys from it.
    # We must compare against the *original* reference data *after*
    # simulating the same deletions.
    
    expected_metadata = copy.deepcopy(reference_data["metadata"])
    expected_metadata.pop("n_quantities", None)
    expected_metadata.pop("quantities", None)
    expected_metadata.pop("sections", None)
    expected_metadata.pop("section_defs", None)

    assert produced_data["metadata"] == expected_metadata
    
    # --- Check Run section ---
    assert produced_data["run"][0]["program"]["name"] == reference_data["run"][0]["program"]["name"]
    assert produced_data["run"][0]["program"]["version"] == reference_data["run"][0]["program"]["version"]
    
    # --- Check Method section ---
    assert produced_data["run"][0]["method"][0]["dft"]["xc_functional"]["name"] == reference_data["run"][0]["method"][0]["dft"]["xc_functional"]["name"]
    assert produced_data["run"][0]["method"][0]["electronic"]["method"] == "DFT"
    
    # --- Check System section ---
    assert produced_data["run"][0]["system"][0]["chemical_composition_hill"] == reference_data["run"][0]["system"][0]["chemical_composition_hill"]
    assert produced_data["run"][0]["system"][0]["atoms"]["periodic"] == [True, True, True]
    assert produced_data["run"][0]["system"][0]["symmetry"][0]["crystal_system"] == reference_data["run"][0]["system"][0]["symmetry"][0]["crystal_system"]
    
    # --- Check Calculation section ---
    assert produced_data["run"][0]["calculation"][0]["energy"]["total"]["value"] == reference_data["run"][0]["calculation"][0]["energy"]["total"]["value"]
    assert produced_data["run"][0]["calculation"][0]["energy"]["fermi"] == reference_data["run"][0]["calculation"][0]["energy"]["fermi"]
    # Check that scf_iteration list is present and has the correct number of items
    assert "scf_iteration" in produced_data["run"][0]["calculation"][0]
    assert len(produced_data["run"][0]["calculation"][0]["scf_iteration"]) == len(reference_data["run"][0]["calculation"][0]["scf_iteration"])
    
    # --- Check Results section ---
    assert produced_data["results"]["material"]["chemical_formula_descriptive"] == reference_data["results"]["material"]["chemical_formula_descriptive"]
    assert produced_data["results"]["material"]["symmetry"]["space_group_symbol"] == reference_data["results"]["material"]["symmetry"]["space_group_symbol"]
    assert produced_data["results"]["material"]["topology"][0]["label"] == "original"
    assert produced_data["results"]["material"]["topology"][2]["label"] == "conventional cell"
    
    assert produced_data["results"]["method"]["method_name"] == reference_data["results"]["method"]["method_name"]
    assert produced_data["results"]["method"]["simulation"]["program_name"] == reference_data["results"]["method"]["simulation"]["program_name"]
    assert produced_data["results"]["method"]["simulation"]["dft"]["jacobs_ladder"] == reference_data["results"]["method"]["simulation"]["dft"]["jacobs_ladder"]
    
    assert produced_data["results"]["properties"]["electronic"]["band_gap"][0]["value"] == reference_data["results"]["properties"]["electronic"]["band_gap"][0]["value"]
    assert produced_data["results"]["properties"]["electronic"]["dos_electronic"][0]["spin_polarized"] == reference_data["results"]["properties"]["electronic"]["dos_electronic"][0]["spin_polarized"]
    
    # --- Final check: Compare the modified produced_data with the original reference_data ---
    # This ensures no *other* fields were accidentally dropped or modified
    
    expected_final_data = copy.deepcopy(reference_data)
    # Re-apply the metadata pops to the expected data for a final full comparison
    expected_final_data["metadata"].pop("n_quantities", None)
    expected_final_data["metadata"].pop("quantities", None)
    expected_final_data["metadata"].pop("sections", None)
    expected_final_data["metadata"].pop("section_defs", None)

    assert produced_data == expected_final_data

