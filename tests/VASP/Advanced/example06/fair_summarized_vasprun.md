
# __AcAg VASP GeometryOptimization simulation__

<div class="grid cards" markdown>

{{ structure_viewer("fair-structure.json") }}

- ### Material Composition - original

    | Property                     | Value                       |
    |------------------------------|-----------------------------|
    | Chemical formula (IUPAC) | **AcAg** |
    | Chemical formula (Reduced) | **AcAg** |
    | Label | **original** |
    | Elements | **Ac, Ag** |
    | Number of elements | **2** |
    | Number of atoms | **2** |
    | Dimensionality | **3D** |

</div>

## __Structural information__

<div class="grid cards" markdown>

- ### Lattice (original)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **4.610** | Angstrom |
    | b | **4.610** | Angstrom |
    | c | **4.610** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **60** | Degrees |
    | Beta | **60** | Degrees |
    | Gamma | **60** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **69.263** | Å³ |
    | Mass density | **8.028e-27** | kg / Å³ |
    | Atomic density | **0.029** | Å⁻³ |

- ### Lattice (conventional cell)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **6.519** | Angstrom |
    | b | **6.519** | Angstrom |
    | c | **6.519** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **90** | Degrees |
    | Beta | **90** | Degrees |
    | Gamma | **90** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **277.053** | Å³ |
    | Mass density | **8.028e-27** | kg / Å³ |
    | Atomic density | **0.029** | Å⁻³ |

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
    | Prototype name | **rock salt** |
    | Prototype label aflow | **AB_cF8_225_a_b** |

- ### K points information

    | Property               | Value |
    |------------------------|--------|
    | Dimensionality | **3** |
    | Sampling method | **Gamma-centered** |
    | Number of points | **4096** |
    | Grid | **[16, 16, 16]** |

</div>

## __Metadata__

<div class="grid cards" markdown>

- ### Calculation Metadata

    | Property                   | Value                                                      |
    |----------------------------|------------------------------------------------------------|
    | **Method name** | DFT |
    | **Workflow name** | GeometryOptimization |
    | **Program name** | VASP |
    | **Program version** | 5.3.2 13Sep12 complex serial LinuxIFC |
    | **Basis set type** | plane waves |
    | **Core electron treatment** | pseudopotential |
    | **Jacob's ladder** | GGA |
    | **XC functional names** | GGA_C_PBE, GGA_X_PBE |
    | **Code-specific tier** | VASP - accurate |
    | **Basis set** | plane waves |
    | **Entry type** | VASP GeometryOptimization |
    | **Entry name** | AcAg VASP GeometryOptimization simulation |
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
    const scfData = JSON.parse('[{"step": 1, "total_ev": 116.45879606000001, "free_ev": 116.45875643, "total_t0_ev": 116.45876963999999}, {"step": 2, "total_ev": 1.70506718, "free_ev": 1.70437998, "total_t0_ev": 1.70460905}, {"step": 3, "total_ev": -7.14910245, "free_ev": -7.15838638, "total_t0_ev": -7.15529174}, {"step": 4, "total_ev": -7.54341347, "free_ev": -7.5526309, "total_t0_ev": -7.54955842}, {"step": 5, "total_ev": -7.54680735, "free_ev": -7.55602137, "total_t0_ev": -7.552950029999999}, {"step": 6, "total_ev": -7.174492580000001, "free_ev": -7.18432144, "total_t0_ev": -7.18104515}, {"step": 7, "total_ev": -7.13505768, "free_ev": -7.144869639999999, "total_t0_ev": -7.14159899}, {"step": 8, "total_ev": -7.129721, "free_ev": -7.139541510000001, "total_t0_ev": -7.13626801}, {"step": 9, "total_ev": -7.12740713, "free_ev": -7.13725155, "total_t0_ev": -7.133970080000001}, {"step": 10, "total_ev": -7.12765117, "free_ev": -7.13747424, "total_t0_ev": -7.134199879999999}, {"step": 11, "total_ev": -7.12750385, "free_ev": -7.13733102, "total_t0_ev": -7.1340553}, {"step": 12, "total_ev": -7.127518769999999, "free_ev": -7.137336329999999, "total_t0_ev": -7.134063809999999}]');

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
    | **Total** | -7.134064 |
    | **Free** | -7.137336 |
    | **Total (T=0)** | -0.009818 |

- ### SCF Iteration Energies

    | Step | Total Energy (eV) | Free Energy (eV) | Total Energy (T=0) (eV) |
    |:---|---:|---:|---:|
| 1 | 116.45880 | 116.45876 | 116.45877 |
| 2 | 1.70507 | 1.70438 | 1.70461 |
| 3 | -7.14910 | -7.15839 | -7.15529 |
| 4 | -7.54341 | -7.55263 | -7.54956 |
| 5 | -7.54681 | -7.55602 | -7.55295 |
| 6 | -7.17449 | -7.18432 | -7.18105 |
| 7 | -7.13506 | -7.14487 | -7.14160 |
| 8 | -7.12972 | -7.13954 | -7.13627 |
| 9 | -7.12741 | -7.13725 | -7.13397 |
| 10 | -7.12765 | -7.13747 | -7.13420 |
| 11 | -7.12750 | -7.13733 | -7.13406 |
| 12 | -7.12752 | -7.13734 | -7.13406 |

</div>


<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<div id="scf_chart_div" style="width: 100%; height: 500px; margin-bottom: 20px;"></div>
<script type="text/javascript">
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    // Parse the JSON data passed from Python
    const scfData = JSON.parse('[{"step": 1, "total_ev": 116.45879606000001, "free_ev": 116.45875643, "total_t0_ev": 116.45876963999999}, {"step": 2, "total_ev": 1.70506718, "free_ev": 1.70437998, "total_t0_ev": 1.70460905}, {"step": 3, "total_ev": -7.14910245, "free_ev": -7.15838638, "total_t0_ev": -7.15529174}, {"step": 4, "total_ev": -7.54341347, "free_ev": -7.5526309, "total_t0_ev": -7.54955842}, {"step": 5, "total_ev": -7.54680735, "free_ev": -7.55602137, "total_t0_ev": -7.552950029999999}, {"step": 6, "total_ev": -7.174492580000001, "free_ev": -7.18432144, "total_t0_ev": -7.18104515}, {"step": 7, "total_ev": -7.13505768, "free_ev": -7.144869639999999, "total_t0_ev": -7.14159899}, {"step": 8, "total_ev": -7.129721, "free_ev": -7.139541510000001, "total_t0_ev": -7.13626801}, {"step": 9, "total_ev": -7.12740713, "free_ev": -7.13725155, "total_t0_ev": -7.133970080000001}, {"step": 10, "total_ev": -7.12765117, "free_ev": -7.13747424, "total_t0_ev": -7.134199879999999}, {"step": 11, "total_ev": -7.12750385, "free_ev": -7.13733102, "total_t0_ev": -7.1340553}, {"step": 12, "total_ev": -7.127518769999999, "free_ev": -7.137336329999999, "total_t0_ev": -7.134063809999999}]');

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


### Density of States (DOS)


