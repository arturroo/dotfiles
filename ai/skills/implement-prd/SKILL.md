---
name: implement-prd
description: >-
  Executes the codebase implementation based on the final specifications in PRD.md. Skipping automatic commits.
---

# Implement PRD

## Overview
This skill reads the Product Requirements Document (`PRD.md`) and translates the "Implementation Spec" directly into working code (scripts, schemas, packages, and configurations).

## Requirements
- **Prerequisite**: `PRD.md` must exist in the target task directory.

## Workflow
1. **Read Specification**: Read `PRD.md` carefully, focusing on the "Implementation Spec" at the bottom (File Structure, Tech Stack, Coding Standards, and Implementation Order).
2. **Setup Dependencies**: Use `uv` for python environments, specify precise dependency versions (sorted alphabetically, no caret `^` operator).
3. **Core Coding Standards**:
   - Use `pathlib.Path` for all paths.
   - Enforce contract-first schema design using Pydantic (all fields must have `Field(description=...)` and a `reasoning` field).
   - Never hardcode external API URLs or secrets (use `.env` variables).
4. **Implementation Step-by-Step**:
   - Follow the exact "Step-by-Step Implementation Order" specified in the PRD.
   - Run verification scripts or local runs at each step to ensure correctness.
5. **Git Policy**:
   - **DO NOT perform automatic git commits or pushes**.
   - Leave the code unstaged for the user to review, test, and commit manually.

## Output
- Present the list of modified/new files to the user.
- Explain how to run the verification tests manually.
