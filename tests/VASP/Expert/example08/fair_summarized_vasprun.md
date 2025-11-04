
# __C428H42N8O8 VASP DFT SinglePoint simulation__

<div class="grid cards" markdown>

{{ structure_viewer("fair-structure.json") }}

- ### Material Composition - original

    | Property                     | Value                       |
    |------------------------------|-----------------------------|
    | Chemical formula (IUPAC) | **C214N4H21O4** |
    | Chemical formula (Reduced) | **C214H21N4O4** |
    | Label | **original** |
    | Elements | **C, H, N, O** |
    | Number of elements | **4** |
    | Number of atoms | **486** |

</div>

## __Structural information__

<div class="grid cards" markdown>

- ### Lattice (original)

    | Lattice constant | Value     | Units |
    |------------------|-----------|-------|
    | a | **29.774** | Angstrom |
    | b | **30.067** | Angstrom |
    | c | **29.542** | Angstrom |

    | Lattice angles    | Value     | Units |
    |------------------|-----------|-------|
    | Alpha | **90** | Degrees |
    | Beta | **90** | Degrees |
    | Gamma | **90** | Degrees |

    | Cell quantities   | Value     | Units |
    |------------------|-----------|-------|
    | Volume | **26445.060** | Å³ |
    | Mass density | **3.405e-28** | kg / Å³ |
    | Atomic density | **0.018** | Å⁻³ |





- ### K points information

    | Property               | Value |
    |------------------------|--------|
    | Dimensionality | **3** |
    | Sampling method | **Gamma-centered** |
    | Number of points | **9** |
    | Grid | **[3, 3, 1]** |

</div>

## __Metadata__

<div class="grid cards" markdown>

- ### Calculation Metadata

    | Property                   | Value                                                      |
    |----------------------------|------------------------------------------------------------|
    | **Method name** | DFT |
    | **Workflow name** | SinglePoint |
    | **Program name** | VASP |
    | **Program version** | 5.4.4.18Apr17-6-g9f103f2a35 complex parallel LinuxIFC |
    | **Basis set type** | plane waves |
    | **Core electron treatment** | pseudopotential |
    | **Jacob's ladder** | GGA |
    | **XC functional names** | GGA_C_PBE, GGA_X_PBE |
    | **Code-specific tier** | VASP - accurate |
    | **Basis set** | plane waves |
    | **Entry type** | VASP DFT SinglePoint |
    | **Entry name** | C428H42N8O8 VASP DFT SinglePoint simulation |
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
    const scfData = JSON.parse('[{"step": 1, "total_ev": 23536.445688, "free_ev": 23536.445688, "total_t0_ev": 23536.445688}, {"step": 2, "total_ev": 9360.34183158, "free_ev": 9360.34183158, "total_t0_ev": 9360.34183158}, {"step": 3, "total_ev": 4237.00816844, "free_ev": 4237.00816844, "total_t0_ev": 4237.00816844}, {"step": 4, "total_ev": -1402.05743773, "free_ev": -1402.05743773, "total_t0_ev": -1402.05743773}, {"step": 5, "total_ev": -3678.32075784, "free_ev": -3678.32075784, "total_t0_ev": -3678.32075784}, {"step": 6, "total_ev": -4276.13044916, "free_ev": -4276.13044916, "total_t0_ev": -4276.13044916}, {"step": 7, "total_ev": -4420.33254886, "free_ev": -4420.33254886, "total_t0_ev": -4420.33254886}, {"step": 8, "total_ev": -4465.25998318, "free_ev": -4465.25998318, "total_t0_ev": -4465.25998318}, {"step": 9, "total_ev": -4484.4407469, "free_ev": -4484.4407469, "total_t0_ev": -4484.4407469}, {"step": 10, "total_ev": -4487.27402134, "free_ev": -4487.27402134, "total_t0_ev": -4487.27402134}, {"step": 11, "total_ev": -4487.38885891, "free_ev": -4487.38885891, "total_t0_ev": -4487.38885891}, {"step": 12, "total_ev": -4487.40663269, "free_ev": -4487.40663269, "total_t0_ev": -4487.40663269}, {"step": 13, "total_ev": -4281.25336229, "free_ev": -4281.25336229, "total_t0_ev": -4281.25336229}, {"step": 14, "total_ev": -4211.80625336, "free_ev": -4211.80625336, "total_t0_ev": -4211.80625336}, {"step": 15, "total_ev": -4209.7724227, "free_ev": -4209.7724227, "total_t0_ev": -4209.7724227}, {"step": 16, "total_ev": -4209.14419515, "free_ev": -4209.14419515, "total_t0_ev": -4209.14419515}, {"step": 17, "total_ev": -4208.8051858, "free_ev": -4208.8051858, "total_t0_ev": -4208.8051858}, {"step": 18, "total_ev": -4208.72094278, "free_ev": -4208.72094278, "total_t0_ev": -4208.72094278}, {"step": 19, "total_ev": -4208.74086017, "free_ev": -4208.74086017, "total_t0_ev": -4208.74086017}, {"step": 20, "total_ev": -4208.77789868, "free_ev": -4208.77789868, "total_t0_ev": -4208.77789868}, {"step": 21, "total_ev": -4208.81131797, "free_ev": -4208.81131797, "total_t0_ev": -4208.81131797}, {"step": 22, "total_ev": -4208.85549137, "free_ev": -4208.85549137, "total_t0_ev": -4208.85549137}, {"step": 23, "total_ev": -4208.89082249, "free_ev": -4208.89082249, "total_t0_ev": -4208.89082249}, {"step": 24, "total_ev": -4208.9111405, "free_ev": -4208.9111405, "total_t0_ev": -4208.9111405}, {"step": 25, "total_ev": -4208.91708139, "free_ev": -4208.91708139, "total_t0_ev": -4208.91708139}, {"step": 26, "total_ev": -4208.92309493, "free_ev": -4208.92309493, "total_t0_ev": -4208.92309493}, {"step": 27, "total_ev": -4208.92698804, "free_ev": -4208.92698804, "total_t0_ev": -4208.92698804}, {"step": 28, "total_ev": -4208.92845233, "free_ev": -4208.92845233, "total_t0_ev": -4208.92845233}, {"step": 29, "total_ev": -4208.92989582, "free_ev": -4208.92989582, "total_t0_ev": -4208.92989582}, {"step": 30, "total_ev": -4208.93054947, "free_ev": -4208.93054947, "total_t0_ev": -4208.93054947}, {"step": 31, "total_ev": -4208.93071745, "free_ev": -4208.93071745, "total_t0_ev": -4208.93071745}, {"step": 32, "total_ev": -4208.93127719, "free_ev": -4208.93127719, "total_t0_ev": -4208.93127719}, {"step": 33, "total_ev": -4208.93141213, "free_ev": -4208.93141213, "total_t0_ev": -4208.93141213}, {"step": 34, "total_ev": -4208.93161842, "free_ev": -4208.93161842, "total_t0_ev": -4208.93161842}, {"step": 35, "total_ev": -4208.9315897, "free_ev": -4208.9315897, "total_t0_ev": -4208.9315897}, {"step": 36, "total_ev": -4208.93180914, "free_ev": -4208.93180914, "total_t0_ev": -4208.93180914}, {"step": 37, "total_ev": -4208.93184731, "free_ev": -4208.93184731, "total_t0_ev": -4208.93184731}, {"step": 38, "total_ev": -4208.93183431, "free_ev": -4208.93183431, "total_t0_ev": -4208.93183431}, {"step": 39, "total_ev": -4208.93186265, "free_ev": -4208.93186265, "total_t0_ev": -4208.93186265}, {"step": 40, "total_ev": -4208.93184377, "free_ev": -4208.93184377, "total_t0_ev": -4208.93184377}, {"step": 41, "total_ev": -4208.93187937, "free_ev": -4208.93187937, "total_t0_ev": -4208.93187937}, {"step": 42, "total_ev": -4208.93188922, "free_ev": -4208.93188922, "total_t0_ev": -4208.93188922}]');

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
    | **Total** | -4252.290045 |
    | **Free** | -4252.290045 |
    | **Total (T=0)** | 0.000000 |
    | **Band Gap** | 0.000000 |

- ### SCF Iteration Energies

    | Step | Total Energy (eV) | Free Energy (eV) | Total Energy (T=0) (eV) |
    |:---|---:|---:|---:|
| 1 | 23536.44569 | 23536.44569 | 23536.44569 |
| 2 | 9360.34183 | 9360.34183 | 9360.34183 |
| 3 | 4237.00817 | 4237.00817 | 4237.00817 |
| 4 | -1402.05744 | -1402.05744 | -1402.05744 |
| 5 | -3678.32076 | -3678.32076 | -3678.32076 |
| 6 | -4276.13045 | -4276.13045 | -4276.13045 |
| 7 | -4420.33255 | -4420.33255 | -4420.33255 |
| 8 | -4465.25998 | -4465.25998 | -4465.25998 |
| 9 | -4484.44075 | -4484.44075 | -4484.44075 |
| 10 | -4487.27402 | -4487.27402 | -4487.27402 |
| 11 | -4487.38886 | -4487.38886 | -4487.38886 |
| 12 | -4487.40663 | -4487.40663 | -4487.40663 |
| 13 | -4281.25336 | -4281.25336 | -4281.25336 |
| 14 | -4211.80625 | -4211.80625 | -4211.80625 |
| 15 | -4209.77242 | -4209.77242 | -4209.77242 |
| 16 | -4209.14420 | -4209.14420 | -4209.14420 |
| 17 | -4208.80519 | -4208.80519 | -4208.80519 |
| 18 | -4208.72094 | -4208.72094 | -4208.72094 |
| 19 | -4208.74086 | -4208.74086 | -4208.74086 |
| 20 | -4208.77790 | -4208.77790 | -4208.77790 |
| 21 | -4208.81132 | -4208.81132 | -4208.81132 |
| 22 | -4208.85549 | -4208.85549 | -4208.85549 |
| 23 | -4208.89082 | -4208.89082 | -4208.89082 |
| 24 | -4208.91114 | -4208.91114 | -4208.91114 |
| 25 | -4208.91708 | -4208.91708 | -4208.91708 |
| 26 | -4208.92309 | -4208.92309 | -4208.92309 |
| 27 | -4208.92699 | -4208.92699 | -4208.92699 |
| 28 | -4208.92845 | -4208.92845 | -4208.92845 |
| 29 | -4208.92990 | -4208.92990 | -4208.92990 |
| 30 | -4208.93055 | -4208.93055 | -4208.93055 |
| 31 | -4208.93072 | -4208.93072 | -4208.93072 |
| 32 | -4208.93128 | -4208.93128 | -4208.93128 |
| 33 | -4208.93141 | -4208.93141 | -4208.93141 |
| 34 | -4208.93162 | -4208.93162 | -4208.93162 |
| 35 | -4208.93159 | -4208.93159 | -4208.93159 |
| 36 | -4208.93181 | -4208.93181 | -4208.93181 |
| 37 | -4208.93185 | -4208.93185 | -4208.93185 |
| 38 | -4208.93183 | -4208.93183 | -4208.93183 |
| 39 | -4208.93186 | -4208.93186 | -4208.93186 |
| 40 | -4208.93184 | -4208.93184 | -4208.93184 |
| 41 | -4208.93188 | -4208.93188 | -4208.93188 |
| 42 | -4208.93189 | -4208.93189 | -4208.93189 |

</div>


<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<div id="scf_chart_div" style="width: 100%; height: 500px; margin-bottom: 20px;"></div>
<script type="text/javascript">
  google.charts.load('current', {'packages':['corechart']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    // Parse the JSON data passed from Python
    const scfData = JSON.parse('[{"step": 1, "total_ev": 23536.445688, "free_ev": 23536.445688, "total_t0_ev": 23536.445688}, {"step": 2, "total_ev": 9360.34183158, "free_ev": 9360.34183158, "total_t0_ev": 9360.34183158}, {"step": 3, "total_ev": 4237.00816844, "free_ev": 4237.00816844, "total_t0_ev": 4237.00816844}, {"step": 4, "total_ev": -1402.05743773, "free_ev": -1402.05743773, "total_t0_ev": -1402.05743773}, {"step": 5, "total_ev": -3678.32075784, "free_ev": -3678.32075784, "total_t0_ev": -3678.32075784}, {"step": 6, "total_ev": -4276.13044916, "free_ev": -4276.13044916, "total_t0_ev": -4276.13044916}, {"step": 7, "total_ev": -4420.33254886, "free_ev": -4420.33254886, "total_t0_ev": -4420.33254886}, {"step": 8, "total_ev": -4465.25998318, "free_ev": -4465.25998318, "total_t0_ev": -4465.25998318}, {"step": 9, "total_ev": -4484.4407469, "free_ev": -4484.4407469, "total_t0_ev": -4484.4407469}, {"step": 10, "total_ev": -4487.27402134, "free_ev": -4487.27402134, "total_t0_ev": -4487.27402134}, {"step": 11, "total_ev": -4487.38885891, "free_ev": -4487.38885891, "total_t0_ev": -4487.38885891}, {"step": 12, "total_ev": -4487.40663269, "free_ev": -4487.40663269, "total_t0_ev": -4487.40663269}, {"step": 13, "total_ev": -4281.25336229, "free_ev": -4281.25336229, "total_t0_ev": -4281.25336229}, {"step": 14, "total_ev": -4211.80625336, "free_ev": -4211.80625336, "total_t0_ev": -4211.80625336}, {"step": 15, "total_ev": -4209.7724227, "free_ev": -4209.7724227, "total_t0_ev": -4209.7724227}, {"step": 16, "total_ev": -4209.14419515, "free_ev": -4209.14419515, "total_t0_ev": -4209.14419515}, {"step": 17, "total_ev": -4208.8051858, "free_ev": -4208.8051858, "total_t0_ev": -4208.8051858}, {"step": 18, "total_ev": -4208.72094278, "free_ev": -4208.72094278, "total_t0_ev": -4208.72094278}, {"step": 19, "total_ev": -4208.74086017, "free_ev": -4208.74086017, "total_t0_ev": -4208.74086017}, {"step": 20, "total_ev": -4208.77789868, "free_ev": -4208.77789868, "total_t0_ev": -4208.77789868}, {"step": 21, "total_ev": -4208.81131797, "free_ev": -4208.81131797, "total_t0_ev": -4208.81131797}, {"step": 22, "total_ev": -4208.85549137, "free_ev": -4208.85549137, "total_t0_ev": -4208.85549137}, {"step": 23, "total_ev": -4208.89082249, "free_ev": -4208.89082249, "total_t0_ev": -4208.89082249}, {"step": 24, "total_ev": -4208.9111405, "free_ev": -4208.9111405, "total_t0_ev": -4208.9111405}, {"step": 25, "total_ev": -4208.91708139, "free_ev": -4208.91708139, "total_t0_ev": -4208.91708139}, {"step": 26, "total_ev": -4208.92309493, "free_ev": -4208.92309493, "total_t0_ev": -4208.92309493}, {"step": 27, "total_ev": -4208.92698804, "free_ev": -4208.92698804, "total_t0_ev": -4208.92698804}, {"step": 28, "total_ev": -4208.92845233, "free_ev": -4208.92845233, "total_t0_ev": -4208.92845233}, {"step": 29, "total_ev": -4208.92989582, "free_ev": -4208.92989582, "total_t0_ev": -4208.92989582}, {"step": 30, "total_ev": -4208.93054947, "free_ev": -4208.93054947, "total_t0_ev": -4208.93054947}, {"step": 31, "total_ev": -4208.93071745, "free_ev": -4208.93071745, "total_t0_ev": -4208.93071745}, {"step": 32, "total_ev": -4208.93127719, "free_ev": -4208.93127719, "total_t0_ev": -4208.93127719}, {"step": 33, "total_ev": -4208.93141213, "free_ev": -4208.93141213, "total_t0_ev": -4208.93141213}, {"step": 34, "total_ev": -4208.93161842, "free_ev": -4208.93161842, "total_t0_ev": -4208.93161842}, {"step": 35, "total_ev": -4208.9315897, "free_ev": -4208.9315897, "total_t0_ev": -4208.9315897}, {"step": 36, "total_ev": -4208.93180914, "free_ev": -4208.93180914, "total_t0_ev": -4208.93180914}, {"step": 37, "total_ev": -4208.93184731, "free_ev": -4208.93184731, "total_t0_ev": -4208.93184731}, {"step": 38, "total_ev": -4208.93183431, "free_ev": -4208.93183431, "total_t0_ev": -4208.93183431}, {"step": 39, "total_ev": -4208.93186265, "free_ev": -4208.93186265, "total_t0_ev": -4208.93186265}, {"step": 40, "total_ev": -4208.93184377, "free_ev": -4208.93184377, "total_t0_ev": -4208.93184377}, {"step": 41, "total_ev": -4208.93187937, "free_ev": -4208.93187937, "total_t0_ev": -4208.93187937}, {"step": 42, "total_ev": -4208.93188922, "free_ev": -4208.93188922, "total_t0_ev": -4208.93188922}]');

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


