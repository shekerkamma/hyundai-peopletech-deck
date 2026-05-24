const variants = window.demoVariants;
const contexts = [
  {
    title: "UC05 predictive quality specification",
    path: "build_ml_pipeline_deck.js and hyundai-ml-pipeline-strategy.md",
    use: "Pilot scope, metrics, SDF problem framing, and MES closed-loop behavior."
  },
  {
    title: "OpenHands AGENTS.md pattern",
    path: "https://github.com/OpenHands/OpenHands/blob/main/AGENTS.md",
    use: "Repo guidance, frontend/backend boundaries, test rules, and agent working conventions."
  },
  {
    title: "OpenHands skills/microagent pattern",
    path: "OpenHands skills and .openhands guidance",
    use: "Markdown instructions with triggers that inject domain knowledge only when useful."
  },
  {
    title: "Code structure cleanup skill",
    path: "skills/code-structure-cleanup/SKILL.md",
    use: "Separate cleanup pass for duplicated API calls, parsing, validation, and service-layer mechanics."
  }
];

const agentSteps = [
  {
    title: "Schema agent",
    detail: "Reads defect DB, historian stream, and tolerance-table schemas. Produces station feature contracts."
  },
  {
    title: "Training agent",
    detail: "Generates PyTorch baseline models per variant and test fixtures for synthetic drift cases."
  },
  {
    title: "Edge optimization agent",
    detail: "Exports ONNX/TensorRT artifacts and validates the <200ms station inference budget."
  },
  {
    title: "MES connector agent",
    detail: "Implements quality-gate actions: continue, inspect, hold, and rework ticket creation."
  },
  {
    title: "Review loop agent",
    detail: "Runs typechecks, regression tests, and reviewer feedback until the PR is merge-ready."
  }
];

let activeVariant = variants[0];
let engine = window.QualityEngine.createQualityEngine(activeVariant);
let drift = 0;
let agentProgress = 1;
let running = false;
let timer = null;
let latestUnit = null;
let eventLog = [];
let modelVersionIndex = 0;
let artifacts = [];
let activeArtifactId = null;
let buildLog = [
  "Plan created: split UC05 demo into data schema, scoring engine, UI controller, and artifact service.",
  "Reference pack loaded: UC05 strategy, OpenHands AGENTS pattern, code-structure cleanup skill."
];
const modelVersions = [
  {
    id: "v1.0 baseline",
    note: "Initial thresholds from historical SDF defect data.",
    change: "Baseline station means, sigmas, and quality limits."
  }
];

const variantSelect = document.querySelector("#variantSelect");
const lineSpeed = document.querySelector("#lineSpeed");
const stationGrid = document.querySelector("#stationGrid");
const gateStatus = document.querySelector("#gateStatus");
const riskScore = document.querySelector("#riskScore");
const mesAction = document.querySelector("#mesAction");
const detectionRate = document.querySelector("#detectionRate");
const falsePositive = document.querySelector("#falsePositive");
const latency = document.querySelector("#latency");
const agentList = document.querySelector("#agentList");
const contextList = document.querySelector("#contextList");
const starterPrompt = document.querySelector("#starterPrompt");
const runLine = document.querySelector("#runLine");
const unitLog = document.querySelector("#unitLog");
const eventCount = document.querySelector("#eventCount");
const holdCount = document.querySelector("#holdCount");
const inspectedCount = document.querySelector("#inspectedCount");
const artifactTabs = document.querySelector("#artifactTabs");
const artifactPreview = document.querySelector("#artifactPreview");
const versionList = document.querySelector("#versionList");
const modelVersionPill = document.querySelector("#modelVersionPill");
const buildConsole = document.querySelector("#buildConsole");
const backendStatus = document.querySelector("#backendStatus");
const backendEventCount = document.querySelector("#backendEventCount");
const backendIncidentCount = document.querySelector("#backendIncidentCount");
const backendPreview = document.querySelector("#backendPreview");

function statusClass(status) {
  return status === "hold" ? "stop" : status === "inspect" ? "warn" : "";
}

function renderVariants() {
  variantSelect.innerHTML = variants.map((variant) => `<option value="${variant.id}">${variant.name}</option>`).join("");
}

function scoreUnit() {
  latestUnit = engine.nextUnit(Number(lineSpeed.value));
  latestUnit.modelVersion = modelVersions[modelVersionIndex].id;
  eventLog.unshift(latestUnit);
  eventLog = eventLog.slice(0, 100);
  renderStations();
  renderDecision();
  renderEventLog();
  renderArtifacts();
}

function renderStations() {
  if (!latestUnit) {
    scoreUnit();
    return;
  }

  stationGrid.innerHTML = latestUnit.stationResults.map((result) => `
    <div class="station-card">
      <div>
        <strong>${result.station.name}</strong>
        <p>${result.station.metric}</p>
      </div>
      <div>
        <div class="bar-track">
          <div class="bar ${statusClass(result.status)}" style="width: ${result.score}%"></div>
        </div>
        <p>Observed ${result.value.toFixed(3)} vs limit ${result.station.limit.toFixed(3)} · z ${result.zScore.toFixed(1)}</p>
      </div>
      <div class="delta">${result.score}%</div>
    </div>
  `).join("");
}

function renderDecision() {
  const { decision } = latestUnit;
  const cssStatus = statusClass(decision.status);
  gateStatus.className = `status-pill ${cssStatus}`;
  mesAction.className = `action-box ${cssStatus}`;

  const copy = {
    clear: "MES action: continue production. Store telemetry and keep recalibrating per active variant.",
    inspect: "MES action: route next unit to inspection, flag station drift, and continue unless the next unit worsens.",
    hold: "MES action: hold the unit, create rework ticket, attach station telemetry, and require quality sign-off."
  };

  gateStatus.textContent = decision.action.replaceAll("_", " ");
  mesAction.textContent = copy[decision.status];
  riskScore.textContent = `${decision.escapeRisk}%`;

  const inspected = eventLog.filter((event) => event.decision.status === "inspect").length;
  const holds = eventLog.filter((event) => event.decision.status === "hold").length;
  const qualityPressure = Math.min(1, (inspected + holds * 2) / Math.max(1, eventLog.length * 0.8));
  detectionRate.textContent = `${(96.2 - qualityPressure * 4.8).toFixed(1)}%`;
  falsePositive.textContent = `${(2.9 + qualityPressure * 3.6).toFixed(1)}%`;
  latency.textContent = `${Math.round(112 + Number(lineSpeed.value) * 0.82 + drift * 9)}ms`;
}

function renderEventLog() {
  const holds = eventLog.filter((event) => event.decision.status === "hold").length;
  const inspected = eventLog.filter((event) => event.decision.status === "inspect").length;

  eventCount.textContent = String(eventLog.length);
  holdCount.textContent = String(holds);
  inspectedCount.textContent = String(inspected);

  unitLog.innerHTML = eventLog.slice(0, 14).map((event) => `
    <tr>
      <td>${event.timestamp}</td>
      <td>${event.id}</td>
      <td>${event.variant}</td>
      <td>${event.decision.escapeRisk}%</td>
      <td><span class="table-pill ${statusClass(event.decision.status)}">${event.decision.action.replaceAll("_", " ")}</span></td>
    </tr>
  `).join("");
}

function renderAgents() {
  agentList.innerHTML = agentSteps.map((step, index) => `
    <div class="agent-step ${index < agentProgress ? "is-done" : ""}">
      <span>${index < agentProgress ? "✓" : index + 1}</span>
      <div>
        <strong>${step.title}</strong>
        <p>${step.detail}</p>
      </div>
    </div>
  `).join("");
  renderBuildConsole();
}

function renderBuildConsole() {
  buildConsole.innerHTML = buildLog.slice(-8).map((item, index) => `
    <div><span>${String(index + 1).padStart(2, "0")}</span>${item}</div>
  `).join("");
}

function renderContext() {
  contextList.innerHTML = contexts.map((context, index) => `
    <div class="context-item">
      <span>${index + 1}</span>
      <div>
        <strong>${context.title}</strong>
        <p>${context.path}<br />${context.use}</p>
      </div>
    </div>
  `).join("");

  starterPrompt.textContent = `Task: Build a working UC05 Predictive Quality demo, not a storyboard.

Context to inspect first:
- hyundai-ml-pipeline-strategy.md: UC05 pilot scope and ROI
- build_ml_pipeline_deck.js: UC05 problem, solution, metrics, OpenHands realization
- second-brain/github/openhands-openhands.md: OpenHands component mapping
- uc05-predictive-quality-demo/quality-engine.js: scoring engine
- uc05-predictive-quality-demo/demo-data.js: variant tolerance schema

Rules:
1. Keep the app static and locally runnable.
2. Implement actual event simulation, station scoring, drift detection, and MES decisions.
3. Keep scoring mechanics in a service-layer module.
4. Show OpenHands as the development acceleration layer, not as fake runtime magic.
5. Verify JavaScript syntax and summarize assumptions.`;
}

function setRunning(nextRunning) {
  running = nextRunning;
  runLine.textContent = running ? "Pause line" : "Run line";
  if (timer) {
    clearInterval(timer);
    timer = null;
  }
  if (running) {
    timer = setInterval(scoreUnit, 1200);
  }
}

function currentVersion() {
  return modelVersions[modelVersionIndex].id;
}

function addArtifact(type, report) {
  const artifact = {
    id: `${type}-${Date.now()}`,
    type,
    title: type === "incident" ? "Incident report" : "Retraining brief",
    createdAt: new Date().toLocaleTimeString(),
    markdown: report.markdown
  };
  artifacts.unshift(artifact);
  artifacts = artifacts.slice(0, 8);
  activeArtifactId = artifact.id;
  buildLog.push(`Artifact generated: ${artifact.title} from ${eventLog.length} scored unit events.`);
  renderArtifacts();
  renderAgents();
}

function renderArtifacts() {
  if (!artifacts.length) {
    artifactTabs.innerHTML = "";
    artifactPreview.textContent = "Generate an incident report or retraining brief after scoring a few units.";
    return;
  }

  artifactTabs.innerHTML = artifacts.map((artifact) => `
    <button class="${artifact.id === activeArtifactId ? "is-active" : ""}" type="button" data-artifact-id="${artifact.id}">
      ${artifact.title} · ${artifact.createdAt}
    </button>
  `).join("");

  const active = artifacts.find((artifact) => artifact.id === activeArtifactId) || artifacts[0];
  artifactPreview.textContent = active.markdown;
}

function renderVersions() {
  modelVersionPill.textContent = currentVersion();
  versionList.innerHTML = modelVersions.map((version, index) => `
    <div class="version-card ${index === modelVersionIndex ? "is-active" : ""}">
      <strong>${version.id}</strong>
      <p>${version.note}</p>
      <span>${version.change}</span>
    </div>
  `).join("");
}

function backendEventToLocalEvent(event) {
  return {
    id: event.event_id,
    timestamp: new Date(event.timestamp).toLocaleTimeString(),
    variant: event.model_variant,
    lineSpeed: event.line_speed,
    modelVersion: event.prediction.model_version,
    stationResults: event.station_results.map((result) => ({
      station: {
        id: result.station_id,
        name: result.station_name,
        metric: result.metric,
        limit: result.limit
      },
      value: result.value,
      score: result.score,
      zScore: result.z_score,
      driftScore: 0,
      status: result.status
    })),
    decision: {
      status: event.prediction.status,
      action: event.mes_action.action,
      escapeRisk: event.prediction.escape_risk
    },
    backendPayload: event
  };
}

async function checkBackend() {
  try {
    const [health, incidents, versions] = await Promise.all([
      window.BackendClient.health(),
      window.BackendClient.incidents(),
      window.BackendClient.modelVersions()
    ]);
    backendStatus.textContent = health.ok ? "Connected" : "Unavailable";
    backendIncidentCount.textContent = String(incidents.incidents.length);
    backendPreview.textContent = JSON.stringify({ health, model_versions: versions.model_versions.slice(0, 3) }, null, 2);
    buildLog.push("Backend connected: API, SQLite store, incidents, and model versions are reachable.");
    renderAgents();
  } catch (error) {
    backendStatus.textContent = "Offline";
    backendPreview.textContent = `${error.message}\n\nStart it with:\npython3 backend/server.py`;
  }
}

async function scoreViaBackend() {
  try {
    const response = await window.BackendClient.generateEvent({
      variant_id: activeVariant.id,
      line_speed: Number(lineSpeed.value),
      drift
    });
    latestUnit = backendEventToLocalEvent(response.event);
    eventLog.unshift(latestUnit);
    eventLog = eventLog.slice(0, 100);
    backendPreview.textContent = JSON.stringify(response.event, null, 2);
    renderStations();
    renderDecision();
    renderEventLog();
    await loadBackendEvents(false);
  } catch (error) {
    backendStatus.textContent = "Offline";
    backendPreview.textContent = `${error.message}\n\nStart it with:\npython3 backend/server.py`;
  }
}

async function loadBackendEvents(updatePreview = true) {
  try {
    const [events, incidents] = await Promise.all([
      window.BackendClient.events(25),
      window.BackendClient.incidents()
    ]);
    backendStatus.textContent = "Connected";
    backendEventCount.textContent = String(events.events.length);
    backendIncidentCount.textContent = String(incidents.incidents.length);
    if (events.events.length) {
      eventLog = events.events.map(backendEventToLocalEvent);
      latestUnit = eventLog[0];
      renderStations();
      renderDecision();
      renderEventLog();
    }
    if (updatePreview) {
      backendPreview.textContent = JSON.stringify({
        events: events.events.slice(0, 3),
        incidents: incidents.incidents.slice(0, 3)
      }, null, 2);
    }
  } catch (error) {
    backendStatus.textContent = "Offline";
    backendPreview.textContent = `${error.message}\n\nStart it with:\npython3 backend/server.py`;
  }
}

function retrainModel() {
  const nextIndex = modelVersions.length;
  const nextVersion = `v1.${nextIndex} shadow`;
  const summary = window.ArtifactService.summarizeEvents(eventLog);
  const adjustment = summary.holds > 0
    ? "Raised hold sensitivity on stations with repeated drift and added shift-transition guard band."
    : "Tuned inspection threshold using latest batch telemetry and prepared shadow validation.";

  modelVersions.push({
    id: nextVersion,
    note: `Candidate generated from ${summary.total} scored units on ${activeVariant.name}.`,
    change: adjustment
  });
  modelVersionIndex = modelVersions.length - 1;
  buildLog.push(`Model candidate created: ${nextVersion}. Validation gates added before promotion.`);
  addArtifact("retraining", window.ArtifactService.createRetrainingSummary(
    eventLog,
    activeVariant,
    modelVersions[Math.max(0, modelVersionIndex - 1)].id,
    nextVersion
  ));
  renderVersions();
}

function resetEngine() {
  engine = window.QualityEngine.createQualityEngine(activeVariant, Date.now() % 100000);
  drift = 0;
  engine.setDrift(drift);
  latestUnit = null;
  eventLog = [];
  artifacts = [];
  activeArtifactId = null;
  buildLog.push(`Variant switched to ${activeVariant.name}. Engine reset with ${currentVersion()}.`);
  scoreUnit();
  renderArtifacts();
}

variantSelect.addEventListener("change", (event) => {
  activeVariant = variants.find((variant) => variant.id === event.target.value);
  resetEngine();
});

lineSpeed.addEventListener("input", scoreUnit);

document.querySelector("#runLine").addEventListener("click", () => setRunning(!running));
document.querySelector("#scoreNext").addEventListener("click", scoreUnit);
document.querySelector("#simulateShift").addEventListener("click", () => {
  drift = Math.max(0, drift - 0.45);
  engine.setDrift(drift);
  scoreUnit();
});
document.querySelector("#injectDrift").addEventListener("click", () => {
  drift = Math.min(3.5, drift + 0.75);
  engine.setDrift(drift);
  scoreUnit();
});
document.querySelector("#exportLog").addEventListener("click", () => {
  const blob = new Blob([JSON.stringify(eventLog, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "uc05-quality-events.json";
  link.click();
  URL.revokeObjectURL(url);
});
document.querySelector("#generateIncident").addEventListener("click", () => {
  addArtifact("incident", window.ArtifactService.createIncidentReport(eventLog, activeVariant, currentVersion()));
});
document.querySelector("#generateRetraining").addEventListener("click", () => {
  addArtifact("retraining", window.ArtifactService.createRetrainingSummary(
    eventLog,
    activeVariant,
    currentVersion(),
    `v1.${modelVersions.length} candidate`
  ));
});
document.querySelector("#retrainModel").addEventListener("click", retrainModel);
document.querySelector("#checkBackend").addEventListener("click", checkBackend);
document.querySelector("#scoreBackend").addEventListener("click", scoreViaBackend);
document.querySelector("#loadBackendEvents").addEventListener("click", () => loadBackendEvents(true));
artifactTabs.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-artifact-id]");
  if (!button) {
    return;
  }
  activeArtifactId = button.dataset.artifactId;
  renderArtifacts();
});
document.querySelector("#advanceAgents").addEventListener("click", () => {
  agentProgress = Math.min(agentSteps.length, agentProgress + 1);
  buildLog.push(`Agent step completed: ${agentSteps[agentProgress - 1].title}.`);
  renderAgents();
});

renderVariants();
renderContext();
renderAgents();
renderVersions();
renderArtifacts();
resetEngine();
