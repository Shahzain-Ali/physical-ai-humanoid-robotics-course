---
id: 0001
title: Initial Project Constitution
stage: constitution
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: system
command: /sp.constitution
labels: ["constitution", "governance", "setup", "initial-configuration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

```text
# Project Constitution: Physical AI & Humanoid Robotics Textbook

## 1. Global Mission
We are building a comprehensive, open-source academic textbook on "Physical AI & Humanoid Robotics" using Docusaurus. The output must be a fully functional static website deployed to GitHub Pages, containing rigorous, verified academic content.

## 2. Role & Persona
You act as a dual-expert:
1.  **Senior Academic Editor:** Rigorous about citations, clarity, and factual accuracy.
2.  **Docusaurus Developer:** Expert in Markdown (MDX), React components, and static site architecture.

## 3. Core Principles (Non-Negotiable)
1.  **The Golden Rule of SDD:** No code or content is written until a corresponding Specification file (`/specs/xx-name.md`) is created and approved.
2.  **Accuracy:** All claims must be verified against primary sources. Hallucination is strictly forbidden.
3.  **Clarity:** Writing must target Computer Science undergraduates (Flesch-Kincaid Grade 10-12).
4.  **Reproducibility:** All technical claims must be traceable.

## 4. Content Standards (The "Academic" Spec)
*   **Citation Style:** APA Format for all references.
*   **Source Quality:** Minimum 15 total unique sources across the project; at least 50% must be peer-reviewed articles (IEEE, ACM, Nature, Science).
*   **Plagiarism:** 0% tolerance. All text must be original synthesis of concepts.
*   **Structure per Chapter:**
    *   **Learning Objectives:** Bullet points at the start of every page.
    *   **Core Content:** Deep technical explanation (approx 1,000 words per chapter).
    *   **References:** A bibliography section at the bottom of every page.

## 5. Technical Standards (The "Docusaurus" Spec)
*   **Strict Naming Convention:** All folders and filenames must use **kebab-case** (lowercase, hyphen-separated).
    *   *Correct:* `chapter-1-introduction.md`
    *   *Incorrect:* `Chapter 1 Introduction.md`
*   **Location:** All chapters go into the `/docs` folder.
*   **Configuration:** `docusaurus.config.js` must be configured with correct `organizationName` and `projectName` for GitHub Pages deployment.
*   **Diagrams:** Use Mermaid.js code blocks for flowcharts and architecture diagrams within the MDX files.
*   **Formatting:** Use standard Markdown headers (#, ##, ###). Do not use H1 (#) inside the document body (Docusaurus handles title automatically).

## 6. Verification Checklist (Definition of Done)
Before marking any spec or task as complete, you must verify:
1.  [ ] Does the project build (`npm run build`) without errors?
2.  [ ] Are all filenames strictly lowercase/kebab-case?
3.  [ ] Are there valid sources cited for the specific chapter?
4.  [ ] Is the content free of "Lorem Ipsum" or placeholders?

## 7. Operational Constraints
*   **Total Word Count:** 5,000 - 7,000 words.
*   **Tone:** Objective, technical, and educational.
*   **Workflow:**
    1. Write Spec → 2. Create Structure → 3. Write Content → 4. Verify Build.
```

## Response snapshot

Constitution successfully created at `.specify/memory/constitution.md` with version 1.0.0. The document establishes:

**7 Core Principles:**
1. Spec-Driven Development (SDD) - Golden Rule
2. Accuracy and Verification
3. Clarity and Accessibility
4. Reproducibility and Traceability
5. Citation and Attribution Standards
6. Zero-Tolerance Plagiarism Policy
7. Strict Naming and Technical Conventions

**Key Standards:**
- Content: Learning objectives, 1,000+ words/chapter, APA citations, 15+ sources (50% peer-reviewed)
- Technical: kebab-case naming, `/docs` location, Docusaurus configuration
- Verification: 10-point checklist for Definition of Done
- Workflow: Spec → Structure → Content → Verify → Deploy

**Templates Validated:**
- plan-template.md: Aligns with constitution check requirements
- spec-template.md: Aligns with mandatory sections
- tasks-template.md: Aligns with test-first and verification principles

Version 1.0.0 ratified on 2025-12-07. All placeholders filled. No deferred items.

## Outcome

- ✅ Impact: Constitution established for Physical AI & Humanoid Robotics Textbook project. All governance rules, content standards, technical conventions, and verification requirements now documented and enforceable.
- 🧪 Tests: N/A (governance document, no code tests required)
- 📁 Files: Created `.specify/memory/constitution.md` (201 lines)
- 🔁 Next prompts: Ready for feature specification creation (`/sp.specify`), project structure setup, or Docusaurus initialization
- 🧠 Reflection: Constitution provides clear, measurable standards for academic content quality (citations, word count, reading level) and technical rigor (kebab-case, build verification). The 10-point verification checklist ensures consistent quality gates.

## Evaluation notes (flywheel)

- Failure modes observed: None. Template successfully filled with all placeholders resolved.
- Graders run and results (PASS/FAIL): PASS - All validation checks passed (no unresolved placeholders, version coherent, dates in ISO format, principles declarative)
- Prompt variant (if applicable): Initial baseline constitution (no variants)
- Next experiment (smallest change to try): When first feature spec is created, verify constitution principles are correctly referenced in spec template's "Constitution Check" section
