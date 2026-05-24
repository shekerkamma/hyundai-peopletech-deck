function summarizeEvents(events) {
  const total = events.length;
  const holds = events.filter((event) => event.decision.status === "hold").length;
  const inspections = events.filter((event) => event.decision.status === "inspect").length;
  const avgRisk = total
    ? Math.round(events.reduce((sum, event) => sum + event.decision.escapeRisk, 0) / total)
    : 0;
  const worst = events.reduce((current, event) => (
    !current || event.decision.escapeRisk > current.decision.escapeRisk ? event : current
  ), null);

  return {
    total,
    holds,
    inspections,
    avgRisk,
    worst
  };
}

function createIncidentReport(events, activeVariant, modelVersion) {
  const summary = summarizeEvents(events);
  const holdEvents = events.filter((event) => event.decision.status === "hold");
  const inspectEvents = events.filter((event) => event.decision.status === "inspect");
  const reportId = `UC05-${new Date().toISOString().slice(0, 10)}-${String(summary.total).padStart(3, "0")}`;

  const recommendation = holdEvents.length > 0
    ? "Hold affected units, open station-level rework tickets, and trigger quality engineer review before releasing the batch."
    : inspectEvents.length > 0
      ? "Route next units through inspection and monitor whether drift clears after shift stabilization."
      : "Continue production and retain telemetry as baseline evidence.";

  return {
    id: reportId,
    generatedAt: new Date().toLocaleString(),
    variant: activeVariant.name,
    modelVersion,
    summary,
    recommendation,
    markdown: [
      `# UC05 Predictive Quality Incident Report`,
      ``,
      `Report: ${reportId}`,
      `Generated: ${new Date().toLocaleString()}`,
      `Variant: ${activeVariant.name}`,
      `Model version: ${modelVersion}`,
      ``,
      `## Batch Summary`,
      `- Units scored: ${summary.total}`,
      `- Average escape risk: ${summary.avgRisk}%`,
      `- Inspection routes: ${summary.inspections}`,
      `- Line holds: ${summary.holds}`,
      summary.worst ? `- Highest-risk unit: ${summary.worst.id} at ${summary.worst.decision.escapeRisk}%` : `- Highest-risk unit: none`,
      ``,
      `## MES Recommendation`,
      recommendation,
      ``,
      `## Evidence`,
      ...events.slice(0, 8).map((event) => `- ${event.timestamp} · ${event.id} · ${event.decision.escapeRisk}% · ${event.decision.action}`)
    ].join("\n")
  };
}

function createRetrainingSummary(events, activeVariant, currentVersion, nextVersion) {
  const summary = summarizeEvents(events);
  const driftStations = new Map();

  events.forEach((event) => {
    event.stationResults.forEach((result) => {
      if (result.driftScore > 1.2 || result.status !== "clear") {
        const current = driftStations.get(result.station.name) || { count: 0, maxScore: 0 };
        current.count += 1;
        current.maxScore = Math.max(current.maxScore, result.score);
        driftStations.set(result.station.name, current);
      }
    });
  });

  const driftLines = [...driftStations.entries()].map(([station, data]) => (
    `- ${station}: ${data.count} drift signals, max station risk ${data.maxScore}%`
  ));

  return {
    id: `RETRAIN-${nextVersion}`,
    generatedAt: new Date().toLocaleString(),
    markdown: [
      `# Model Retraining Summary`,
      ``,
      `Variant: ${activeVariant.name}`,
      `Current model: ${currentVersion}`,
      `Candidate model: ${nextVersion}`,
      ``,
      `## Trigger`,
      summary.holds > 0
        ? `Line holds detected in the current batch. Retraining candidate should be reviewed before next shift.`
        : `Inspection routes or drift signals detected. Candidate model can be prepared for shadow validation.`,
      ``,
      `## Drift Signals`,
      driftLines.length ? driftLines.join("\n") : `- No significant station drift detected.`,
      ``,
      `## Validation Gates`,
      `- Backtest against last 100 scored units.`,
      `- Confirm false-positive rate does not exceed pilot target.`,
      `- Run edge latency check before deployment.`,
      `- Promote only after quality engineer approval.`
    ].join("\n")
  };
}

window.ArtifactService = {
  createIncidentReport,
  createRetrainingSummary,
  summarizeEvents
};
