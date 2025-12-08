# Physical AI & Humanoid Robotics Textbook Constitution

<!--
SYNC IMPACT REPORT
===================
Version Change: Initial (no previous version) → 1.0.0
Modified Principles: None (initial creation)
Added Sections:
  - Global Mission
  - Role & Persona
  - Core Principles (7 principles)
  - Content Standards
  - Technical Standards
  - Verification Checklist
  - Operational Constraints
  - Governance
Removed Sections: None
Templates Status:
  ✅ .specify/templates/plan-template.md - Reviewed, aligns with constitution check requirements
  ✅ .specify/templates/spec-template.md - Reviewed, aligns with mandatory sections
  ✅ .specify/templates/tasks-template.md - Reviewed, aligns with test-first and verification principles
Follow-up TODOs: None
===================
-->

## Global Mission

We are building a comprehensive, open-source academic textbook on "Physical AI & Humanoid Robotics" using Docusaurus. The output must be a fully functional static website deployed to GitHub Pages, containing rigorous, verified academic content.

## Role & Persona

The development team acts as dual-experts:

1. **Senior Academic Editor:** Rigorous about citations, clarity, and factual accuracy.
2. **Docusaurus Developer:** Expert in Markdown (MDX), React components, and static site architecture.

## Core Principles

### I. Spec-Driven Development (SDD)

**The Golden Rule of SDD:** No code or content is written until a corresponding Specification file (`/specs/xx-name.md`) is created and approved. This principle ensures all work is planned, reviewed, and aligned with requirements before implementation begins.

**Rationale:** Prevents scope creep, ensures stakeholder alignment, and creates a traceable decision history.

### II. Accuracy and Verification

All claims MUST be verified against primary sources. Hallucination is strictly forbidden. Every technical, historical, or scientific assertion must be traceable to an authoritative reference.

**Rationale:** Academic integrity is non-negotiable. Readers must be able to trust and verify all information presented.

### III. Clarity and Accessibility

Writing MUST target Computer Science undergraduates at Flesch-Kincaid Grade 10-12 reading level. Complex concepts must be explained with clear definitions, examples, and progressive disclosure of detail.

**Rationale:** Educational content serves diverse learners. Clarity maximizes understanding and retention.

### IV. Reproducibility and Traceability

All technical claims must be traceable to their sources. Implementations, algorithms, and experimental results must provide sufficient detail for independent verification.

**Rationale:** Scientific rigor requires reproducibility. Readers must be able to verify and build upon presented work.

### V. Citation and Attribution Standards

All references MUST use APA Format. Minimum 15 total unique sources across the project. At least 50% of sources MUST be peer-reviewed articles from reputable venues (IEEE, ACM, Nature, Science, etc.).

**Rationale:** Proper attribution honors original authors, enables verification, and maintains academic standards.

### VI. Zero-Tolerance Plagiarism Policy

All text must be original synthesis of concepts. Direct quotations must be clearly marked and attributed. Paraphrasing without attribution is prohibited.

**Rationale:** Plagiarism undermines academic integrity and violates intellectual property rights.

### VII. Strict Naming and Technical Conventions

All folders and filenames MUST use **kebab-case** (lowercase, hyphen-separated). All chapters go into the `/docs` folder. Configuration files must follow Docusaurus best practices.

**Rationale:** Consistent naming prevents build errors, improves maintainability, and ensures cross-platform compatibility.

## Content Standards

### Chapter Structure Requirements

Each chapter MUST include:

1. **Learning Objectives:** Bullet points at the start of every page clearly stating what readers will learn.
2. **Core Content:** Deep technical explanation of approximately 1,000 words per chapter minimum.
3. **References:** A bibliography section at the bottom of every page with properly formatted citations.

### Source Quality Requirements

- **Minimum Total Sources:** 15 unique sources across the entire project
- **Peer-Reviewed Requirement:** At least 50% must be peer-reviewed articles
- **Acceptable Venues:** IEEE, ACM, Nature, Science, arXiv (for recent preprints), university presses
- **Citation Format:** APA Format for all references

### Writing Quality Standards

- **Reading Level:** Flesch-Kincaid Grade 10-12
- **Tone:** Objective, technical, and educational
- **Clarity:** Define technical terms on first use; use examples to illustrate abstract concepts
- **Completeness:** No "Lorem Ipsum" or placeholder content in production

## Technical Standards

### File and Folder Conventions

- **Naming Convention:** Strict **kebab-case** (lowercase, hyphen-separated)
  - ✅ Correct: `chapter-1-introduction.md`
  - ❌ Incorrect: `Chapter 1 Introduction.md`
- **Location:** All chapters in `/docs` folder
- **Configuration:** `docusaurus.config.js` must specify correct `organizationName` and `projectName` for GitHub Pages

### Markdown and Documentation Standards

- **Format:** Standard Markdown with MDX support for React components
- **Headers:** Do not use H1 (#) inside document body (Docusaurus handles titles automatically)
- **Diagrams:** Use Mermaid.js code blocks for flowcharts and architecture diagrams
- **Code Blocks:** Use syntax highlighting with proper language tags

### Build and Deployment Requirements

- **Build Command:** `npm run build` must complete without errors
- **Deployment Target:** GitHub Pages
- **Testing:** Local preview with `npm start` must render correctly before deployment

## Verification Checklist (Definition of Done)

Before marking any spec, task, or chapter as complete, verify ALL of the following:

1. [ ] **Build Success:** Does the project build (`npm run build`) without errors?
2. [ ] **Naming Compliance:** Are all filenames strictly lowercase/kebab-case?
3. [ ] **Citations Present:** Are there valid sources cited for the specific chapter?
4. [ ] **Content Quality:** Is the content free of "Lorem Ipsum" or placeholders?
5. [ ] **Learning Objectives:** Does the chapter start with clear learning objectives?
6. [ ] **Word Count:** Does the chapter meet the minimum 1,000 word requirement?
7. [ ] **References Section:** Is there a properly formatted bibliography at the end?
8. [ ] **Reading Level:** Is the writing appropriate for the target audience (Grade 10-12)?
9. [ ] **Technical Accuracy:** Have all technical claims been verified against primary sources?
10. [ ] **Preview Check:** Does the page render correctly in local preview (`npm start`)?

## Operational Constraints

### Scope and Scale

- **Total Word Count:** 5,000 - 7,000 words across all chapters
- **Minimum Sources:** 15 unique references total
- **Peer-Review Ratio:** At least 50% peer-reviewed sources
- **Chapter Length:** Approximately 1,000 words per chapter minimum

### Development Workflow

All work MUST follow this sequence:

1. **Write Spec:** Create detailed specification in `/specs/xx-name.md`
2. **Create Structure:** Set up folders, files, and navigation in kebab-case
3. **Write Content:** Draft content with proper citations and learning objectives
4. **Verify Build:** Run `npm run build` and fix any errors
5. **Review Quality:** Complete verification checklist
6. **Deploy:** Push to GitHub Pages when ready

### Quality Gates

- **Pre-Implementation:** Specification must be approved before any content creation
- **Pre-Deployment:** All items in verification checklist must pass
- **Post-Deployment:** Verify live site renders correctly and all links work

## Governance

### Constitution Authority

This constitution supersedes all other practices and guides. When conflicts arise between this document and other guidance, this constitution takes precedence.

### Amendment Process

Amendments to this constitution require:

1. **Documentation:** Proposed changes documented with rationale
2. **Review:** Review by project stakeholders
3. **Migration Plan:** Clear plan for updating existing content to comply with changes
4. **Version Update:** Semantic versioning applied to constitution version number

### Compliance Verification

- All pull requests must verify compliance with this constitution
- All specifications must reference relevant constitutional principles
- Any deviation from constitutional principles must be explicitly justified and documented

### Complexity Justification

Complexity must be justified. Before adding new tools, frameworks, dependencies, or patterns, demonstrate:

1. Why existing approaches are insufficient
2. What specific problem the addition solves
3. What simpler alternatives were considered and rejected

### Version History

**Version**: 1.0.0 | **Ratified**: 2025-12-07 | **Last Amended**: 2025-12-07
