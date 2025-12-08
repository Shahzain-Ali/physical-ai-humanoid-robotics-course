---
id: 1
title: "Create Physical AI Course Book Spec"
stage: spec
date: 2025-12-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-physical-ai-course
branch: 001-physical-ai-course
user: user
command: /sp.specify
labels:
  - specification
  - docusaurus
  - robotics
  - education
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-physical-ai-course/spec.md
  - specs/001-physical-ai-course/checklists/requirements.md
tests: []
outcome: "Specification created successfully with all required sections completed"
evaluation: "The specification includes all required sections: User Scenarios & Testing, Functional Requirements, Key Entities, and Success Criteria. Quality checklist was created and validated."
---

## Prompt

Title: Physical AI & Humanoid Robotics — Course Book
Target audience: Hackathon participants, instructors
Focus: Create a Docusaurus-based book covering Physical AI & Humanoid Robotics modules, deployable to GitHub Pages.

Instructions:
1. First, define the complete repo layout and folder/file structure, including all modules and weekly chapters.
2. Then, generate a Spec-Kit Plus compatible spec.
3. Produce first-draft Markdown for all chapters and capstone.
4. Include example ROS 2 and NVIDIA Isaac code snippets.
5. Provide GitHub Actions workflow to deploy site to GitHub Pages.

Modules & Chapters Mapping:
- Module 1: The Robotic Nervous System (ROS 2) → 03-ros2.md
- Module 2: The Digital Twin (Gazebo & Unity) → 04-simulation.md
- Module 3: The AI-Robot Brain (NVIDIA Isaac™) → 05-isaac.md
- Module 4: Vision-Language-Action (VLA) → 06-vla.md
- Capstone Project: The Autonomous Humanoid → 07-capstone.md
- Introduction / Course Overview → index.md
- Assessments → assessments.md

Weekly Breakdown (for chapter details / subpages):
- Weeks 1-2: Introduction to Physical AI (include sensors, embodied intelligence)
- Weeks 3-5: ROS 2 Fundamentals (nodes, topics, services, rclpy)
- Weeks 6-7: Robot Simulation with Gazebo & Unity
- Weeks 8-10: NVIDIA Isaac Platform (perception, manipulation, sim-to-real)
- Weeks 11-12: Humanoid Robot Development (kinematics, bipedal locomotion, manipulation)
- Week 13: Conversational Robotics (GPT integration, multi-modal interaction)

Success criteria:
- Repo layout clearly defined and matches hackathon deliverables.
- Each module/week has a corresponding book page.
- Spec document complete and usable by Spec-Kit Plus.
- Docusaurus skeleton with docs/, docusaurus.config.js, sidebars.js, package.json.
- Example code snippets exist in /examples/.
- Acceptance checklist for build, serve, deploy.

Constraints:
- Markdown format compatible with Docusaurus and Spec-Kit Plus.
- Word count per module: 800–2000 words.
- Only small runnable code snippets; no large binaries.
- Citation placeholders [cite:authorYear] optional.

Not building:
- Vendor comparisons, live demos, ethics discussions.

Deliverables:
- Complete repo layout.
- Spec-Kit Plus spec Markdown.
- First-draft docs/ pages for all modules and capstone.
- Example code snippets in /examples/.
- Docusaurus config, sidebars, package.json, README.
- GitHub Actions workflow for deployment.
- Acceptance checklist and milestones.

## Response

Created feature branch `001-physical-ai-course` and generated a comprehensive specification for the Physical AI & Humanoid Robotics Course Book. The specification includes:

- User Scenarios & Testing with 3 prioritized user stories
- Functional Requirements with 10 specific requirements
- Key Entities describing the course structure
- Success Criteria with 7 measurable outcomes

The spec addresses all specified modules (Introduction, ROS 2, Simulation, Isaac, VLA, Capstone, Assessments) and weekly breakdowns (Weeks 1-2, 3-5, 6-7, 8-10, 11-12, Week 13). A quality checklist was also created and validated to ensure the spec is ready for the next phase.