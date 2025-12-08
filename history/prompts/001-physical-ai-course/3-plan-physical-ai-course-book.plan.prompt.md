---
id: 3
title: "Plan Physical AI Course Book"
stage: plan
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-physical-ai-course
branch: 001-physical-ai-course
user: user
command: /sp.plan
labels:
  - planning
  - docusaurus
  - robotics
  - education
  - static-site
links:
  spec: specs/001-physical-ai-course/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-physical-ai-course/plan.md
  - specs/001-physical-ai-course/research.md
  - specs/001-physical-ai-course/data-model.md
  - specs/001-physical-ai-course/quickstart.md
  - specs/001-physical-ai-course/contracts/build-api.yaml
tests: []
outcome: "Implementation plan created with research, data model, quickstart guide, and contracts"
evaluation: "Successfully created comprehensive implementation plan for the Physical AI & Humanoid Robotics course book, including all required artifacts and meeting constitutional requirements."
---

## Prompt

Project: Physical AI & Humanoid Robotics — Docusaurus Course Book

Objective:
Create a technical plan (MVP) for building the course book based on the business/spec requirements, deployable to GitHub Pages, using Docusaurus, ROS 2 examples, NVIDIA Isaac snippets, and Spec-Kit Plus specification.

Include:

1. **Architecture Sketch**
   - High-level repo structure (docs/, examples/, specs/, CI/CD)
   - Docusaurus setup (config, sidebars, theme)
   - GitHub Actions workflow for automatic deploy
   - Example code placement and simulation snippets

2. **Section Structure**
   - Chapters mapped to modules and weekly breakdown
   - Index, Introduction, Module pages (ROS2, Simulation, Isaac, VLA), Capstone, Assessments
   - Subpages for labs, exercises, and code examples
   - References / citations section

3. **Research Approach**
   - Research-concurrent: gather references and evidence while writing chapters
   - Follow APA citation style placeholders [cite:authorYear]
   - Include technical notes for ROS 2, Gazebo, Isaac Sim, GPT integration
   - Document best practices for humanoid simulation and embodied intelligence

4. **Quality Validation**
   - Acceptance criteria from spec (build, serve, deploy, module pages exist, example code runs)
   - Check for Docusaurus site compilation without errors
   - Validate GitHub Pages deployment workflow
   - Ensure content completeness and APA citation consistency

5. **Decisions Needing Documentation**
   - GitHub Pages URL: option A (specific) vs B (repo-default) vs C (placeholder)
   - ROS 2 code snippet locations and size (small runnable only)
   - Isaac simulation assets (lightweight examples, no full binaries)
   - LLM integration approach for VLA (GPT models, Whisper, planning)
   - Sidebars structure: flat vs nested vs collapsible

6. **Testing Strategy**
   - Build & serve Docusaurus locally (npm run build, npx docusaurus serve)
   - Check all module pages exist and render correctly
   - Validate example ROS 2 and Isaac snippets run without error
   - Test GitHub Actions deployment workflow to gh-pages
   - Link check for all Markdown cross-references

Technical Details / Recommendations:
- Use research-concurrent approach: research while writing chapters
- Organize by phases: Research → Foundation → Analysis → Synthesis
- MVP-first: focus on basic docs + sample code + deployable site first
- Use npx for Docusaurus commands; installation via Node.js / npm assumed
- Include minimal configuration to make site build quickly
- Additional features (search, multi-modal interactions) can be added later

Output:
- High-level architecture diagram (ASCII or descriptive)
- Section/chapter plan with filenames
- Decisions + tradeoffs table
- Testing checklist
- Phased plan: MVP → enhanced → full-featured

## Response

Successfully completed the implementation plan for the Physical AI & Humanoid Robotics course book with all required artifacts:

1. **Plan** (plan.md): Comprehensive implementation plan with technical context, constitution check, and project structure
2. **Research** (research.md): Research summary covering technology stack, deployment, code examples, and content organization
3. **Data Model** (data-model.md): Entity definitions for course modules, code examples, navigation structure, and user roles
4. **Quickstart Guide** (quickstart.md): Setup instructions, project structure, and deployment guidance
5. **Contracts** (contracts/build-api.yaml): API contract for the build and validation process
6. **Agent Context Update**: Updated CLAUDE.md with new technology stack information

The plan addresses all requirements including:
- Docusaurus-based course book with proper repo structure
- GitHub Pages deployment workflow
- ROS 2 and NVIDIA Isaac code examples in /examples/ directory
- Proper navigation structure and content organization
- Performance targets and constitutional compliance

The implementation follows the research-concurrent approach and is structured for MVP-first development.