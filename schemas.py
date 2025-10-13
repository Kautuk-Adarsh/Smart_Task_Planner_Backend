from pydantic import BaseModel, Field


class GoalRequest(BaseModel):
    """Defines the structure for the API request body."""

    goal_text: str = Field(
        ...,
        min_length=10,
        max_length=500,
        example="Launch a successful marketing campaign for the new app by next month",
    )
    user_id: str | None = Field(
        None,
        example="user-abbc12323",
        description="Optional ID of the user submitting the goal.",
    )
    context: str | None = Field(
        None,
        max_length=1000,
        description="Optional additional context for the LLM (e.g., budget, resource constraints).",
    )


class Task(BaseModel):
    """A single, actionable task for the overall plan."""

    task_id: str = Field(
        ..., description="A unique short ID for this task (e.g., 'T01', 'T02')."
    )
    description: str = Field(
        ..., description="A clear, actionable description of the task."
    )
    estimated_duration_days: int = Field(
        ...,
        description="Estimated time in full days to complete the task (e.g., 1, 3, 7).",
    )
    dependencies: list[str] = Field(
        ...,
        description="A list of task_ids (e.g., ['T01', 'T03']) that must be completed before this task can start. Use an empty list if none.",
    )
    priority: str = Field(
        ..., description="The priority level of the task: 'High', 'Medium', or 'Low'."
    )
    suggested_deadline: str = Field(
        ...,
        description="The suggested completion date in YYYY-MM-DD format (e.g., 2025-10-20).",
    )


class TaskPlan(BaseModel):
    """The final, complete structured task plan returned by the API."""

    tasks: list[Task] = Field(
        ...,
        description="A list containing all the generated tasks, their details, and dependencies.",
    )
    summary: str = Field(
        ..., description="A high-level summary of the entire generated plan."
    )
