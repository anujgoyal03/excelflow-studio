"""
modes.py
--------
Configuration for the four workspaces shown in the sidebar.

To add a new workspace later, add an entry here and a matching branch
in engine.select_sheets(). The Streamlit UI can then use this
configuration dynamically.

Each entry:
    icon        -> sidebar navigation icon
    title       -> main page heading
    description -> subtitle shown under the heading
    mode        -> string passed to engine.select_sheets()
                   and process_workbook()
"""

MODES = {
    "L0-L3": {
        "icon": "\u25A6",
        "title": "L0\u2013L3 Excel Processor",
        "description": (
            "Process every source sheet except 'Instructions' "
            "and update the original template."
        ),
        "mode": "all",
    },

    "L4 FLOW DIAGRAMS": {
        "icon": "\u25C8",
        "title": "L4 Flow Diagram Processor",
        "description": (
            "Process only sheets beginning with 'Alphabets and numbers' "
            "also synchronize them with the template."
        ),
        "mode": "pp",
    },

    "L4 TASK ATTRIBUTES": {
        "icon": "\u25C7",
        "title": "L4 Task Attributes Processor",
        "description": (
            "Process every source sheet except 'Instructions' "
            "and 'Data Validation' and update the original template."
        ),
        "mode": "task_attributes",
    },

    "USER STORIES": {
        "icon": "\u25C6",
        "title": "User Stories Processor",
        "description": (
            "Extract only the 'User Stories' sheet "
            "and update the original template."
        ),
        "mode": "user_stories",
    },
}


# Default workspace shown when the application starts
DEFAULT_MODE = "L0-L3"