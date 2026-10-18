# CS::Statistics

CS::Statistics is a static, browser-based educational tool for exploring statistical analyses and creating charts. The project is a collection of HTML, JavaScript, Python, JSON, and image files; it has no server-side application or build pipeline in this checkout. The main page loads the interface and analysis code as static resources, while Pyodide runs the Python analyses in the browser. This is achieved using WebAssembly.

[WebAssembly](https://webassembly.org/) is a low-level, assembly-like binary instruction format that runs with near-native speed inside web browsers and other sandboxed environments. The primary purpose of WebAssembly (abbreviated as Wasm) is to enable high-performance, near-native speed code execution on the web. It is designed as a portable, compact binary instruction format that serves as a universal compilation target for high-level programming languages like C, C++, Rust, and Go, allowing them to run directly inside web browsers alongside JavaScript.

> **Intended use:** The in-app About page describes this as an educational aid, not a professional or critical-use statistics package. Check results with an appropriate statistical tool before relying on them.

## Features

The main interface (`index.html`) offers:

- **Data import:** Load the bundled example dataset or upload an `.xlsx` workbook.
- **Univariate analyses:** Linear regression, logistic regression, one-way ANOVA, and one-sample, independent two-sample, and paired-sample Student's *t*-tests.
- **Multivariate analyses:** K-means clustering, multidimensional scaling (MDS), multivariate analysis of variance (MANOVA), and principal components analysis (PCA).
- **Charts:** Bar, box, line, pie, radar, and scatter charts.
- **Results workspace:** View analyses in separate tabs, with up to ten result tabs available at a time. The data table is sortable and paginated (25 rows per page).
- **Tutorial and FAQ:** In-app guidance is available from the Tutorial and FAQ tabs.

Analysis dialogs let you choose columns for each procedure, usually by dragging column names into the requested variable areas. Analyses produce a chart and, where implemented, summary or test-statistic tables.

## Data and input expectations

The main page's **Load Example Data** action reads `example.json`, which contains 74 records with these columns: `feature`, `label`, `abnormal`, `tuberculosis`, `pneumonia`, `bronchitis`, and `weight`. `iris.json` is another bundled dataset (150 records; sepal and petal measurements, `species`, and `encoding`), but it is not connected to the main page's example-data action.

The upload control accepts `.xlsx` files. `execs/xlsx2json.py` reads the workbook through pandas/openpyxl and converts its records to JSON; spaces in column names are replaced with underscores. Choose variables with values appropriate to the requested role (for example, numeric columns for measurements and predictors, and categorical columns where a grouping or label is required). The dialogs display the role and count of columns expected for each analysis.

## How it works

1. `index.html` builds the interface, loads the selected modal from `modal/`, and places results in an available tab.
2. For statistical procedures, the result page in `export/` fetches the corresponding Python module from `execs/` and invokes it through Pyodide.
3. Python modules use scientific Python packages to calculate results and return JSON for the page.
4. Chart.js renders the plots; `assets/boxplot.js` registers box-plot and violin-plot chart types used by the chart integration.

The analysis and workbook conversion happen in the browser; this repository contains no application API or backend service. The browser still needs network access to retrieve the externally hosted runtime and library assets referenced by the HTML.

## Project layout

```text
.
├── index.html          Main app page and client-side application logic
├── default.html        Alternate app shell (see note below)
├── about.html          About modal content
├── help.html           Tutorial loaded by the main app
├── faq.html            FAQ loaded by the main app
├── example.json        Dataset used by “Load Example Data”
├── iris.json           Additional bundled dataset
├── assets/
│   ├── boxplot.js      Chart.js box-plot/violin-plot integration
│   ├── help.html       Additional tutorial copy
│   ├── modal/          Screenshots of analysis/chart dialogs
│   └── export/         Screenshots of example results
├── modal/              Variable-selection dialogs
├── export/             Analysis result and chart pages
└── execs/              Python analysis and XLSX conversion modules
```

The `modal/` and `export/` folders contain templates for the procedures and charts exposed by the main page. They also include a volcano-chart template that is not linked from `index.html`. `default.html` is an alternate shell with extra Ensemble menu links (decision tree, Naive Bayes, random forest, and SVM); the corresponding modal, result, and Python implementation files are not present in this checkout. Use `index.html` for the available, wired feature set.

## Runtime dependencies

There is no `package.json`, requirements file, or build configuration in the project. Dependencies are declared or loaded by the HTML at runtime:

- jQuery 3.7.1 and Semantic UI 2.5.0
- Pyodide 0.27.7
- Chart.js (loaded from jsDelivr without an explicit version in the page)
- Pyodide packages: scikit-learn, pandas, and micropip; `openpyxl` and `statsmodels` are installed through micropip
- Scientific modules import NumPy, SciPy, scikit-learn, pandas, and statsmodels as needed

For changes, keep the `index.html` menu entries, matching `modal/` and `export/` templates, and any required `execs/` modules in sync. Confirm that runtime package imports are available in the configured Pyodide environment.

## Guidance and limitations

- This project is presented as an educational demonstration, not validated statistical software for clinical, financial, safety-critical, or other consequential decisions.
- Statistical methods have assumptions and constraints; review the procedure and its assumptions for the data and question at hand.
- `index.html` loads libraries and Python packages at runtime from third-party CDNs. Offline use and fully reproducible dependency versions are not configured.
- The project has no checked-in automated test suite, dependency lockfile, or documented deployment workflow. It is organized as a static site and can be hosted by a static web server that serves the files and subdirectories.
