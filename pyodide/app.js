const canvas = document.querySelector("#gas-canvas");
const context = canvas.getContext("2d");
const statusElement = document.querySelector("#status");
const runtimeElement = document.querySelector("#runtime");
const countInput = document.querySelector("#particle-count");
const temperatureInput = document.querySelector("#temperature");
const resetButton = document.querySelector("#reset");

let pyodide;
let advanceSimulation;
let getSimulationState;
let simulationState;
let lastFrameTime = 0;

function updateControlLabels() {
  document.querySelector("#count-output").value = countInput.value;
  document.querySelector("#temperature-output").value =
    Number(temperatureInput.value).toFixed(1);
}

function resizeCanvas() {
  const bounds = canvas.getBoundingClientRect();
  const pixelRatio = window.devicePixelRatio || 1;
  canvas.width = Math.round(bounds.width * pixelRatio);
  canvas.height = Math.round(bounds.height * pixelRatio);
  context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
  draw();
}

function draw() {
  if (!simulationState) return;

  const bounds = canvas.getBoundingClientRect();
  const scaleX = bounds.width / simulationState.width;
  const scaleY = bounds.height / simulationState.height;
  context.clearRect(0, 0, bounds.width, bounds.height);

  for (const [x, y] of simulationState.particles) {
    const px = x * scaleX;
    const py = y * scaleY;
    context.beginPath();
    context.arc(px, py, 3.1, 0, Math.PI * 2);
    context.fillStyle = "#73d5ff";
    context.shadowColor = "#73d5ff";
    context.shadowBlur = 8;
    context.fill();
  }
  context.shadowBlur = 0;
}

function updateMetrics() {
  document.querySelector("#measured-temperature").textContent =
    simulationState.temperature.toFixed(2);
  document.querySelector("#pressure").textContent =
    simulationState.pressure.toFixed(3);
  document.querySelector("#energy").textContent =
    simulationState.energy.toFixed(1);
}

function readState() {
  simulationState = JSON.parse(getSimulationState());
  updateMetrics();
  draw();
}

function resetSimulation() {
  const initialize = pyodide.globals.get("initialize");
  try {
    initialize(Number(countInput.value), Number(temperatureInput.value), Date.now());
  } finally {
    initialize.destroy();
  }
  readState();
  statusElement.textContent = "Running";
}

function animate(time) {
  if (lastFrameTime !== 0) {
    const dt = Math.min((time - lastFrameTime) / 1000, 0.05);
    advanceSimulation(dt);
    readState();
  }
  lastFrameTime = time;
  requestAnimationFrame(animate);
}

async function start() {
  try {
    statusElement.textContent = "Downloading Python WebAssembly runtime…";
    pyodide = await loadPyodide();
    statusElement.textContent = "Loading simulation code…";

    const response = await fetch("./simulation.py");
    if (!response.ok) {
      throw new Error(`Could not load simulation.py (${response.status})`);
    }
    pyodide.runPython(await response.text());

    advanceSimulation = pyodide.globals.get("advance");
    getSimulationState = pyodide.globals.get("state_json");
    resetSimulation();
    resetButton.disabled = false;
    runtimeElement.textContent = `Python ${pyodide.version} · WebAssembly`;
    requestAnimationFrame(animate);
  } catch (error) {
    console.error(error);
    statusElement.textContent = "Could not start the simulation.";
    runtimeElement.textContent = error.message;
  }
}

countInput.addEventListener("input", updateControlLabels);
temperatureInput.addEventListener("input", updateControlLabels);
resetButton.addEventListener("click", resetSimulation);
window.addEventListener("resize", resizeCanvas);

updateControlLabels();
resizeCanvas();
start();
