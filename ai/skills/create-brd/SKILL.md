---
name: create-brd
description: >-
  Extracts task requirements from the lesson markdown or context and creates a structured BRD.md in a context-defined task folder.
author: Artur Fejklowicz
copyright: "Copyright (c) 2026 Artur Fejklowicz"
license: Apache-2.0
version: 1.0.0
updated_at: 2026-10-14
---

# Create BRD (Business Requirements Document)

## Overview
This skill extracts task requirements, constraints, resources, and API interactions from the lesson notes or transcripts, translating and structuring them into a standard `BRD.md` format.

## Quick Start
To trigger this skill, ask:
"Create a BRD.md for this task."

## Workflow

### 1. Locate Lesson Materials
- Scan the current directory, parent directories, or ask the user for context to locate relevant markdown files (e.g., `s[season]e[episode]-*.md`, `lesson.md`, `notes.md`, or transcript files).
- Read the content of these files to identify the section describing the task.

### 2. Standardize Document Structure
Generate a `BRD.md` file. It should be saved in the last lesson task folder by default, or in a folder determined by the conversation context (asking the user if unsure). The document must contain the following sections:
- **Overview**: High-level summary of what the task wants to achieve.
- **Requirements**:
  - Functional requirements (logic, outputs, expectations).
  - Special exceptions or safety rules (e.g., custom conditions, special domain rules).
- **System & Token Constraints**:
  - Context limits (e.g., max tokens).
  - Execution budgets or pricing structures if applicable.
- **Data Input**:
  - Where to download/find data (e.g. CSV, JSON, API).
  - Note: Use environment variable placeholders for URLs (see Security section below).
- **API Integration**:
  - Endpoints used, request types, payload schemas.

### 3. Security & Environment Setup
- **CRITICAL**: Never hardcode raw API URLs in the `BRD.md`.
- Map all external API endpoints or data source URLs to environment variables (e.g. `$API_VERIFY_URL`, `$SERVICE_DATA_URL`).
- Clearly list these environment variables in the BRD under the "Environment Setup" section so the user knows what to populate in their `.env` file.

### 4. Output
- Save the structured requirements as `BRD.md` in the target directory.
- Respond with a brief confirmation message containing a relative link to the generated [BRD.md](BRD.md).

## Common Mistakes
- **Hardcoding URLs**: Do not copy raw URLs into the markdown. Always use the `$VAR` format.
- **Missing Constraints**: Forgetting to document token limits or cost constraints that are critical to the design phase.
