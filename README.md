# ServiceNow Task Handler

The **ServiceNow Task Handler** is a Python script designed to automate the lifecycle of ServiceNow tasks. It continuously polls for new tasks, updates their status, processes them, and closes them out.
---

## Getting Started

### Prerequisites

- A ServiceNow instance with API access enabled
- API credentials for a user with appropriate permissions

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/streamflowtech/ServiceNow-Task-Handler.git
2. Optional: Create & activate virtual environment:
   ```bash
   python3 -m venv ~/venvs/snow_task_handler
   source ~/venvs/snow_task_handler/bin/activate
3. Install required packages
   ```bash
   pip install -r requirements.txt

### Configuration

1. Create a .env file and populate the following variables:
   ```bash
   INSTANCE=""
   USERNAME=""
   PASSWORD=""
   ASSIGNMENT_GROUP=""

### Running the Task Handler

To start the task handler, run:
   ```bash
   python3 snow_task_handler.py -v
   ```
Note: The -v will log to the console.  Remove this flag to run in silent mode

### Customization

To tailor the **ServiceNow Task Handler** to your specific needs, you can add your own logic to fulfill tasks by modifying the `fulfill_task` function. This function is a placeholder for task-specific actions and can be extended or updated to handle various use cases.
