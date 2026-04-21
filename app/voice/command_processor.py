"""Voice command processor — executes parsed commands against the task system."""

from typing import Optional
from sqlalchemy.orm import Session
from app.core.logging import logger
from app.schemas.task import TaskResponse
from app.schemas.voice import VoiceIntent, VoiceResponse
from app.services.task_service import (
    delete_task, delete_task_by_title, find_task_by_title,
    get_all_tasks, get_pending_tasks, get_top_task_with_score,
    mark_task_completed, quick_add_task,
)
from app.voice.intent_parser import ParsedCommand


def process_command(cmd: ParsedCommand, db: Session) -> VoiceResponse:
    """Central dispatcher — routes each intent to its handler."""
    logger.info("Processing voice command: intent=%s title='%s'", cmd.intent, cmd.task_title)
    handlers = {
        "add_task": _handle_add_task, "delete_task": _handle_delete_task,
        "complete_task": _handle_complete_task, "next_action": _handle_next_action,
        "list_tasks": _handle_list_tasks, "task_status": _handle_task_status,
        "help": _handle_help,
    }
    return handlers.get(cmd.intent, _handle_unknown)(cmd, db)


def _handle_add_task(cmd: ParsedCommand, db: Session) -> VoiceResponse:
    if not cmd.task_title:
        return VoiceResponse(intent=VoiceIntent.ADD_TASK, spoken_response="What task would you like me to add?", success=False)
    task = quick_add_task(title=cmd.task_title, db=db, priority=cmd.priority)
    spoken = f"Done! I've added '{task.title}' as a {task.priority} priority task. It's task number {task.id}."
    return VoiceResponse(intent=VoiceIntent.ADD_TASK, spoken_response=spoken, task=TaskResponse.model_validate(task))


def _handle_delete_task(cmd: ParsedCommand, db: Session) -> VoiceResponse:
    deleted = None
    if cmd.task_id:
        deleted = delete_task(cmd.task_id, db)
    elif cmd.task_title:
        deleted = delete_task_by_title(cmd.task_title, db)
    if deleted:
        return VoiceResponse(intent=VoiceIntent.DELETE_TASK, spoken_response=f"Task '{deleted.title}' has been deleted. One less thing to worry about!")
    target = cmd.task_title or f"#{cmd.task_id}"
    return VoiceResponse(intent=VoiceIntent.DELETE_TASK, spoken_response=f"I couldn't find a task matching '{target}'.", success=False)


def _handle_complete_task(cmd: ParsedCommand, db: Session) -> VoiceResponse:
    completed = None
    if cmd.task_id:
        completed = mark_task_completed(cmd.task_id, db)
    elif cmd.task_title:
        task = find_task_by_title(cmd.task_title, db)
        if task:
            completed = mark_task_completed(task.id, db)
    if completed:
        remaining = len(get_pending_tasks(db))
        spoken = f"Awesome! '{completed.title}' is marked as completed. You have {remaining} task{'s' if remaining != 1 else ''} remaining."
        return VoiceResponse(intent=VoiceIntent.COMPLETE_TASK, spoken_response=spoken, task=TaskResponse.model_validate(completed))
    return VoiceResponse(intent=VoiceIntent.COMPLETE_TASK, spoken_response=f"I couldn't find that task.", success=False)


def _handle_next_action(cmd: ParsedCommand, db: Session) -> VoiceResponse:
    top_task, score, reason = get_top_task_with_score(db)
    if not top_task:
        return VoiceResponse(intent=VoiceIntent.NEXT_ACTION, spoken_response="You have no pending tasks. You're all caught up!")
    pending = get_pending_tasks(db)
    spoken = f"I recommend you work on '{top_task.title}' because {reason}. It's {top_task.priority} priority. You have {len(pending)} task{'s' if len(pending) != 1 else ''} pending."
    return VoiceResponse(intent=VoiceIntent.NEXT_ACTION, spoken_response=spoken, task=TaskResponse.model_validate(top_task))


def _handle_list_tasks(cmd: ParsedCommand, db: Session) -> VoiceResponse:
    pending = get_pending_tasks(db)
    if not pending:
        return VoiceResponse(intent=VoiceIntent.LIST_TASKS, spoken_response="You have no pending tasks.", tasks=[])
    items = [f"Number {i}: '{t.title}', {t.priority} priority" for i, t in enumerate(pending[:5], 1)]
    extra = f" and {len(pending) - 5} more" if len(pending) > 5 else ""
    spoken = f"You have {len(pending)} pending task{'s' if len(pending) != 1 else ''}. Here they are: {'. '.join(items)}{extra}."
    return VoiceResponse(intent=VoiceIntent.LIST_TASKS, spoken_response=spoken, tasks=[TaskResponse.model_validate(t) for t in pending])


def _handle_task_status(cmd: ParsedCommand, db: Session) -> VoiceResponse:
    task = None
    if cmd.task_id:
        from app.services.task_service import get_task_by_id
        task = get_task_by_id(cmd.task_id, db)
    elif cmd.task_title:
        task = find_task_by_title(cmd.task_title, db)
    if task:
        return VoiceResponse(intent=VoiceIntent.TASK_STATUS, spoken_response=f"Task '{task.title}' is {task.status} with {task.priority} priority.", task=TaskResponse.model_validate(task))
    return VoiceResponse(intent=VoiceIntent.TASK_STATUS, spoken_response="I couldn't find that task.", success=False)


def _handle_help(cmd: ParsedCommand, db: Session) -> VoiceResponse:
    spoken = ("I'm Jarvis, your task assistant. Say 'add task' to create one. "
              "Say 'delete task' to remove. Say 'what should I do next' for recommendations. "
              "Say 'list tasks' to hear all. Say 'mark task done' to complete.")
    return VoiceResponse(intent=VoiceIntent.HELP, spoken_response=spoken)


def _handle_unknown(cmd: ParsedCommand, db: Session) -> VoiceResponse:
    return VoiceResponse(intent=VoiceIntent.UNKNOWN, spoken_response=f"I didn't catch that. You said: '{cmd.raw_text}'. Try 'help'.", success=False)
