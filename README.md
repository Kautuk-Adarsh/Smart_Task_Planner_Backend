# Smart Task Planner API

## Project Overview

The Smart Task Planner API is a full-stack backend service designed to transform unstructured, high-level goals into detailed, actionable task plans. It leverages the power of the Google Gemini Large Language Model (LLM) to intelligently break down complex objectives and utilizes MongoDB for persistent storage of the generated plans.

The API is built using FastAPI for high performance and asynchronous request handling, providing a structured endpoint for task planning.

## Key Features

* **Intelligent Task Breakdown:** Uses the Gemini 2.5 Flash model for generating comprehensive task lists, including suggested deadlines, dependencies, and priority levels.
* **Structured Output:** Enforces strict output compliance by utilizing Pydantic models with the Gemini API to ensure the task plan is returned as clean, predictable JSON.
* **Database Persistence:** Plans are saved asynchronously to a MongoDB Atlas cluster, allowing for historical retrieval and management of user goals.
* **Scalable Architecture:** Built on FastAPI with asynchronous database drivers (`motor`) and the asynchronous Gemini client (`aio`), designed for concurrency and high traffic.

## Technical Stack

* **Framework:** FastAPI
* **Language:** Python 3.10+
* **AI/LLM:** Google Gemini API (`google-genai` client)
* **Database:** MongoDB Atlas
* **Database Driver:** Motor (Asynchronous Python driver for MongoDB)
* **Data Validation:** Pydantic V2
* **Configuration:** `dotenv` for environment variables

## Prerequisites

Before running the application, ensure you have the following:

1. **Python 3.10+** installed.
2. A **Google AI Studio API Key** (for Gemini).
3. A **MongoDB Atlas Cluster** (or local instance) and the corresponding **Connection URI** and **Database Name**.

## Project Structure

The project follows a modular structure for maintainability:

```
.
├── api/
│   └── planner.py           # The main API router/endpoint (LLM call and DB save logic)
├── db/
│   ├── database.py          # MongoDB connection and shutdown logic (using Motor)
│   └── model.py             # Pydantic model for database persistence (PlanDB)
├── config.py                # Handles environment variables, logging, and Gemini client initialization
├── main.py                  # FastAPI application entry point and lifespan management
├── schemas.py               # Pydantic models for API request/response (GoalRequest, TaskPlan)
└── README.md
```

## Setup and Installation

### 1. Environment Variables

Create a file named `.env` in the root directory and populate it with your credentials:

```bash
# .env

# Google Gemini API Key
PROJECT_API_KEY="YOUR_GEMINI_API_KEY_HERE"

# MongoDB Credentials
MONGO_URI="mongodb+srv://<user>:<password>@<cluster-url>/?"
MONGO_DB_NAME="smart_planner_db"
```

### 2. Install Dependencies

You will need a virtual environment.

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# .\venv\Scripts\activate # On Windows

# Install required packages
pip install -r requirements.txt
# Or install manually:
pip install fastapi uvicorn google-genai pydantic motor python-dotenv
```

### 3. Run the Application

The application is started via the `main.py` entry point using Uvicorn with auto-reload:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Usage

### Endpoint: Create Task Plan

This is the primary endpoint to generate a plan from a user goal.

* **URL:** `/api/v1/plans`
* **Method:** `POST`

#### Request Body (JSON - GoalRequest)

| Field | Type | Description |
|-------|------|-------------|
| `goal_text` | string | The high-level goal to be planned (e.g., "Write a book"). |
| `user_id` | string (Optional) | The ID of the user submitting the goal. |
| `context` | string (Optional) | Additional context for the LLM (e.g., "Budget is low"). |

#### Success Response (201 Created - TaskPlan)

A structured JSON object containing a high-level summary and a list of detailed tasks, which strictly adheres to the Pydantic `TaskPlan` schema.

#### Example Call (using curl)

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/plans" \
-H "Content-Type: application/json" \
-d '{
  "goal_text": "Develop and launch a new feature on the mobile app within 30 days.",
  "user_id": "user-456",
  "context": "Focus on quick implementation for MVP rollout."
}'
```

## Documentation

Once the server is running, you can access the interactive API documentation (Swagger UI) at:

**http://127.0.0.1:8000/docs**

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions, please open an issue on the project repository.