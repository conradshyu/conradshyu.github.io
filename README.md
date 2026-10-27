# CS::Statistics

CS::Statistics is a static, browser-based educational application for exploring statistical analyses and creating charts. The interface is built with HTML and JavaScript; Python analysis code runs locally in the browser through Pyodide (Python compiled to WebAssembly). There is no application server or project backend required for the main application.

> **Educational use only:** The application is an aid for learning and exploration, not for professional, clinical, financial, or other critical decisions. Statistical results depend on the input data, method, and assumptions. Independently validate any result that matters.

## Features

Open `index.html` to use the main application. It provides:

| Area | Available procedures |
| --- | --- |
| Univariate analysis | Linear regression, logistic regression, one-way ANOVA, and Student's t-tests (one-sample, independent two-sample, and paired-sample) |
| Multivariate analysis | K-means clustering, multidimensional scaling (MDS), multivariate analysis of variance (MANOVA), and principal component analysis (PCA) |
| Predictive/classification methods | Decision tree, Naive Bayes, random forest, and support vector machine (SVM) |
| Charts | Bar, box, line, pie, radar, and scatter plots |
| Data import | Bundled example data or an Excel `.xlsx` workbook |

Load data first, then choose a procedure from the menu. The procedure dialog describes the columns to select and their roles. Results and charts are displayed in tabs alongside the data table. The table shows 25 records per page.

## Run locally

Serve the project directory over HTTP so that the browser can load local HTML fragments, JSON data, and Python modules:

```sh
cd /path/to/github.io
python3 -m http.server 8000
```

Open <http://localhost:8000/> in a modern browser. An internet connection is needed to download the external JavaScript libraries, Pyodide runtime, and Python packages used by the app. Opening `index.html` directly with a `file://` URL may prevent the browser from loading local resources correctly.

`default.html` is an older alternate page, not the recommended entry point. Its spreadsheet upload handler posts to `upload.php`, which is not present in this project. The main `index.html` page instead reads the selected workbook in the browser and converts it with Pyodide.

## Data

`example.json` is the data loaded by **Import Data → Load Example Data**. It contains 74 records with these fields:

- `feature`
- `label`
- `abnormal`
- `tuberculosis`
- `pneumonia`
- `bronchitis`
- `weight`

The import control accepts `.xlsx` files. `execs/xlsx2json.py` reads the workbook using pandas and openpyxl, converts rows to JSON records, and replaces spaces in column names with underscores. It uses pandas' default worksheet selection (the first worksheet). The workbook is read in the browser; `index.html` does not post it to a project server.

Choose columns that match the selected method's requirements. For example, regression and dimensionality-reduction procedures generally need numeric values, while classification and group-comparison procedures may also require categorical labels or grouping variables. The dialogs provide role guidance; this project is not a general-purpose data-cleaning tool.

## How it works

1. `index.html` initializes the interface, data table, and Pyodide runtime. It loads the Tutorial (`help.html`), FAQ (`faq.html`), and analysis-selection dialogs (`modal/`) as needed.
2. Selecting an action loads its result page from `export/`. The page uses the selected data and columns and, for statistical analyses, calls the relevant Python module from `execs/` through Pyodide.
3. Chart.js renders visualizations. `assets/boxplot.js` adds box-plot and violin-plot chart types for the chart integration.
4. Workbook conversion also runs in Pyodide. `execs/xlsx2json.py` reads the workbook with pandas/openpyxl and returns JSON for the main page.

The main page loads Pyodide 0.27.7 and requests `scikit-learn`, `pandas`, and `micropip`; it uses `micropip` to install `openpyxl` and `statsmodels`. The analysis scripts also use NumPy and SciPy. The interface uses jQuery 3.7.1 and Semantic UI 2.5.0; charts use Chart.js loaded from jsDelivr. The tutorial pages load MathJax from a CDN. These runtime dependencies are external and are not vendored or locked to exact versions in this project.

## Project layout

```text
.
├── index.html                 Main application and browser-side orchestration
├── default.html               Older alternate page; references missing upload.php
├── about.html                 About dialog content
├── help.html                  In-app tutorial
├── faq.html                   In-app FAQ
├── example.json               Example dataset (74 records)
├── favicon.ico                Site icon
├── LICENSE                    Apache License 2.0
├── modal/                     Variable-selection dialogs loaded by index.html
│   ├── anova.html
│   ├── bar_chart.html
│   ├── bayes.html
│   ├── box_chart.html
│   ├── cluster.html
│   ├── forest.html
│   ├── line_chart.html
│   ├── linear.html
│   ├── logistic.html
│   ├── manova.html
│   ├── mds.html
│   ├── pca.html
│   ├── pie_chart.html
│   ├── radar_chart.html
│   ├── scatter_chart.html
│   ├── student0.html           One-sample t-test dialog
│   ├── student1.html           Two-sample t-test dialog
│   ├── student2.html           Paired-sample t-test dialog
│   ├── svm.html
│   ├── tree.html
│   └── volcano.html            Template not linked from the main menu
├── export/                    Result and chart pages loaded by the app
│   ├── anova.html
│   ├── bar_chart.html
│   ├── bayes.html
│   ├── box_chart.html
│   ├── cluster.html
│   ├── forest.html
│   ├── line_chart.html
│   ├── linear.html
│   ├── logistic.html
│   ├── manova.html
│   ├── mds.html
│   ├── pca.html
│   ├── pie_chart.html
│   ├── radar_chart.html
│   ├── scatter_chart.html
│   ├── student0.html           One-sample t-test result
│   ├── student1.html           Two-sample t-test result
│   ├── student2.html           Paired-sample t-test result
│   ├── svm.html
│   ├── tree.html
│   └── volcano.html            Template not linked from the main menu
├── execs/                     Python modules used by result pages
│   ├── anova.py
│   ├── bayes.py
│   ├── cluster.py
│   ├── forest.py
│   ├── linear.py
│   ├── logistic.py
│   ├── manova.py
│   ├── mds.py
│   ├── pca.py
│   ├── student.py              Shared implementation for the three t-tests
│   ├── svm.py
│   ├── tree.py
│   └── xlsx2json.py             XLSX-to-JSON conversion
└── assets/
    ├── boxplot.js               Chart.js box/violin chart integration
    ├── help.html                Additional copy of tutorial content
    ├── export/*.png             Tutorial result screenshots
    └── modal/*.png              Tutorial dialog screenshots
```

The `assets/` scripts and images are supplementary examples and tutorial material; the interactive application uses the Python modules in `execs/`. Its standalone Python examples are `decision_tree.py`, `driver.py`, `mds_metrics.py`, `naive_bayes.py`, `random_forest.py`, `svm_linear.py`, and `svm_nonlinear.py`. The root-level PNGs in `assets/` are `mds_metrics.png`, `naive_bayes.png`, and `svm_linear.png`; `assets/export/` and `assets/modal/` contain tutorial screenshots corresponding to result pages and selection dialogs. `assets/help.html` is a copy of the root tutorial `help.html`.

The analysis and chart features are wired across the menu in `index.html`, a dialog in `modal/`, a result page in `export/`, and (for statistical methods) a Python module in `execs/`. The three t-test pages share `execs/student.py`.

## Development notes and limitations

- This is a static site: there is no package manifest, Python requirements file, build configuration, automated test suite, or checked-in deployment workflow in the project.
- Runtime libraries and Python packages are downloaded from external CDNs/package sources. Offline use and fully reproducible dependency versions are not configured.
- The main page's workbook conversion is client-side, but the older `default.html` flow expects an absent `upload.php`.
- Statistical procedures have method-specific input requirements and assumptions. Review those requirements and validate outputs with an appropriate tool before relying on them.

## License

The project includes the Apache License, Version 2.0 in `LICENSE`.
