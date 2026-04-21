"""Action API router — AI-powered task recommendations and pipeline."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.agents.manager import decide_next_action
from app.config.database import get_db
from app.schemas.task import ActionResponse, ErrorResponse, RecommendationResponse, TaskResponse
from app.services.task_service import get_pending_tasks, get_top_task_with_score

router = APIRouter(tags=["Actions"])


@router.get("/next-action", response_model=ActionResponse, summary="Run AI pipeline on top task",
             responses={404: {"model": ErrorResponse}})
async def next_action(db: Session = Depends(get_db)) -> ActionResponse:
    """Run the full agent pipeline (Planner → Executor → Reviewer) on the top task."""
    result = decide_next_action(db)
    if result.get("message") == "No pending tasks available":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No pending tasks available")
    task_obj = result.get("task")
    return ActionResponse(
        task_id=getattr(task_obj, "id", None), plan=result.get("plan"),
        result=result.get("result"), review=result.get("review_result"),
        message="Pipeline completed successfully",
    )


@router.get("/recommend", response_model=RecommendationResponse, summary="Get Jarvis's smart recommendation",
             responses={404: {"model": ErrorResponse}})
async def recommend_task(db: Session = Depends(get_db)) -> RecommendationResponse:
    """Lightweight scoring-based recommendation (no LLM pipeline)."""
    top_task, score, reason = get_top_task_with_score(db)
    pending = get_pending_tasks(db)
    if not top_task:
        return RecommendationResponse(
            reason="No pending tasks", spoken_recommendation="You have no pending tasks.", pending_count=0,
        )
    spoken = f"I recommend '{top_task.title}' because {reason}. You have {len(pending)} task{'s' if len(pending) != 1 else ''} pending."
    return RecommendationResponse(
        recommended_task=TaskResponse.model_validate(top_task),
        reason=reason, score=score, spoken_recommendation=spoken, pending_count=len(pending),
    )
