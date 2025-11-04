
# __Mg VASP DFT SinglePoint simulation__

<div class="grid cards" markdown>

{{ structure_viewer("fair-structure.json") }}

- ### Material Composition - original

    | Property                     | Value                       |
    |------------------------------|-----------------------------|
    | Chemical formula (IUPAC) | **Mg** |
    | Chemical formula (Reduced) | **Mg** |
    | Label | **original** |
    | Elements | **Mg** |
    | Number of elements | **1** |
    | Number of atoms | **1** |
    | Dimensionality | **3D** |

</div>

## __Structural information__

<div class="grid cards" markdown>

- ### Lattice (original)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **3.093** | Angstrom |
    | b | **3.093** | Angstrom |
    | c | **3.093** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **109** | Degrees |
    | Beta | **109** | Degrees |
    | Gamma | **109** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **22.772** | Å³ |
    | Mass density | **1.772e-27** | kg / Å³ |
    | Atomic density | **0.044** | Å⁻³ |

- ### Lattice (conventional cell)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **3.571** | Angstrom |
    | b | **3.571** | Angstrom |
    | c | **3.571** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **90** | Degrees |
    | Beta | **90** | Degrees |
    | Gamma | **90** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **45.545** | Å³ |
    | Mass density | **1.772e-27** | kg / Å³ |
    | Atomic density | **0.044** | Å⁻³ |

- ### Symmetry (conventional cell)

    | Property                       | Value            |
    |---------------------------------|------------------|
    | Crystal system | **cubic** |
    | Bravais lattice | **cI** |
    | Space group symbol | **Im-3m** |
    | Space group number | **229** |
    | Point group | **m-3m** |
    | Hall number | **529** |
    | Hall symbol | **-I 4 2 3** |
    | Prototype name | **bcc** |
    | Prototype label aflow | **A_cI2_229_a** |

- ### K points information

    | Property               | Value |
    |------------------------|--------|
    | Dimensionality | **3** |
    | Sampling method | **Monkhorst-Pack** |
    | Number of points | **32768** |
    | Grid | **[32, 32, 32]** |

</div>

## __Metadata__

<div class="grid cards" markdown>

- ### Calculation Metadata

    | Property                   | Value                                                      |
    |----------------------------|------------------------------------------------------------|
    | **Method name** | DFT |
    | **Workflow name** | SinglePoint |
    | **Program name** | VASP |
    | **Program version** | 4.6.35 3Apr08 complex parallel LinuxIFC |
    | **Basis set type** | plane waves |
    | **Core electron treatment** | pseudopotential |
    | **Jacob's ladder** | GGA |
    | **XC functional names** | GGA_C_PBE, GGA_X_PBE |
    | **Code-specific tier** | VASP - high |
    | **Basis set** | plane waves |
    | **Entry type** | VASP DFT SinglePoint |
    | **Entry name** | Mg VASP DFT SinglePoint simulation |
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
    const scfData = JSON.parse('[{"step": 1, "total_ev": 97.52414131, "free_ev": 97.52414131, "total_t0_ev": 97.52414131}, {"step": 2, "total_ev": 3.8989064399999998, "free_ev": 3.8989064399999998, "total_t0_ev": 3.8989064399999998}, {"step": 3, "total_ev": -1.42044566, "free_ev": -1.42044566, "total_t0_ev": -1.42044566}, {"step": 4, "total_ev": -1.45772087, "free_ev": -1.45772087, "total_t0_ev": -1.45772087}, {"step": 5, "total_ev": -1.45776307, "free_ev": -1.45776307, "total_t0_ev": -1.45776307}, {"step": 6, "total_ev": -1.45155287, "free_ev": -1.45155287, "total_t0_ev": -1.45155287}, {"step": 7, "total_ev": -1.45203253, "free_ev": -1.45203253, "total_t0_ev": -1.45203253}, {"step": 8, "total_ev": -1.45204832, "free_ev": -1.45204832, "total_t0_ev": -1.45204832}, {"step": 9, "total_ev": -1.4520482, "free_ev": -1.4520482, "total_t0_ev": -1.4520482}]');

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
    | **Total** | -1.452048 |
    | **Free** | -1.452048 |
    | **Total (T=0)** | 0.000000 |
    | **Band Gap** | 0.000000 |

- ### SCF Iteration Energies

    | Step | Total Energy (eV) | Free Energy (eV) | Total Energy (T=0) (eV) |
    |:---|---:|---:|---:|
| 1 | 97.52414 | 97.52414 | 97.52414 |
| 2 | 3.89891 | 3.89891 | 3.89891 |
| 3 | -1.42045 | -1.42045 | -1.42045 |
| 4 | -1.45772 | -1.45772 | -1.45772 |
| 5 | -1.45776 | -1.45776 | -1.45776 |
| 6 | -1.45155 | -1.45155 | -1.45155 |
| 7 | -1.45203 | -1.45203 | -1.45203 |
| 8 | -1.45205 | -1.45205 | -1.45205 |
| 9 | -1.45205 | -1.45205 | -1.45205 |

</div>


<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<div id="scf_chart_div" style="width: 100%; height: 500px; margin-bottom: 20px;"></div>
<script type="text/javascript">
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    // Parse the JSON data passed from Python
    const scfData = JSON.parse('[{"step": 1, "total_ev": 97.52414131, "free_ev": 97.52414131, "total_t0_ev": 97.52414131}, {"step": 2, "total_ev": 3.8989064399999998, "free_ev": 3.8989064399999998, "total_t0_ev": 3.8989064399999998}, {"step": 3, "total_ev": -1.42044566, "free_ev": -1.42044566, "total_t0_ev": -1.42044566}, {"step": 4, "total_ev": -1.45772087, "free_ev": -1.45772087, "total_t0_ev": -1.45772087}, {"step": 5, "total_ev": -1.45776307, "free_ev": -1.45776307, "total_t0_ev": -1.45776307}, {"step": 6, "total_ev": -1.45155287, "free_ev": -1.45155287, "total_t0_ev": -1.45155287}, {"step": 7, "total_ev": -1.45203253, "free_ev": -1.45203253, "total_t0_ev": -1.45203253}, {"step": 8, "total_ev": -1.45204832, "free_ev": -1.45204832, "total_t0_ev": -1.45204832}, {"step": 9, "total_ev": -1.4520482, "free_ev": -1.4520482, "total_t0_ev": -1.4520482}]');

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


