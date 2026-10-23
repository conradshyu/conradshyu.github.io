# CS::Statistics

CS::Statistics is a static, browser-based educational application for exploring statistical analyses and creating charts. It combines an HTML and JavaScript interface with Python calculations executed in the browser through Pyodide (Python compiled to WebAssembly). The application does not require an application server or send analyses to a project backend.

> **Educational use only:** The in-app About page says this tool is not intended for professional or critical applications. Statistical output depends on the method, input data, and assumptions; verify results with an appropriate, validated tool before relying on them.

## Features

Open `index.html` to use the main application. Its menus provide:

- **Univariate analyses:** linear regression, logistic regression, one-way ANOVA, and one-sample, independent two-sample, and paired-sample Student's *t*-tests.
- **Multivariate analyses:** K-means clustering, multidimensional scaling (MDS), multivariate analysis of variance (MANOVA), and principal component analysis (PCA).
- **Ensemble and predictive methods:** decision tree, Naive Bayes, random forest, and support vector machine (SVM).
- **Charts:** bar, box, line, pie, radar, and scatter plots.
- **Data import:** load the bundled example data or upload an Excel `.xlsx` workbook.

Choose a procedure after loading data, then assign columns to the roles described in its dialog. Most dialogs use drag and drop. Analysis results appear in separate tabs with charts and, where implemented, statistical summaries. Up to ten result tabs can be open. The data table supports sorting and displays 25 rows per page. Chart result pages include controls for titles, axes, legends, and other presentation options.

The Tutorial and FAQ tabs are available in the application. The tutorial uses the bundled example data to illustrate variable selection and reading results.

## Run locally

Serve the project directory over HTTP so the page can load its HTML fragments, data, and Python modules:

```sh
cd /path/to/github.io
python3 -m http.server 8000
```

Then open <http://localhost:8000/> in a modern browser. The application loads JavaScript libraries, Pyodide, and Python packages from external CDNs at runtime, so an internet connection is required on first use and for any resources not cached by the browser. Opening the HTML directly as a `file://` URL may prevent the browser from loading the required local resources.

`default.html` is an older alternate page, not the recommended entry point. Its spreadsheet upload flow posts to `upload.php`, which is not included in this repository. Use `index.html`, whose workbook conversion runs in the browser.

## Data

- `example.json` is the dataset used by **Import Data → Load Example Data**. It contains 74 records with the columns `feature`, `label`, `abnormal`, `tuberculosis`, `pneumonia`, `bronchitis`, and `weight`.
- `iris.json` contains 150 Iris records with `sepal_length`, `sepal_width`, `petal_length`, `petal_width`, `species`, and `encoding`. It is included as additional sample data but is not connected to the main page's example-data action.
- The upload control accepts `.xlsx` files. `execs/xlsx2json.py` reads the workbook with pandas and openpyxl and converts the worksheet records to JSON. It replaces spaces in column names with underscores. The reader uses pandas' default worksheet selection (the first worksheet).

Select variables that fit the role requested by each analysis or chart. For example, measurements and predictors generally need numeric values, while some procedures use a categorical grouping or label. The dialogs describe their expected variables; the application does not provide a general-purpose data-cleaning workflow.

## How the application works

1. `index.html` initializes the interface and data table, loads `modal/` dialogs and the Tutorial/FAQ fragments, and creates result tabs.
2. An analysis result page in `export/` fetches its matching Python module from `execs/`, passes the selected columns and dataset to Pyodide, then renders the returned results.
3. Chart.js renders the plots. `assets/boxplot.js` adds box-plot and violin-plot chart types used by the chart integration.
4. The workbook conversion is also performed in Pyodide; no workbook is uploaded to a project server by `index.html`.

The main page loads Pyodide 0.27.7 and requests the `scikit-learn`, `pandas`, and `micropip` packages. It uses `micropip` to install `openpyxl` and `statsmodels`; the Python modules also import NumPy and SciPy. jQuery 3.7.1 and Semantic UI 2.5.0 provide interface behavior, while Chart.js is loaded from jsDelivr without a version specified in the page. These external runtime dependencies are not vendored or locked in this repository.

## Project structure

```text
.
├── index.html                 Main application entry point and client-side logic
├── default.html               Older alternate page; references a missing upload.php
├── about.html                 About dialog content
├── help.html                  Tutorial loaded by index.html
├── faq.html                   FAQ loaded by index.html
├── example.json               Dataset loaded by the example-data action
├── iris.json                  Additional Iris dataset
├── favicon.ico                Site icon
├── LICENSE                    Apache License 2.0
├── assets/
│   ├── boxplot.js             Chart.js box-plot/violin-plot integration
│   ├── help.html              Copy of the tutorial page
│   ├── modal/                 Tutorial screenshots of selection dialogs
│   └── export/                Tutorial screenshots of example results
├── modal/                     Variable-selection dialogs loaded by the app
├── export/                    Result and chart pages loaded by the app
└── execs/                     Python analysis and XLSX conversion modules
```

The `modal/` and `export/` directories each contain pages for ANOVA, Naive Bayes, bar/box/line/pie/radar/scatter charts, clustering, random forest, linear/logistic regression, MANOVA, MDS, PCA, the three *t*-tests, SVM, and decision tree. They also contain `volcano.html` templates that are not linked from the main page's menu. The corresponding analysis modules in `execs/` are `anova.py`, `bayes.py`, `cluster.py`, `forest.py`, `linear.py`, `logistic.py`, `manova.py`, `mds.py`, `pca.py`, `student.py`, `svm.py`, and `tree.py`; `xlsx2json.py` handles workbook conversion. The three *t*-test pages share `student.py`.

When adding or changing a feature, keep its menu entry in `index.html`, selection dialog in `modal/`, result page in `export/`, and any required Python module in `execs/` consistent. Confirm that imports are available in the Pyodide runtime and that local resources load when served over HTTP.

## Development notes and limitations

- This is a static site: the repository has no package manifest, Python requirements file, build configuration, automated test suite, or checked-in deployment workflow.
- The runtime depends on third-party CDNs and dynamically fetched Python packages. Offline operation and fully reproducible dependency versions are not configured.
- Statistical methods have assumptions and input requirements. Review those requirements for the data and question at hand; the application is an educational aid rather than validated software for consequential decisions.

## License

The project includes an Apache License 2.0 in `LICENSE`.
