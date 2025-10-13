import json
from fastapi import APIRouter, HTTPException, Request
from google.genai import types
from schemas import GoalRequest, TaskPlan
from db.model import PlanDB
from db.database import get_plan_collection
from config import logger


router = APIRouter(tags=["Planner"], prefix="/v1")


@router.post("/plans", status_code=201, response_model=TaskPlan)
async def create_task_plan(request: Request, goal_request: GoalRequest):
    """
    Takes a high-level user goal, generates a structured task plan using Gemini,
    saves the plan to MongoDB, and returns the plan.
    """
    aio = request.app.state.aio
    full_prompt = f"""
Goal: {goal_request.goal_text}
CONTEXT: {goal_request.context or 'No additional context provided'}

You are an expert project manager. Break down the user's GOAL into 5 to 10 distinct, actionable tasks.
Ensure task IDs are sequential (T01, T02, T03, ...).
Calculate suggested deadlines based on the estimated durations, assuming the current date is 2025-10-13.
The final output MUST strictly conform to the provided JSON schema (TaskPlan).
Return only valid JSON that exactly matches the schema.
"""

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=TaskPlan,
        temperature=0.3,
    )

    try:

        response = await aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt,
            config=config,
        )

        raw_text = getattr(response, "text", None)
        if not raw_text:
            logger.error(
                "LLM returned empty response for goal: %s", goal_request.goal_text
            )
            raise HTTPException(status_code=500, detail="LLM returned empty response.")

        stripped = raw_text.strip()
        if not (stripped.startswith("{") or stripped.startswith("[")):
            logger.error("LLM failed to generate valid JSON: %s", raw_text)
            raise HTTPException(
                status_code=500, detail="LLM failed to generate valid JSON."
            )

        parsed = json.loads(raw_text)

        plan = TaskPlan.model_validate(parsed)
        plan_dict = plan.model_dump()

        plan_db_data = PlanDB(
            user_id=goal_request.user_id,
            goal_text=goal_request.goal_text,
            context=goal_request.context,
            summary=plan_dict["summary"],
            tasks=plan_dict["tasks"],
        )

        collection = get_plan_collection()
        inserted_result = await collection.insert_one(
            plan_db_data.model_dump(by_alias=True)
        )

        logger.info(
            "Successfully generated and saved plan (ID: %s) for goal: %s",
            inserted_result.inserted_id,
            goal_request.goal_text[:30] + "...",
        )

        return plan

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Unexpected error during LLM or DB processing: %s", e)

        if "Database connection failed" in str(e):
            raise HTTPException(
                status_code=503,
                detail="Service Unavailable: Database connection failed.",
            )
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
