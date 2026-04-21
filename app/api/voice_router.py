"""Voice API router — process voice commands via REST."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.voice import VoiceCommandRequest, VoiceResponse
from app.voice.command_processor import process_command
from app.voice.intent_parser import parse_voice_command

router = APIRouter(prefix="/voice", tags=["Voice"])


@router.post("/command", response_model=VoiceResponse, summary="Process a voice command")
async def voice_command(request: VoiceCommandRequest, db: Session = Depends(get_db)) -> VoiceResponse:
    """
    Accept a text command (from speech-to-text or typed) and process it.

    **Example commands:**
    - ``"add task buy groceries with high priority"``
    - ``"delete task buy groceries"``
    - ``"what should I do next"``
    - ``"list my tasks"``
    - ``"mark task 3 as done"``
    """
    cmd = parse_voice_command(request.text)
    return process_command(cmd, db)
