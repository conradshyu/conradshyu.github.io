# Ideal Gas Simulator (Python + WebAssembly)

A small, interactive ideal-gas demonstration. Particle motion and gas statistics are calculated by Python running in the browser through [Pyodide](https://pyodide.org/), a WebAssembly build of CPython. JavaScript only loads the Python runtime and draws the returned particle positions on a canvas.

## Features

- Adjustable particle count and initial temperature.
- Animated particles reflecting elastically from a rectangular container.
- Live temperature, kinetic-energy, and two-dimensional pressure readouts.
- No server-side application, Python installation, or build step is needed to run the hosted version.
- A standard-library-only simulation module that can also be tested with desktop Python.

## Requirements

- A modern browser with WebAssembly support.
- Python 3.9 or newer to serve the files locally and to run the optional tests.
- Internet access on first load when using the default Pyodide CDN URL. The CDN serves the WebAssembly runtime; `simulation.py` is fetched from this project.

## Run locally

Browsers restrict loading local Python files with `file://`, so serve the project over HTTP instead:

```sh
cd /home/shyu/assembly
python3 -m http.server 8000
```

Open <http://localhost:8000> in a browser. Stop the server with `Ctrl+C`.

## Build and compile

The project does not compile Python source itself. Pyodide provides CPython and its standard library already compiled to WebAssembly; the browser downloads that runtime and executes `simulation.py` inside it. This keeps the project build-free and avoids a separate native Python service.

For a normal deployment, there is no compilation step:

1. Keep `index.html`, `style.css`, `app.js`, and `simulation.py` together.
2. Host the directory on any static web server that serves `index.html` and allows fetching adjacent files.
3. Open the deployed HTTPS page in a WebAssembly-capable browser.

The Pyodide version is pinned in `index.html` (`0.27.7`) so the runtime is reproducible. To upgrade, change the version in the CDN script URL and verify the app in the target browsers.

### Optional: serve Pyodide locally

To avoid a runtime dependency on the CDN or deploy fully offline, download the matching Pyodide distribution and serve its files alongside the application:

```sh
cd /home/shyu/assembly
mkdir -p vendor/pyodide
npm pack pyodide@0.27.7 --pack-destination /tmp
tar -xzf /tmp/pyodide-0.27.7.tgz -C vendor/pyodide --strip-components=1
```

This retrieves the version-pinned Pyodide distribution from npm; it does not install anything into the project or compile the simulator. Change the script in `index.html` to:

```html
<script src="./vendor/pyodide/pyodide.js"></script>
```

Keep all files from that distribution together because `pyodide.js` loads WebAssembly and data files relative to its own URL. For offline operation, cache the application files and the entire Pyodide distribution with a service worker or package them into the deployed static site. Confirm the applicable Pyodide license and notices when redistributing its files.

If you later add third-party Python dependencies, they may need to be installed as Pyodide-compatible packages; native CPython wheels or extensions cannot automatically be used in WebAssembly. This project currently uses only Python's standard library.

## Deploy

The application is static and can be deployed to GitHub Pages, Cloudflare Pages, Netlify, an object-storage static website, or any conventional web server:

1. Upload or publish the project directory as the site's document root.
2. Ensure the server serves `.py` files as fetchable text (a `text/plain` content type is suitable) and serves `.wasm` files as `application/wasm` if self-hosting Pyodide.
3. Use HTTPS for public deployments. Pyodide's WebAssembly assets should be served from the same origin when self-hosted.
4. Visit the site's root URL and wait for the status to change to **Running**.

For GitHub Pages, publish the contents of this directory as the selected Pages source (for example, the `main` branch root or a `gh-pages` branch). No framework-specific build command or output directory is required.

## Physics model and units

This is a deliberately simple **two-dimensional, non-interacting point-particle** model:

- Particle positions move at constant velocity between wall encounters.
- Container walls reverse the velocity component normal to the wall, conserving kinetic energy.
- Particles do not collide with each other; this keeps the simulation an ideal-gas model rather than a hard-sphere gas.
- Velocities are initially sampled from independent Gaussian distributions. With Boltzmann's constant set to `1`, the measured temperature is `T = mean(vx² + vy²) / 2`.
- The displayed pressure uses the 2D ideal-gas relation `P A = N T`, where `A` is the container area. These are dimensionless simulation units, not a prediction in pascals for a real 3D gas.

The finite random sample means the measured initial temperature will usually differ slightly from the slider's requested temperature. Reset to sample a new gas at the selected initial temperature.

## Test the simulation

The browser app has no package installation step. To run the Python unit tests:

```sh
cd /home/shyu/assembly
python3 -m unittest discover -s tests -v
```

The tests check deterministic initialization, wall containment, kinetic-energy conservation, and the ideal-gas pressure relation.

## Project files

| Path | Purpose |
| --- | --- |
| `index.html` | Page structure and pinned Pyodide runtime |
| `app.js` | Runtime loading, controls, animation, and canvas rendering |
| `simulation.py` | Python particle dynamics and thermodynamic readouts |
| `style.css` | Responsive page styling |
| `tests/test_simulation.py` | Desktop Python tests for the simulation |

## Troubleshooting

- **It remains on “Downloading Python WebAssembly runtime…”** — check the browser console and network access to `cdn.jsdelivr.net`, or use the self-hosted setup.
- **The page opens but reports that simulation code could not load** — serve the project through HTTP(S) and confirm `simulation.py` is next to `index.html`.
- **A browser blocks WebAssembly** — use a current browser and serve the page over HTTPS or `localhost`.
- **A deployment shows stale files** — clear the browser cache or configure the host to revalidate these small static assets.
