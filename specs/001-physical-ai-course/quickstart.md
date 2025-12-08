# Quickstart Guide: Physical AI & Humanoid Robotics Course Book

## Prerequisites
- Node.js (v18 or higher)
- npm or yarn package manager
- Git

## Setup Instructions

### 1. Clone and Initialize
```bash
git clone [repository-url]
cd physical-ai-humanoid-robotics-course
npm install
```

### 2. Local Development
```bash
# Start local development server
npm start

# The site will be available at http://localhost:3000
```

### 3. Build for Production
```bash
# Build the static site
npm run build

# The built site will be in the build/ directory
```

### 4. Serve Built Site Locally
```bash
# Serve the built site locally for testing
npm run serve
```

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
├── docusaurus.config.js    # Docusaurus configuration
├── sidebars.js             # Navigation structure
├── package.json           # Project dependencies and scripts
└── README.md              # Project overview
```

## Adding New Content

### 1. Create a new module page
```bash
# Add a new Markdown file in the docs/ directory
# Example: docs/new-module.md
```

### 2. Update navigation
Edit `sidebars.js` to add the new page to the navigation structure.

### 3. Build and test
```bash
npm run build
npm run serve
```

## Deployment
The site is automatically deployed to GitHub Pages when changes are pushed to the main branch via GitHub Actions workflow.