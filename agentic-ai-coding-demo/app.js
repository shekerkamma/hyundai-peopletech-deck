const workflowSteps = [
  {
    title: "Frame the outcome",
    tag: "Human-owned",
    body: "Decide the user-visible result, scope it to one reviewable unit, and keep product judgment outside the agent."
  },
  {
    title: "Attach source context",
    tag: "Reference first",
    body: "Point the agent at local source, official docs, or relevant repo folders before it guesses package APIs."
  },
  {
    title: "Build the minimum",
    tag: "Small diff",
    body: "Ask for the smallest working implementation. Avoid broad refactors while the feature is still taking shape."
  },
  {
    title: "Clean repeated mechanics",
    tag: "Service layer",
    body: "After it works, extract duplicated parsing, API calls, validation, or runtime mechanics without changing behavior."
  },
  {
    title: "Run review loops",
    tag: "Feedback",
    body: "Read the diff, address real review comments, add tests where useful, and stop when checks pass or a human decision is needed."
  },
  {
    title: "Ship and learn",
    tag: "Launch",
    body: "Prefer a tested, narrow MVP with feedback over a hidden project waiting for one more feature."
  }
];

const references = [
  {
    id: "agentic",
    title: "Agentic Engineering Workflow",
    path: "skills/agentic-engineering-workflow/SKILL.md",
    localPath: "agentic-ai-coding-demo/reference-context/repos/micky-podcast-agentic-engineering/skills/agentic-engineering-workflow/SKILL.md",
    note: "Use as the high-level operating model: small tasks, focused context, cleanup, review, launch, and security."
  },
  {
    id: "cleanup",
    title: "Code Structure Cleanup",
    path: "skills/code-structure-cleanup/SKILL.md",
    localPath: "agentic-ai-coding-demo/reference-context/repos/micky-podcast-agentic-engineering/skills/code-structure-cleanup/SKILL.md",
    note: "Use after a feature works to move repeated mechanics into service-layer modules."
  },
  {
    id: "grep",
    title: "Grep Loop Review Workflow",
    path: "skills/grep-loop-review-workflow/SKILL.md",
    localPath: "agentic-ai-coding-demo/reference-context/repos/micky-podcast-agentic-engineering/skills/grep-loop-review-workflow/SKILL.md",
    note: "Use when a small PR has actionable review feedback and objective checks."
  },
  {
    id: "local",
    title: "Local PeopleTech Customer Review Skill",
    path: "tooling/peopletech-ai-layer/skills/customer-facing-review/SKILL.md",
    localPath: "tooling/peopletech-ai-layer/skills/customer-facing-review/SKILL.md",
    note: "Use before Hyundai-facing deliverables to check framing, confidentiality, and architecture consistency."
  }
];

const reviewStates = [
  {
    score: "2/5",
    label: "Needs focused fixes",
    fixed: 0,
    items: [
      "Diff mixes demo UI with unrelated deck changes.",
      "Prompt generator does not state a stop condition.",
      "No verification checklist is visible."
    ]
  },
  {
    score: "3/5",
    label: "Closer, but incomplete",
    fixed: 1,
    items: [
      "Unrelated deck changes are out of scope.",
      "Prompt generator now states a stop condition.",
      "Verification checklist still needs objective checks."
    ]
  },
  {
    score: "4/5",
    label: "Nearly merge-ready",
    fixed: 2,
    items: [
      "Scope is clean.",
      "Prompt generator states a stop condition.",
      "Add one final test/typecheck note before shipping."
    ]
  },
  {
    score: "5/5",
    label: "Merge-ready",
    fixed: 3,
    items: [
      "Scope is clean.",
      "Prompt generator states a stop condition.",
      "Verification checklist includes objective checks."
    ]
  }
];

const workflowGrid = document.querySelector("#workflowGrid");
const referenceList = document.querySelector("#referenceList");
const contextPack = document.querySelector("#contextPack");
const taskInput = document.querySelector("#taskInput");
const promptText = document.querySelector("#promptText");
const scoreValue = document.querySelector("#scoreValue");
const scoreLabel = document.querySelector("#scoreLabel");
const reviewItems = document.querySelector("#reviewItems");

let reviewIndex = 0;

function renderWorkflow() {
  workflowGrid.innerHTML = workflowSteps.map((step, index) => `
    <article class="step-card">
      <header>
        <div>
          <span class="step-index">${String(index + 1).padStart(2, "0")}</span>
          <h3>${step.title}</h3>
        </div>
        <span class="pill">${step.tag}</span>
      </header>
      <p>${step.body}</p>
    </article>
  `).join("");
}

function renderReferences() {
  referenceList.innerHTML = references.map((reference, index) => `
    <label class="reference-card">
      <input type="checkbox" value="${reference.id}" ${index < 3 ? "checked" : ""} />
      <span>
        <strong>${reference.title}</strong>
        <p>${reference.note}</p>
      </span>
    </label>
  `).join("");

  referenceList.addEventListener("change", updateContextPack);
  updateContextPack();
}

function getSelectedReferences() {
  const selectedIds = [...referenceList.querySelectorAll("input:checked")].map((input) => input.value);
  return references.filter((reference) => selectedIds.includes(reference.id));
}

function updateContextPack() {
  const selected = getSelectedReferences();
  contextPack.textContent = selected.map((reference) => `- ${reference.title}\n  Source path: ${reference.path}\n  Local context path: ${reference.localPath}\n  Use for: ${reference.note}`).join("\n\n") || "Select at least one reference before asking an agent to code.";
}

function buildPrompt() {
  const referencesText = getSelectedReferences().map((reference) => `- ${reference.localPath}: ${reference.note}`).join("\n");
  const task = taskInput.value.trim() || "<describe the feature or fix>";

  promptText.textContent = `We are going to build this using an agentic engineering workflow.

Task:
${task}

Rules:
1. Keep the change small and reviewable.
2. Search the existing code before creating new abstractions.
3. Use these references before guessing APIs or workflow mechanics:
${referencesText || "- No references selected yet."}
4. Build the minimal working version first.
5. After it works, run a code-structure cleanup pass for duplicated mechanics.
6. Run relevant tests, typechecks, or static validation.
7. Stop only when the feature works, objective checks pass, and unresolved decisions are listed for a human.`;
}

function renderReview() {
  const state = reviewStates[reviewIndex];
  scoreValue.textContent = state.score;
  scoreValue.style.color = state.score === "5/5" ? "var(--green)" : state.score === "4/5" ? "var(--gold)" : "var(--red)";
  scoreLabel.textContent = state.label;
  reviewItems.innerHTML = state.items.map((item, index) => `
    <li class="${index < state.fixed ? "is-fixed" : ""}">${item}</li>
  `).join("");
}

function bindNavigation() {
  document.querySelectorAll(".nav-button").forEach((button) => {
    button.addEventListener("click", () => {
      document.querySelectorAll(".nav-button").forEach((navButton) => navButton.classList.remove("is-active"));
      document.querySelectorAll(".panel").forEach((panel) => panel.classList.remove("is-active"));
      button.classList.add("is-active");
      document.querySelector(`#${button.dataset.panel}`).classList.add("is-active");
    });
  });
}

document.querySelector("#generatePrompt").addEventListener("click", buildPrompt);
document.querySelector("#resetPrompt").addEventListener("click", () => {
  taskInput.value = "Add a small demo feature that helps a user compare agentic coding workflows against normal chatbot prompting.";
  buildPrompt();
});
document.querySelector("#runLoop").addEventListener("click", () => {
  reviewIndex = Math.min(reviewIndex + 1, reviewStates.length - 1);
  renderReview();
});

renderWorkflow();
renderReferences();
buildPrompt();
renderReview();
bindNavigation();
