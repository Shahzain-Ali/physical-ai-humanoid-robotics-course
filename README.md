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

### Weekly Breakdown

The course is structured across 13 weeks, with detailed weekly content covering:
- **Weeks 1-2**: Introduction to Physical AI (sensors, perception, embodied intelligence)
- **Weeks 3-5**: ROS 2 Fundamentals (architecture, nodes, topics, services)
- **Weeks 6-7**: Robot Simulation (Gazebo, Unity, digital twins)
- **Weeks 8-10**: NVIDIA Isaac Platform (perception, manipulation, sim-to-real)
- **Weeks 11-12**: Humanoid Robot Development (kinematics, bipedal locomotion)
- **Week 13**: Conversational Robotics (GPT integration, multi-modal interaction)

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
│   ├── index.md            # Introduction / Course Overview (includes weekly breakdown)
│   ├── ros2.md             # Module 1: The Robotic Nervous System (ROS 2)
│   ├── simulation.md       # Module 2: The Digital Twin (Gazebo & Unity)
│   ├── isaac.md            # Module 3: The AI-Robot Brain (NVIDIA Isaac™)
│   ├── vla.md              # Module 4: Vision-Language-Action (VLA)
│   ├── capstone.md         # Capstone Project: The Autonomous Humanoid
│   └── assessments.md      # Assessments
├── examples/               # ROS 2 and Isaac code examples
│   ├── ros2-examples/      # ROS 2 publisher/subscriber examples
│   ├── isaac-examples/     # NVIDIA Isaac perception examples
│   └── simulation-examples/ # Robot controller examples
├── src/                    # Custom React components and CSS
│   └── css/custom.css      # Custom styling
├── static/                 # Static assets (images, etc.)
├── .github/workflows/      # GitHub Actions for deployment
│   └── deploy.yml          # Automated GitHub Pages deployment
├── docusaurus.config.js    # Docusaurus configuration
├── sidebars.js             # Navigation structure
├── package.json            # Project dependencies and scripts
└── README.md               # Project overview
```

## Contributing

To add new content:

1. Create a new Markdown file in the `docs/` directory
2. Add the new page to the navigation by editing `sidebars.js`
3. Build and test the site with `npm run build` and `npm run serve`

## License

This project is licensed under the MIT License.