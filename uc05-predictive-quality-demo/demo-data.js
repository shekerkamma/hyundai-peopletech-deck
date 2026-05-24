window.demoVariants = [
  {
    id: "ioniq5",
    code: "NE",
    name: "IONIQ 5 · EV crossover",
    stations: [
      { id: "body-weld", name: "Body weld", metric: "gap variance mm", mean: 0.18, sigma: 0.035, limit: 0.34, driftSensitivity: 0.045, speedSensitivity: 0.036 },
      { id: "battery-seal", name: "Battery seal", metric: "thermal leak index", mean: 0.11, sigma: 0.032, limit: 0.27, driftSensitivity: 0.06, speedSensitivity: 0.022 },
      { id: "paint-booth", name: "Paint booth", metric: "film drift index", mean: 0.21, sigma: 0.044, limit: 0.41, driftSensitivity: 0.052, speedSensitivity: 0.034 },
      { id: "final-torque", name: "Final torque", metric: "torque residual Nm", mean: 0.16, sigma: 0.038, limit: 0.32, driftSensitivity: 0.038, speedSensitivity: 0.05 }
    ]
  },
  {
    id: "santafe",
    code: "MX5",
    name: "Santa Fe · SUV",
    stations: [
      { id: "body-weld", name: "Body weld", metric: "gap variance mm", mean: 0.2, sigma: 0.042, limit: 0.4, driftSensitivity: 0.052, speedSensitivity: 0.038 },
      { id: "door-fitment", name: "Door fitment", metric: "flushness delta mm", mean: 0.15, sigma: 0.036, limit: 0.31, driftSensitivity: 0.044, speedSensitivity: 0.032 },
      { id: "paint-booth", name: "Paint booth", metric: "orange-peel index", mean: 0.18, sigma: 0.04, limit: 0.38, driftSensitivity: 0.058, speedSensitivity: 0.03 },
      { id: "final-torque", name: "Final torque", metric: "torque residual Nm", mean: 0.18, sigma: 0.04, limit: 0.35, driftSensitivity: 0.04, speedSensitivity: 0.052 }
    ]
  },
  {
    id: "palisade",
    code: "LX3",
    name: "Palisade · large SUV",
    stations: [
      { id: "body-weld", name: "Body weld", metric: "gap variance mm", mean: 0.24, sigma: 0.046, limit: 0.46, driftSensitivity: 0.054, speedSensitivity: 0.042 },
      { id: "seat-install", name: "Seat install", metric: "mounting offset mm", mean: 0.17, sigma: 0.034, limit: 0.33, driftSensitivity: 0.042, speedSensitivity: 0.028 },
      { id: "paint-booth", name: "Paint booth", metric: "film drift index", mean: 0.2, sigma: 0.042, limit: 0.4, driftSensitivity: 0.06, speedSensitivity: 0.032 },
      { id: "final-torque", name: "Final torque", metric: "torque residual Nm", mean: 0.2, sigma: 0.044, limit: 0.38, driftSensitivity: 0.044, speedSensitivity: 0.056 }
    ]
  }
];
