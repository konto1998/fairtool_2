
# __Cs2AgHgCl6 VASP DFT SinglePoint simulation__

<div class="grid cards" markdown>

{{ structure_viewer("fair-structure.json") }}

- ### Material Composition - original

    | Property                     | Value                       |
    |------------------------------|-----------------------------|
    | Chemical formula (IUPAC) | **Cs2AgHgCl6** |
    | Chemical formula (Reduced) | **AgCl6Cs2Hg** |
    | Label | **original** |
    | Elements | **Ag, Cl, Cs, Hg** |
    | Number of elements | **4** |
    | Number of atoms | **10** |
    | Dimensionality | **3D** |

</div>

## __Structural information__

<div class="grid cards" markdown>

- ### Lattice (original)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **7.311** | Angstrom |
    | b | **7.311** | Angstrom |
    | c | **7.311** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **60** | Degrees |
    | Beta | **60** | Degrees |
    | Gamma | **60** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **276.268** | Å³ |
    | Mass density | **4.730e-27** | kg / Å³ |
    | Atomic density | **0.036** | Å⁻³ |

- ### Lattice (conventional cell)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **10.339** | Angstrom |
    | b | **10.339** | Angstrom |
    | c | **10.339** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **90** | Degrees |
    | Beta | **90** | Degrees |
    | Gamma | **90** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **1105.074** | Å³ |
    | Mass density | **4.730e-27** | kg / Å³ |
    | Atomic density | **0.036** | Å⁻³ |

- ### Symmetry (conventional cell)

    | Property                       | Value            |
    |---------------------------------|------------------|
    | Crystal system | **cubic** |
    | Bravais lattice | **cF** |
    | Space group symbol | **Fm-3m** |
    | Space group number | **225** |
    | Point group | **m-3m** |
    | Hall number | **523** |
    | Hall symbol | **-F 4 2 3** |

- ### K points information

    | Property               | Value |
    |------------------------|--------|
    | Dimensionality | **3** |
    | Sampling method | **Gamma-centered** |
    | Number of points | **64** |
    | Grid | **[4, 4, 4]** |

</div>

## __Metadata__

<div class="grid cards" markdown>

- ### Calculation Metadata

    | Property                   | Value                                                      |
    |----------------------------|------------------------------------------------------------|
    | **Method name** | DFT |
    | **Workflow name** | SinglePoint |
    | **Program name** | VASP |
    | **Program version** | 6.3.0 20Jan22 complex parallel LinuxGNU |
    | **Basis set type** | plane waves |
    | **Core electron treatment** | pseudopotential |
    | **Jacob's ladder** | GGA |
    | **XC functional names** | GGA_C_PBE, GGA_X_PBE |
    | **Code-specific tier** | VASP - normal |
    | **Basis set** | plane waves |
    | **Entry type** | VASP DFT SinglePoint |
    | **Entry name** | Cs2AgHgCl6 VASP DFT SinglePoint simulation |
    | **Mainfile** | vasprun.xml |

</div>

## __Energies__

### SCF Convergence

<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<div id="scf_chart_div" style="width: 100%; height: 500px; margin-bottom: 20px;"></div>
<script type="text/javascript">
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    // Parse the JSON data passed from Python
    const scfData = JSON.parse('[{"step": 1, "total_ev": 699.14377904, "free_ev": 699.14377904, "total_t0_ev": 699.14377904}, {"step": 2, "total_ev": 39.53784668, "free_ev": 39.53784668, "total_t0_ev": 39.53784668}, {"step": 3, "total_ev": -29.39822135, "free_ev": -29.39822135, "total_t0_ev": -29.39822135}, {"step": 4, "total_ev": -31.84184981, "free_ev": -31.84185412, "total_t0_ev": -31.84185197}, {"step": 5, "total_ev": -31.95257211, "free_ev": -31.95257728, "total_t0_ev": -31.9525747}, {"step": 6, "total_ev": -23.01513748, "free_ev": -23.01514237, "total_t0_ev": -23.01513993}, {"step": 7, "total_ev": -28.92343522, "free_ev": -28.92343523, "total_t0_ev": -28.92343523}, {"step": 8, "total_ev": -28.75642267, "free_ev": -28.75642381, "total_t0_ev": -28.75642324}, {"step": 9, "total_ev": -29.84021826, "free_ev": -29.84021843, "total_t0_ev": -29.840218340000003}, {"step": 10, "total_ev": -29.927091299999997, "free_ev": -29.927094109999995, "total_t0_ev": -29.92709271}, {"step": 11, "total_ev": -29.897942950000004, "free_ev": -29.897945760000002, "total_t0_ev": -29.89794435}, {"step": 12, "total_ev": -29.95272426, "free_ev": -29.952727229999997, "total_t0_ev": -29.95272575}, {"step": 13, "total_ev": -29.958725700000002, "free_ev": -29.95872851, "total_t0_ev": -29.958727100000004}, {"step": 14, "total_ev": -29.95940956, "free_ev": -29.95941237, "total_t0_ev": -29.95941097}, {"step": 15, "total_ev": -29.95944214, "free_ev": -29.959444950000005, "total_t0_ev": -29.95944354}, {"step": 16, "total_ev": -29.959530640000004, "free_ev": -29.959533450000002, "total_t0_ev": -29.95953204}, {"step": 17, "total_ev": -29.95962655, "free_ev": -29.959629370000002, "total_t0_ev": -29.95962796}, {"step": 18, "total_ev": -29.959630790000002, "free_ev": -29.95963359, "total_t0_ev": -29.95963219}, {"step": 19, "total_ev": -29.95964678, "free_ev": -29.95964959, "total_t0_ev": -29.95964819}, {"step": 20, "total_ev": -29.95965715, "free_ev": -29.95965996, "total_t0_ev": -29.959658560000005}, {"step": 21, "total_ev": -29.95964039, "free_ev": -29.95964319, "total_t0_ev": -29.95964179}, {"step": 22, "total_ev": -29.959668219999998, "free_ev": -29.959671029999996, "total_t0_ev": -29.95966963}, {"step": 23, "total_ev": -29.95967692, "free_ev": -29.959679720000004, "total_t0_ev": -29.959678320000002}, {"step": 24, "total_ev": -29.95967697, "free_ev": -29.95968042, "total_t0_ev": -29.9596787}, {"step": 25, "total_ev": -29.95976083, "free_ev": -29.95976373, "total_t0_ev": -29.959762280000003}, {"step": 26, "total_ev": -29.959692070000003, "free_ev": -29.95969488, "total_t0_ev": -29.95969348}, {"step": 27, "total_ev": -29.959678420000003, "free_ev": -29.95968123, "total_t0_ev": -29.95967983}, {"step": 28, "total_ev": -29.9596972, "free_ev": -29.95970057, "total_t0_ev": -29.95969888}, {"step": 29, "total_ev": -29.959757799999995, "free_ev": -29.95976141, "total_t0_ev": -29.959759609999995}, {"step": 30, "total_ev": -29.95979699, "free_ev": -29.95979989, "total_t0_ev": -29.959798440000004}, {"step": 31, "total_ev": -29.95971031, "free_ev": -29.95971353, "total_t0_ev": -29.95971192}, {"step": 32, "total_ev": -29.95973759, "free_ev": -29.9597404, "total_t0_ev": -29.959739}, {"step": 33, "total_ev": -29.95966008, "free_ev": -29.95966288, "total_t0_ev": -29.95966148}, {"step": 34, "total_ev": -29.95967863, "free_ev": -29.95968225, "total_t0_ev": -29.95968044}, {"step": 35, "total_ev": -29.95980177, "free_ev": -29.95980528, "total_t0_ev": -29.95980352}, {"step": 36, "total_ev": -29.95978607, "free_ev": -29.9597897, "total_t0_ev": -29.95978789}, {"step": 37, "total_ev": -29.9598037, "free_ev": -29.95980735, "total_t0_ev": -29.959805529999997}, {"step": 38, "total_ev": -29.959805699999997, "free_ev": -29.95980864, "total_t0_ev": -29.959807169999998}, {"step": 39, "total_ev": -29.95971226, "free_ev": -29.9597159, "total_t0_ev": -29.95971408}, {"step": 40, "total_ev": -29.95980038, "free_ev": -29.959804009999996, "total_t0_ev": -29.95980219}, {"step": 41, "total_ev": -29.9598011, "free_ev": -29.95980474, "total_t0_ev": -29.95980292}]');

    var data = new google.visualization.DataTable();
    data.addColumn('number', 'Step');
    data.addColumn('number', 'Total Energy (eV)');
    data.addColumn('number', 'Free Energy (eV)');
    data.addColumn('number', 'Total Energy (T=0) (eV)');

    // Convert the list of objects into an array of arrays
    // Google Charts expects null for missing values, which JSON.parse handles
    const rows = scfData.map(item => [
      item.step, 
      item.total_ev, 
      item.free_ev, 
      item.total_t0_ev
    ]);

    data.addRows(rows);

    var options = {
      title: '',
      curveType: 'function',
      legend: { position: 'bottom' },
      hAxis: {
        title: 'SCF Step'
      },
      vAxis: {
        title: 'Energy (eV)'
      },
      // This allows the chart to be responsive
      chartArea: {'width': '85%', 'height': '75%'},
    };

    var chart = new google.visualization.LineChart(document.getElementById('scf_chart_div'));
    chart.draw(data, options);
  }
</script>


<div class="grid cards" markdown>

- ### Final Calculation Energies

    | Energy | Value (eV) |
    |---|---|
    | **Total** | -29.959801 |
    | **Free** | -29.959805 |
    | **Total (T=0)** | -29.959803 |
    | **Band Gap** | 7.225400 |

- ### SCF Iteration Energies

    | Step | Total Energy (eV) | Free Energy (eV) | Total Energy (T=0) (eV) |
    |:---|---:|---:|---:|
| 1 | 699.14378 | 699.14378 | 699.14378 |
| 2 | 39.53785 | 39.53785 | 39.53785 |
| 3 | -29.39822 | -29.39822 | -29.39822 |
| 4 | -31.84185 | -31.84185 | -31.84185 |
| 5 | -31.95257 | -31.95258 | -31.95257 |
| 6 | -23.01514 | -23.01514 | -23.01514 |
| 7 | -28.92344 | -28.92344 | -28.92344 |
| 8 | -28.75642 | -28.75642 | -28.75642 |
| 9 | -29.84022 | -29.84022 | -29.84022 |
| 10 | -29.92709 | -29.92709 | -29.92709 |
| 11 | -29.89794 | -29.89795 | -29.89794 |
| 12 | -29.95272 | -29.95273 | -29.95273 |
| 13 | -29.95873 | -29.95873 | -29.95873 |
| 14 | -29.95941 | -29.95941 | -29.95941 |
| 15 | -29.95944 | -29.95944 | -29.95944 |
| 16 | -29.95953 | -29.95953 | -29.95953 |
| 17 | -29.95963 | -29.95963 | -29.95963 |
| 18 | -29.95963 | -29.95963 | -29.95963 |
| 19 | -29.95965 | -29.95965 | -29.95965 |
| 20 | -29.95966 | -29.95966 | -29.95966 |
| 21 | -29.95964 | -29.95964 | -29.95964 |
| 22 | -29.95967 | -29.95967 | -29.95967 |
| 23 | -29.95968 | -29.95968 | -29.95968 |
| 24 | -29.95968 | -29.95968 | -29.95968 |
| 25 | -29.95976 | -29.95976 | -29.95976 |
| 26 | -29.95969 | -29.95969 | -29.95969 |
| 27 | -29.95968 | -29.95968 | -29.95968 |
| 28 | -29.95970 | -29.95970 | -29.95970 |
| 29 | -29.95976 | -29.95976 | -29.95976 |
| 30 | -29.95980 | -29.95980 | -29.95980 |
| 31 | -29.95971 | -29.95971 | -29.95971 |
| 32 | -29.95974 | -29.95974 | -29.95974 |
| 33 | -29.95966 | -29.95966 | -29.95966 |
| 34 | -29.95968 | -29.95968 | -29.95968 |
| 35 | -29.95980 | -29.95981 | -29.95980 |
| 36 | -29.95979 | -29.95979 | -29.95979 |
| 37 | -29.95980 | -29.95981 | -29.95981 |
| 38 | -29.95981 | -29.95981 | -29.95981 |
| 39 | -29.95971 | -29.95972 | -29.95971 |
| 40 | -29.95980 | -29.95980 | -29.95980 |
| 41 | -29.95980 | -29.95980 | -29.95980 |

</div>


<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<div id="scf_chart_div" style="width: 100%; height: 500px; margin-bottom: 20px;"></div>
<script type="text/javascript">
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    // Parse the JSON data passed from Python
    const scfData = JSON.parse('[{"step": 1, "total_ev": 699.14377904, "free_ev": 699.14377904, "total_t0_ev": 699.14377904}, {"step": 2, "total_ev": 39.53784668, "free_ev": 39.53784668, "total_t0_ev": 39.53784668}, {"step": 3, "total_ev": -29.39822135, "free_ev": -29.39822135, "total_t0_ev": -29.39822135}, {"step": 4, "total_ev": -31.84184981, "free_ev": -31.84185412, "total_t0_ev": -31.84185197}, {"step": 5, "total_ev": -31.95257211, "free_ev": -31.95257728, "total_t0_ev": -31.9525747}, {"step": 6, "total_ev": -23.01513748, "free_ev": -23.01514237, "total_t0_ev": -23.01513993}, {"step": 7, "total_ev": -28.92343522, "free_ev": -28.92343523, "total_t0_ev": -28.92343523}, {"step": 8, "total_ev": -28.75642267, "free_ev": -28.75642381, "total_t0_ev": -28.75642324}, {"step": 9, "total_ev": -29.84021826, "free_ev": -29.84021843, "total_t0_ev": -29.840218340000003}, {"step": 10, "total_ev": -29.927091299999997, "free_ev": -29.927094109999995, "total_t0_ev": -29.92709271}, {"step": 11, "total_ev": -29.897942950000004, "free_ev": -29.897945760000002, "total_t0_ev": -29.89794435}, {"step": 12, "total_ev": -29.95272426, "free_ev": -29.952727229999997, "total_t0_ev": -29.95272575}, {"step": 13, "total_ev": -29.958725700000002, "free_ev": -29.95872851, "total_t0_ev": -29.958727100000004}, {"step": 14, "total_ev": -29.95940956, "free_ev": -29.95941237, "total_t0_ev": -29.95941097}, {"step": 15, "total_ev": -29.95944214, "free_ev": -29.959444950000005, "total_t0_ev": -29.95944354}, {"step": 16, "total_ev": -29.959530640000004, "free_ev": -29.959533450000002, "total_t0_ev": -29.95953204}, {"step": 17, "total_ev": -29.95962655, "free_ev": -29.959629370000002, "total_t0_ev": -29.95962796}, {"step": 18, "total_ev": -29.959630790000002, "free_ev": -29.95963359, "total_t0_ev": -29.95963219}, {"step": 19, "total_ev": -29.95964678, "free_ev": -29.95964959, "total_t0_ev": -29.95964819}, {"step": 20, "total_ev": -29.95965715, "free_ev": -29.95965996, "total_t0_ev": -29.959658560000005}, {"step": 21, "total_ev": -29.95964039, "free_ev": -29.95964319, "total_t0_ev": -29.95964179}, {"step": 22, "total_ev": -29.959668219999998, "free_ev": -29.959671029999996, "total_t0_ev": -29.95966963}, {"step": 23, "total_ev": -29.95967692, "free_ev": -29.959679720000004, "total_t0_ev": -29.959678320000002}, {"step": 24, "total_ev": -29.95967697, "free_ev": -29.95968042, "total_t0_ev": -29.9596787}, {"step": 25, "total_ev": -29.95976083, "free_ev": -29.95976373, "total_t0_ev": -29.959762280000003}, {"step": 26, "total_ev": -29.959692070000003, "free_ev": -29.95969488, "total_t0_ev": -29.95969348}, {"step": 27, "total_ev": -29.959678420000003, "free_ev": -29.95968123, "total_t0_ev": -29.95967983}, {"step": 28, "total_ev": -29.9596972, "free_ev": -29.95970057, "total_t0_ev": -29.95969888}, {"step": 29, "total_ev": -29.959757799999995, "free_ev": -29.95976141, "total_t0_ev": -29.959759609999995}, {"step": 30, "total_ev": -29.95979699, "free_ev": -29.95979989, "total_t0_ev": -29.959798440000004}, {"step": 31, "total_ev": -29.95971031, "free_ev": -29.95971353, "total_t0_ev": -29.95971192}, {"step": 32, "total_ev": -29.95973759, "free_ev": -29.9597404, "total_t0_ev": -29.959739}, {"step": 33, "total_ev": -29.95966008, "free_ev": -29.95966288, "total_t0_ev": -29.95966148}, {"step": 34, "total_ev": -29.95967863, "free_ev": -29.95968225, "total_t0_ev": -29.95968044}, {"step": 35, "total_ev": -29.95980177, "free_ev": -29.95980528, "total_t0_ev": -29.95980352}, {"step": 36, "total_ev": -29.95978607, "free_ev": -29.9597897, "total_t0_ev": -29.95978789}, {"step": 37, "total_ev": -29.9598037, "free_ev": -29.95980735, "total_t0_ev": -29.959805529999997}, {"step": 38, "total_ev": -29.959805699999997, "free_ev": -29.95980864, "total_t0_ev": -29.959807169999998}, {"step": 39, "total_ev": -29.95971226, "free_ev": -29.9597159, "total_t0_ev": -29.95971408}, {"step": 40, "total_ev": -29.95980038, "free_ev": -29.959804009999996, "total_t0_ev": -29.95980219}, {"step": 41, "total_ev": -29.9598011, "free_ev": -29.95980474, "total_t0_ev": -29.95980292}]');

    var data = new google.visualization.DataTable();
    data.addColumn('number', 'Step');
    data.addColumn('number', 'Total Energy (eV)');
    data.addColumn('number', 'Free Energy (eV)');
    data.addColumn('number', 'Total Energy (T=0) (eV)');

    // Convert the list of objects into an array of arrays
    // Google Charts expects null for missing values, which JSON.parse handles
    const rows = scfData.map(item => [
      item.step, 
      item.total_ev, 
      item.free_ev, 
      item.total_t0_ev
    ]);

    data.addRows(rows);

    var options = {
      title: '',
      curveType: 'function',
      legend: { position: 'bottom' },
      hAxis: {
        title: 'SCF Step'
      },
      vAxis: {
        title: 'Energy (eV)'
      },
      // This allows the chart to be responsive
      chartArea: {'width': '85%', 'height': '75%'},
    };

    var chart = new google.visualization.LineChart(document.getElementById('scf_chart_div'));
    chart.draw(data, options);
  }
</script>


