# Physical AI & Humanoid Robotics Course Book

A comprehensive Docusaurus-based course book covering Physical AI and Humanoid Robotics modules, deployable to GitHub Pages.

## Overview

This course book provides comprehensive coverage of Physical AI and Humanoid Robotics topics through 7 modules:

1. **Introduction** - Course overview and foundational concepts
2. **The Robotic Nervous System (ROS 2)** - Understanding robot operating systems
3. **The Digital Twin (Gazebo & Unity)** - Simulation and modeling environments
4. **The AI-Robot Brain (NVIDIA Isaac™)** - Perception and decision making
5. **Vision-Language-Action (VLA)** - Multimodal AI systems
6. **Capstone Project** - Autonomous Humanoid implementation
7. **Assessments** - Evaluation and testing materials

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn package manager

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

The site will be available at http://localhost:3000

## Building for Production

To build the static site:

```bash
npm run build
```

The built site will be in the `build/` directory.

## Deployment

The site is configured for GitHub Pages deployment. The deployment settings are in `docusaurus.config.js`.

## Project Structure

```
physical-ai-humanoid-robotics-course/
├── docs/                    # Course content (Markdown files)
│   ├── index.md            # Introduction / Course Overview
│   ├── 03-ros2.md          # Module 1: The Robotic Nervous System (ROS 2)
│   ├── 04-simulation.md    # Module 2: The Digital Twin (Gazebo & Unity)
│   ├── 05-isaac.md         # Module 3: The AI-Robot Brain (NVIDIA Isaac™)
│   ├── 06-vla.md           # Module 4: Vision-Language-Action (VLA)
│   ├── 07-capstone.md      # Capstone Project: The Autonomous Humanoid
│   └── assessments.md      # Assessments
├── examples/               # ROS 2 and Isaac code examples
├── src/                    # Custom React components (if needed)
├── static/                 # Static assets (images, etc.)
├── .github/workflows/      # GitHub Actions for deployment
├── docusaurus.config.js    # Docusaurus configuration
├── sidebars.js             # Navigation structure
├── package.json           # Project dependencies and scripts
└── README.md              # Project overview
```

## Contributing

To add new content:

1. Create a new Markdown file in the `docs/` directory
2. Add the new page to the navigation by editing `sidebars.js`
3. Build and test the site with `npm run build` and `npm run serve`

## License

This project is licensed under the MIT License.