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
2. Create & activate virtual environment:
   ```bash
   python3 -m venv ~/venvs/snow_task_handler
   source ~/venvs/snow_task_handler/bin/activate
3. Install required packages
   ```bash
   pip install -r requirements.txt
