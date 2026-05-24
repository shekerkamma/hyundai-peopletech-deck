const statusRank = {
  clear: 0,
  inspect: 1,
  hold: 2
};

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function mean(values) {
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function standardDeviation(values) {
  const avg = mean(values);
  const variance = mean(values.map((value) => (value - avg) ** 2));
  return Math.sqrt(variance);
}

function mulberry32(seed) {
  return function random() {
    let t = seed += 0x6D2B79F5;
    t = Math.imul(t ^ t >>> 15, t | 1);
    t ^= t + Math.imul(t ^ t >>> 7, t | 61);
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

function sampleNormal(random, meanValue, deviation) {
  const u = 1 - random();
  const v = random();
  const z = Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  return meanValue + z * deviation;
}

function calculateStationScore(station, value, history) {
  const zScore = (value - station.mean) / station.sigma;
  const thresholdRatio = value / station.limit;
  const driftWindow = history.slice(-10);
  const driftScore = driftWindow.length >= 4
    ? clamp((mean(driftWindow) - station.mean) / station.sigma, 0, 3)
    : 0;
  const volatility = driftWindow.length >= 4
    ? clamp(standardDeviation(driftWindow) / station.sigma, 0, 2.4)
    : 0;

  const score = clamp(
    22 + zScore * 17 + thresholdRatio * 28 + driftScore * 12 + volatility * 8,
    0,
    99
  );

  let status = "clear";
  if (score >= 82 || value >= station.limit * 1.04) {
    status = "hold";
  } else if (score >= 62 || value >= station.limit * 0.92) {
    status = "inspect";
  }

  return {
    value,
    score: Math.round(score),
    zScore,
    driftScore,
    status
  };
}

function aggregateDecision(stationResults) {
  const maxScore = Math.max(...stationResults.map((result) => result.score));
  const avgScore = Math.round(mean(stationResults.map((result) => result.score)));
  const worstStatus = stationResults.reduce((current, result) => (
    statusRank[result.status] > statusRank[current] ? result.status : current
  ), "clear");

  const actionByStatus = {
    clear: "CONTINUE",
    inspect: "INSPECT_NEXT_UNIT",
    hold: "HOLD_AND_REWORK"
  };

  return {
    status: worstStatus,
    action: actionByStatus[worstStatus],
    escapeRisk: Math.round(maxScore * 0.65 + avgScore * 0.35)
  };
}

function createQualityEngine(variant, seed = 42) {
  const random = mulberry32(seed);
  const stationHistory = Object.fromEntries(variant.stations.map((station) => [station.id, []]));
  let unitIndex = 0;
  let driftLevel = 0;

  function setDrift(level) {
    driftLevel = clamp(level, 0, 3.5);
  }

  function nextUnit(lineSpeed) {
    unitIndex += 1;
    const transitionPulse = unitIndex < 10 ? (10 - unitIndex) * 0.018 : 0;
    const speedPressure = clamp((lineSpeed - 42) / 26, 0, 1);

    const stationResults = variant.stations.map((station, stationIndex) => {
      const stationDrift = driftLevel * station.driftSensitivity;
      const pressure = speedPressure * station.speedSensitivity;
      const wave = Math.sin(unitIndex * 0.58 + stationIndex * 0.9) * station.sigma * 0.45;
      const value = sampleNormal(
        random,
        station.mean + stationDrift + pressure + transitionPulse + wave,
        station.sigma
      );
      const history = stationHistory[station.id];
      history.push(value);
      if (history.length > 40) {
        history.shift();
      }
      return {
        station,
        ...calculateStationScore(station, value, history)
      };
    });

    const decision = aggregateDecision(stationResults);
    return {
      id: `${variant.code}-${String(unitIndex).padStart(5, "0")}`,
      timestamp: new Date().toLocaleTimeString(),
      variant: variant.name,
      lineSpeed,
      stationResults,
      decision
    };
  }

  return {
    nextUnit,
    setDrift
  };
}

window.QualityEngine = {
  createQualityEngine
};
