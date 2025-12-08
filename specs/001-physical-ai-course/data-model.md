# Data Model: Physical AI & Humanoid Robotics Course Book

## Course Module Entity
- **Fields**:
  - id: string (kebab-case identifier)
  - title: string (module title)
  - content: string (Markdown content)
  - wordCount: number (between 800-2000)
  - moduleNumber: number (sequence identifier)
  - topics: array<string> (specific topics covered)
  - codeExamples: array<string> (references to example files)
  - weeklyBreakdown: string (associated weeks, e.g. "Weeks 1-2")
  - prerequisites: array<string> (prerequisite modules)

- **Validation Rules**:
  - wordCount must be between 800 and 2000
  - title must not be empty
  - content must be valid Markdown
  - moduleNumber must be unique

## Code Example Entity
- **Fields**:
  - id: string (unique identifier)
  - language: string (e.g., "python", "cpp", "bash")
  - framework: string (e.g., "ROS2", "Isaac", "Gazebo")
  - code: string (the actual code snippet)
  - description: string (brief explanation of the example)
  - associatedModule: string (which module this example belongs to)
  - runnable: boolean (whether the code can be executed as-is)

- **Validation Rules**:
  - code must be syntactically correct for the specified language
  - associatedModule must reference an existing module
  - code length must be appropriate for a snippet (not a full application)

## Navigation Structure Entity
- **Fields**:
  - id: string (unique identifier)
  - label: string (display name in navigation)
  - type: string (doc, link, category)
  - docId: string (reference to a document if type is doc)
  - href: string (external link if type is link)
  - items: array<NavigationStructure> (child items if type is category)
  - collapsible: boolean (whether the category can be collapsed)

- **Validation Rules**:
  - If type is 'doc', docId must reference an existing document
  - If type is 'link', href must be a valid URL
  - Labels must be unique within the same level

## User Role Entity
- **Fields**:
  - id: string (role identifier)
  - name: string (e.g., "participant", "instructor")
  - permissions: array<string> (list of allowed actions)
  - accessLevel: number (hierarchical access level)

- **Validation Rules**:
  - Role name must be unique
  - Permissions must be predefined values
  - Access level must be appropriate for the role type