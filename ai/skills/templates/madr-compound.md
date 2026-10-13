<!-- Compound Architectural Decision Record (MADR Compound) -->
<!-- Combines MADR 4.0 clarity with Google Design Doc architectural rigor -->

---
status: "{proposed | accepted | rejected}"
date: {YYYY-MM-DD}
decision-makers: Artur
consulted: Joi
---

# Architecture Decision Record: {Task / Module Title}

## 1. Context
{1 concise paragraph (2-5 sentences) based on the BRD synthesizing the technical landscape, environment constraints, and the system verification goal (the architectural fitness function / closed-loop termination condition). Focus strictly on forces driving architectural trade-offs, avoiding duplication of functional specs or API payloads.}

## 2. Decision Summary (Executive Overview)
| # | Problem Statement | Chosen Option (Accepted) | Rationale |
|---|-------------------|--------------------------|-----------|
| 1 | {Short problem 1} | {Chosen option title}    | {One-sentence primary reason} |
| 2 | {Short problem 2} | {Chosen option title}    | {One-sentence primary reason} |

---

## 3. Detailed Decisions & Trade-Offs

### Decision 1: {Problem Statement Title}

#### Problem & Drivers
{Brief explanation of the specific trade-off, architectural forces, and constraints.}

#### Considered Options

##### Option 1.1: {Option Name} ({ACCEPTED | REJECTED})
* **Description**: {Concise technical description of this approach}
* **Data Engineering & Performance**: {Impact on latency, token usage, compute resources, monitoring, and telemetry/observability}
* **Cost & FinOps**: {Inference costs, resource efficiency, free-tier compliance}
* **Security & Reliability**: {Blast radius, defensive guardrails, failure recovery, anti-tamper, evaluation}
* **Pros & Cons**:
  * Good, because {positive quality}
  * Bad / Trade-off, because {drawback or overhead}

##### Option 1.2: {Alternative Option Name} ({ACCEPTED | REJECTED})
* **Description**: {Concise technical description of the alternative}
* **Data Engineering & Performance**: {Impact on latency, token usage, compute resources, monitoring, and telemetry/observability}
* **Cost & FinOps**: {Inference costs, resource efficiency, free-tier compliance}
* **Security & Reliability**: {Blast radius, defensive guardrails, failure recovery, anti-tamper, evaluation}
* **Pros & Cons**:
  * Good, because {positive quality}
  * Bad / Trade-off, because {drawback or overhead}

#### Consequences
* **Positive**: {Key architectural benefits gained}
* **Negative / Trade-offs**: {Accepted complexities or limitations}
* **Confirmation**: {How adherence will be verified via unit tests, integration tests, or audit metrics}

---

## 4. Technical Baseline Divergence (GEMINI.md)
None

<!-- If divergences exist, replace with:
## 4. Technical Baseline Alignment (GEMINI.md)
{e.g. 90%}
Divergences:
- {Divergence point 1}
  - Reason: {Specific rationale}
- {Divergence point 2}
  - Reason: {Specific rationale}
-->

---

## 5. More Information

* **Related Documents**:
  - [BRD.md](BRD.md)
  - [{Architectural Pattern or Guide}](path/to/reference.md)
