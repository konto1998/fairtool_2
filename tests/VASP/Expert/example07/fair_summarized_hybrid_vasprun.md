
# __C48H24O26Zn8 VASP DFT SinglePoint simulation__

<div class="grid cards" markdown>

{{ structure_viewer("fair-structure.json") }}

- ### Material Composition - original

    | Property                     | Value                       |
    |------------------------------|-----------------------------|
    | Chemical formula (IUPAC) | **Zn4C24H12O13** |
    | Chemical formula (Reduced) | **C24H12O13Zn4** |
    | Label | **original** |
    | Elements | **C, H, O, Zn** |
    | Number of elements | **4** |
    | Number of atoms | **106** |

</div>

## __Structural information__

<div class="grid cards" markdown>

- ### Lattice (original)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **18.420** | Angstrom |
    | b | **18.420** | Angstrom |
    | c | **18.420** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **60** | Degrees |
    | Beta | **60** | Degrees |
    | Gamma | **60** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **4419.429** | Å³ |
    | Mass density | **5.785e-28** | kg / Å³ |
    | Atomic density | **0.024** | Å⁻³ |





- ### K points information

    | Property               | Value |
    |------------------------|--------|
    | Dimensionality | **3** |
    | Sampling method | **Gamma-centered** |
    | Number of points | **1** |
    | Grid | **[1, 1, 1]** |

</div>

## __Metadata__

<div class="grid cards" markdown>

- ### Calculation Metadata

    | Property                   | Value                                                      |
    |----------------------------|------------------------------------------------------------|
    | **Method name** | DFT |
    | **Workflow name** | SinglePoint |
    | **Program name** | VASP |
    | **Program version** | 5.4.4.18Apr17-6-g9f103f2a35 gamma-only parallel LinuxIFC |
    | **Basis set type** | plane waves |
    | **Core electron treatment** | pseudopotential |
    | **Jacob's ladder** | hybrid |
    | **XC functional names** | HYB_GGA_XC_HSE06 |
    | **Code-specific tier** | VASP - accurate |
    | **Basis set** | plane waves |
    | **Entry type** | VASP DFT SinglePoint |
    | **Entry name** | C48H24O26Zn8 VASP DFT SinglePoint simulation |
    | **Mainfile** | hybrid_vasprun.xml |

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
    const scfData = JSON.parse('[{"step": 1, "total_ev": -854.37958601, "free_ev": -854.37958601, "total_t0_ev": -854.37958601}, {"step": 2, "total_ev": -855.5654164, "free_ev": -855.5654164, "total_t0_ev": -855.5654164}, {"step": 3, "total_ev": -856.24841118, "free_ev": -856.24841118, "total_t0_ev": -856.24841118}, {"step": 4, "total_ev": -856.37872616, "free_ev": -856.37872616, "total_t0_ev": -856.37872616}, {"step": 5, "total_ev": -856.42355726, "free_ev": -856.42355726, "total_t0_ev": -856.42355726}, {"step": 6, "total_ev": -856.44714446, "free_ev": -856.44714446, "total_t0_ev": -856.44714446}, {"step": 7, "total_ev": -856.4558353100001, "free_ev": -856.4558353100001, "total_t0_ev": -856.4558353100001}, {"step": 8, "total_ev": -856.4588498699999, "free_ev": -856.4588498699999, "total_t0_ev": -856.4588498699999}, {"step": 9, "total_ev": -856.45993835, "free_ev": -856.45993835, "total_t0_ev": -856.45993835}, {"step": 10, "total_ev": -856.46029732, "free_ev": -856.46029732, "total_t0_ev": -856.46029732}, {"step": 11, "total_ev": -856.46041887, "free_ev": -856.46041887, "total_t0_ev": -856.46041887}, {"step": 12, "total_ev": -856.46046674, "free_ev": -856.46046674, "total_t0_ev": -856.46046674}, {"step": 13, "total_ev": -856.4604861400001, "free_ev": -856.4604861400001, "total_t0_ev": -856.4604861400001}, {"step": 14, "total_ev": -856.46049594, "free_ev": -856.46049594, "total_t0_ev": -856.46049594}]');

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
    | **Total** | -860.865878 |
    | **Free** | -860.865878 |
    | **Total (T=0)** | -0.000000 |
    | **Band Gap** | 4.547900 |

- ### SCF Iteration Energies

    | Step | Total Energy (eV) | Free Energy (eV) | Total Energy (T=0) (eV) |
    |:---|---:|---:|---:|
| 1 | -854.37959 | -854.37959 | -854.37959 |
| 2 | -855.56542 | -855.56542 | -855.56542 |
| 3 | -856.24841 | -856.24841 | -856.24841 |
| 4 | -856.37873 | -856.37873 | -856.37873 |
| 5 | -856.42356 | -856.42356 | -856.42356 |
| 6 | -856.44714 | -856.44714 | -856.44714 |
| 7 | -856.45584 | -856.45584 | -856.45584 |
| 8 | -856.45885 | -856.45885 | -856.45885 |
| 9 | -856.45994 | -856.45994 | -856.45994 |
| 10 | -856.46030 | -856.46030 | -856.46030 |
| 11 | -856.46042 | -856.46042 | -856.46042 |
| 12 | -856.46047 | -856.46047 | -856.46047 |
| 13 | -856.46049 | -856.46049 | -856.46049 |
| 14 | -856.46050 | -856.46050 | -856.46050 |

</div>


<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<div id="scf_chart_div" style="width: 100%; height: 500px; margin-bottom: 20px;"></div>
<script type="text/javascript">
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    // Parse the JSON data passed from Python
    const scfData = JSON.parse('[{"step": 1, "total_ev": -854.37958601, "free_ev": -854.37958601, "total_t0_ev": -854.37958601}, {"step": 2, "total_ev": -855.5654164, "free_ev": -855.5654164, "total_t0_ev": -855.5654164}, {"step": 3, "total_ev": -856.24841118, "free_ev": -856.24841118, "total_t0_ev": -856.24841118}, {"step": 4, "total_ev": -856.37872616, "free_ev": -856.37872616, "total_t0_ev": -856.37872616}, {"step": 5, "total_ev": -856.42355726, "free_ev": -856.42355726, "total_t0_ev": -856.42355726}, {"step": 6, "total_ev": -856.44714446, "free_ev": -856.44714446, "total_t0_ev": -856.44714446}, {"step": 7, "total_ev": -856.4558353100001, "free_ev": -856.4558353100001, "total_t0_ev": -856.4558353100001}, {"step": 8, "total_ev": -856.4588498699999, "free_ev": -856.4588498699999, "total_t0_ev": -856.4588498699999}, {"step": 9, "total_ev": -856.45993835, "free_ev": -856.45993835, "total_t0_ev": -856.45993835}, {"step": 10, "total_ev": -856.46029732, "free_ev": -856.46029732, "total_t0_ev": -856.46029732}, {"step": 11, "total_ev": -856.46041887, "free_ev": -856.46041887, "total_t0_ev": -856.46041887}, {"step": 12, "total_ev": -856.46046674, "free_ev": -856.46046674, "total_t0_ev": -856.46046674}, {"step": 13, "total_ev": -856.4604861400001, "free_ev": -856.4604861400001, "total_t0_ev": -856.4604861400001}, {"step": 14, "total_ev": -856.46049594, "free_ev": -856.46049594, "total_t0_ev": -856.46049594}]');

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


