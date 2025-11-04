
# __Si VASP DFT SinglePoint simulation__

<div class="grid cards" markdown>

{{ structure_viewer("fair-structure.json") }}

- ### Material Composition - original

    | Property                     | Value                       |
    |------------------------------|-----------------------------|
    | Chemical formula (IUPAC) | **Si** |
    | Chemical formula (Reduced) | **Si** |
    | Label | **original** |
    | Elements | **Si** |
    | Number of elements | **1** |
    | Number of atoms | **2** |
    | Dimensionality | **3D** |

</div>

## __Structural information__

<div class="grid cards" markdown>

- ### Lattice (original)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **3.867** | Angstrom |
    | b | **3.867** | Angstrom |
    | c | **3.867** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **60** | Degrees |
    | Beta | **60** | Degrees |
    | Gamma | **60** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **40.892** | Å³ |
    | Mass density | **2.281e-27** | kg / Å³ |
    | Atomic density | **0.049** | Å⁻³ |

- ### Lattice (conventional cell)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **5.469** | Angstrom |
    | b | **5.469** | Angstrom |
    | c | **5.469** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **90** | Degrees |
    | Beta | **90** | Degrees |
    | Gamma | **90** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **163.568** | Å³ |
    | Mass density | **2.281e-27** | kg / Å³ |
    | Atomic density | **0.049** | Å⁻³ |

- ### Symmetry (conventional cell)

    | Property                       | Value            |
    |---------------------------------|------------------|
    | Crystal system | **cubic** |
    | Bravais lattice | **cF** |
    | Space group symbol | **Fd-3m** |
    | Space group number | **227** |
    | Point group | **m-3m** |
    | Hall number | **525** |
    | Hall symbol | **F 4d 2 3 -1d** |
    | Prototype name | **diamond** |
    | Prototype label aflow | **A_cF8_227_a** |

- ### K points information

    | Property               | Value |
    |------------------------|--------|
    | Dimensionality | **3** |
    | Sampling method | **Line-path** |
    | Number of points | **20** |
    | Grid | **20** |

</div>

## __Metadata__

<div class="grid cards" markdown>

- ### Calculation Metadata

    | Property                   | Value                                                      |
    |----------------------------|------------------------------------------------------------|
    | **Method name** | DFT |
    | **Workflow name** | SinglePoint |
    | **Program name** | VASP |
    | **Program version** | 5.4.1 24Jun15 complex parallel IFC91_ompi |
    | **Basis set type** | plane waves |
    | **Core electron treatment** | pseudopotential |
    | **Jacob's ladder** | GGA |
    | **XC functional names** | GGA_C_PBE, GGA_X_PBE |
    | **Code-specific tier** | VASP - accurate |
    | **Basis set** | plane waves |
    | **Entry type** | VASP DFT SinglePoint |
    | **Entry name** | Si VASP DFT SinglePoint simulation |
    | **Mainfile** | band_si_vasprun.xml |

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
    const scfData = JSON.parse('[{"step": 1, "total_ev": -10.62401272, "free_ev": -10.64739058, "total_t0_ev": -10.63570165}, {"step": 2, "total_ev": -12.04650935, "free_ev": -12.0549797, "total_t0_ev": -12.050744519999999}, {"step": 3, "total_ev": -12.047378519999999, "free_ev": -12.05584021, "total_t0_ev": -12.05160936}, {"step": 4, "total_ev": -12.0473787, "free_ev": -12.05584039, "total_t0_ev": -12.051609549999998}, {"step": 5, "total_ev": -12.0473787, "free_ev": -12.05584039, "total_t0_ev": -12.051609549999998}, {"step": 6, "total_ev": -12.0473787, "free_ev": -12.05584039, "total_t0_ev": -12.051609549999998}]');

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
    | **Total** | -12.051610 |
    | **Free** | -12.055840 |
    | **Total (T=0)** | -0.008462 |
    | **Band Gap** | 0.000000 |

- ### SCF Iteration Energies

    | Step | Total Energy (eV) | Free Energy (eV) | Total Energy (T=0) (eV) |
    |:---|---:|---:|---:|
| 1 | -10.62401 | -10.64739 | -10.63570 |
| 2 | -12.04651 | -12.05498 | -12.05074 |
| 3 | -12.04738 | -12.05584 | -12.05161 |
| 4 | -12.04738 | -12.05584 | -12.05161 |
| 5 | -12.04738 | -12.05584 | -12.05161 |
| 6 | -12.04738 | -12.05584 | -12.05161 |

</div>


<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<div id="scf_chart_div" style="width: 100%; height: 500px; margin-bottom: 20px;"></div>
<script type="text/javascript">
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    // Parse the JSON data passed from Python
    const scfData = JSON.parse('[{"step": 1, "total_ev": -10.62401272, "free_ev": -10.64739058, "total_t0_ev": -10.63570165}, {"step": 2, "total_ev": -12.04650935, "free_ev": -12.0549797, "total_t0_ev": -12.050744519999999}, {"step": 3, "total_ev": -12.047378519999999, "free_ev": -12.05584021, "total_t0_ev": -12.05160936}, {"step": 4, "total_ev": -12.0473787, "free_ev": -12.05584039, "total_t0_ev": -12.051609549999998}, {"step": 5, "total_ev": -12.0473787, "free_ev": -12.05584039, "total_t0_ev": -12.051609549999998}, {"step": 6, "total_ev": -12.0473787, "free_ev": -12.05584039, "total_t0_ev": -12.051609549999998}]');

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


