// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'index', // The initial home page
      label: 'Course Overview'
    },
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        {
          type: 'doc',
          id: 'ros2',
          label: 'ROS 2 Fundamentals'
        }
      ],
      collapsed: false
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        {
          type: 'doc',
          id: 'simulation',
          label: 'Simulation Environments'
        }
      ],
      collapsed: false
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        {
          type: 'doc',
          id: 'isaac',
          label: 'Isaac Platform'
        }
      ],
      collapsed: false
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        {
          type: 'doc',
          id: 'vla',
          label: 'VLA Systems'
        }
      ],
      collapsed: false
    },
    {
      type: 'category',
      label: 'Module 5: Capstone Project',
      items: [
        {
          type: 'doc',
          id: 'capstone',
          label: 'Autonomous Humanoid'
        }
      ],
      collapsed: false
    },
    {
      type: 'doc',
      id: 'assessments',
      label: 'Assessments'
    }
  ],
};

module.exports = sidebars;