
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
    | a | **3.918** | Angstrom |
    | b | **3.918** | Angstrom |
    | c | **3.918** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **60** | Degrees |
    | Beta | **60** | Degrees |
    | Gamma | **60** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **42.528** | Å³ |
    | Mass density | **2.193e-27** | kg / Å³ |
    | Atomic density | **0.047** | Å⁻³ |

- ### Lattice (conventional cell)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **5.541** | Angstrom |
    | b | **5.541** | Angstrom |
    | c | **5.541** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **90** | Degrees |
    | Beta | **90** | Degrees |
    | Gamma | **90** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **170.111** | Å³ |
    | Mass density | **2.193e-27** | kg / Å³ |
    | Atomic density | **0.047** | Å⁻³ |

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
    | Sampling method | **Monkhorst-Pack** |
    | Number of points | **3375** |
    | Grid | **[15, 15, 15]** |

</div>

## __Metadata__

<div class="grid cards" markdown>

- ### Calculation Metadata

    | Property                   | Value                                                      |
    |----------------------------|------------------------------------------------------------|
    | **Method name** | DFT |
    | **Workflow name** | SinglePoint |
    | **Program name** | VASP |
    | **Program version** | 5.2.2 15Apr09 complex serial LinuxIFC |
    | **Basis set type** | plane waves |
    | **Core electron treatment** | pseudopotential |
    | **Jacob's ladder** | GGA |
    | **XC functional names** | GGA_C_PBE, GGA_X_PBE |
    | **Code-specific tier** | VASP - accurate |
    | **Basis set** | plane waves |
    | **Entry type** | VASP DFT SinglePoint |
    | **Entry name** | Si VASP DFT SinglePoint simulation |
    | **Mainfile** | dos_si_vasprun.xml |

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
    const scfData = JSON.parse('[{"step": 1, "total_ev": 3.76925286, "free_ev": 3.76925286, "total_t0_ev": 3.76925286}, {"step": 2, "total_ev": -10.77482824, "free_ev": -10.77482824, "total_t0_ev": -10.77482824}, {"step": 3, "total_ev": -10.97884908, "free_ev": -10.97884908, "total_t0_ev": -10.97884908}, {"step": 4, "total_ev": -10.979694469999998, "free_ev": -10.979694469999998, "total_t0_ev": -10.979694469999998}, {"step": 5, "total_ev": -10.97969569, "free_ev": -10.97969569, "total_t0_ev": -10.97969569}, {"step": 6, "total_ev": -10.87928799, "free_ev": -10.87928799, "total_t0_ev": -10.87928799}, {"step": 7, "total_ev": -10.831247480000002, "free_ev": -10.831247480000002, "total_t0_ev": -10.831247480000002}, {"step": 8, "total_ev": -10.8325844, "free_ev": -10.8325844, "total_t0_ev": -10.8325844}, {"step": 9, "total_ev": -10.8326945, "free_ev": -10.8326945, "total_t0_ev": -10.8326945}, {"step": 10, "total_ev": -10.8327159, "free_ev": -10.8327159, "total_t0_ev": -10.8327159}]');

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
    | **Total** | -10.832716 |
    | **Free** | -10.832716 |
    | **Total (T=0)** | 0.000000 |
    | **Band Gap** | 0.665200 |

- ### SCF Iteration Energies

    | Step | Total Energy (eV) | Free Energy (eV) | Total Energy (T=0) (eV) |
    |:---|---:|---:|---:|
| 1 | 3.76925 | 3.76925 | 3.76925 |
| 2 | -10.77483 | -10.77483 | -10.77483 |
| 3 | -10.97885 | -10.97885 | -10.97885 |
| 4 | -10.97969 | -10.97969 | -10.97969 |
| 5 | -10.97970 | -10.97970 | -10.97970 |
| 6 | -10.87929 | -10.87929 | -10.87929 |
| 7 | -10.83125 | -10.83125 | -10.83125 |
| 8 | -10.83258 | -10.83258 | -10.83258 |
| 9 | -10.83269 | -10.83269 | -10.83269 |
| 10 | -10.83272 | -10.83272 | -10.83272 |

</div>


<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<div id="scf_chart_div" style="width: 100%; height: 500px; margin-bottom: 20px;"></div>
<script type="text/javascript">
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    // Parse the JSON data passed from Python
    const scfData = JSON.parse('[{"step": 1, "total_ev": 3.76925286, "free_ev": 3.76925286, "total_t0_ev": 3.76925286}, {"step": 2, "total_ev": -10.77482824, "free_ev": -10.77482824, "total_t0_ev": -10.77482824}, {"step": 3, "total_ev": -10.97884908, "free_ev": -10.97884908, "total_t0_ev": -10.97884908}, {"step": 4, "total_ev": -10.979694469999998, "free_ev": -10.979694469999998, "total_t0_ev": -10.979694469999998}, {"step": 5, "total_ev": -10.97969569, "free_ev": -10.97969569, "total_t0_ev": -10.97969569}, {"step": 6, "total_ev": -10.87928799, "free_ev": -10.87928799, "total_t0_ev": -10.87928799}, {"step": 7, "total_ev": -10.831247480000002, "free_ev": -10.831247480000002, "total_t0_ev": -10.831247480000002}, {"step": 8, "total_ev": -10.8325844, "free_ev": -10.8325844, "total_t0_ev": -10.8325844}, {"step": 9, "total_ev": -10.8326945, "free_ev": -10.8326945, "total_t0_ev": -10.8326945}, {"step": 10, "total_ev": -10.8327159, "free_ev": -10.8327159, "total_t0_ev": -10.8327159}]');

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


