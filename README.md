# ServiceNow Task Handler

Automate the fulfillment of ServiceNow tasks
---

### Process Diagram

Below is the process flow for the **ServiceNow Task Handler**, showing how tasks are retrieved, processed, and completed:

```mermaid
graph TD
    A[Start Task Handler] --> B[Check for Open Tasks]
    B -->|Tasks Found| C[Retrieve Task Variables]
    B -->|No Tasks| F[Wait 10 Seconds]
    C --> D[Set Task to 'Work in Progress']
    D --> E[Execute Fulfillment Logic]
    E --> G[Close Task]
    G --> F
    F --> B
```
---

### **Explanation of the Workflow**
1. **Start Task Handler**:
   - The script begins execution and enters a continuous loop to monitor for new tasks.
2. **Check for Open Tasks**:
   - The script queries the ServiceNow API for tasks assigned to the configured assignment group with a status of "Open."
   - If no tasks are found, it waits for 10 seconds before rechecking.
3. **Retrieve Task Variables**:
   - If tasks are found, their associated variables are retrieved.
4. **Set Task to 'Work in Progress'**:
   - The task’s status is updated to "Work in Progress" to prevent duplicate handling.
5. **Execute Fulfillment Logic**:
   - Custom logic is applied to fulfill the task based on its variables.
6. **Close Task**:
   - The task’s status is updated to "Closed" after fulfillment.
   - After closing, the script waits for 10 seconds before checking for new tasks.
7. **Repeat**:
   - The handler loops back to check for more open tasks.

---

## Getting Started

### Prerequisites

- A ServiceNow instance with API access enabled
- API credentials for a user with appropriate permissions

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/streamflowtech/ServiceNow-Task-Handler.git
   ```
2. Navigate into the cloned repo:
   ```bash
   cd ServiceNow-Task-Handler
   ```
3. Optional: Create & activate virtual environment:
   ```bash
   python3 -m venv ~/venvs/snow_task_handler
   source ~/venvs/snow_task_handler/bin/activate
   ```
4. Install required packages
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. Create a .env file and populate the following variables:
   ```bash
   INSTANCE=""
   USERNAME=""
   PASSWORD=""
   ASSIGNMENT_GROUP=""
   ```

### Running the Task Handler

To start the task handler, run:
   ```bash
   python3 snow_task_handler.py -v
   ```
Note: The -v will log to the console.  Remove this flag to run in silent mode

When the script is run with -v option, if no tasks are found for fulfillment, the output will look like this:

```plaintext
2025-01-06 14:31:14.204010 - Starting ServiceNow task handler
2025-01-06 14:31:14.204050 - Getting all open tasks assigned to automation group
2025-01-06 14:31:14.442560 - No tasks to fulfill
2025-01-06 14:31:14.442596 - Sleeping for 10 seconds
```

If there are tasks to be fulfilled, the output will look like this:

```plaintext
2025-01-06 14:51:01.021640 - Starting ServiceNow task handler
2025-01-06 14:51:01.021676 - Getting all open tasks assigned to automation group
2025-01-06 14:51:01.311920 - 1 task retrieved for fulfillment
2025-01-06 14:51:01.311963 - Working on task SCTASK0010007
2025-01-06 14:51:01.311970 - Getting item variables for task SCTASK0010007
2025-01-06 14:51:01.556648 - Setting task SCTASK0010007 to "Work in Progress"
2025-01-06 14:51:01.877094 - Fulfilling task SCTASK0010007
2025-01-06 14:51:02.206688 - Closing task SCTASK0010007
2025-01-06 14:51:02.534721 - Task fulfilled successfully
```

---

## Customization

To tailor the **ServiceNow Task Handler** to your specific needs, you can add your own logic to fulfill tasks by modifying the `fulfill_task` function. This function is a placeholder for task-specific actions and can be extended or updated to handle various use cases.
