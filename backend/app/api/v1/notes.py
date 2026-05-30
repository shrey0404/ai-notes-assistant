"""
Notes API endpoints - v1
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.database import get_db
from app.services.note_service import NoteService
from app.services.ai_service import AIService
from app.schemas.note import (
    NoteCreate,
    NoteUpdate,
    NoteResponse,
    NoteListResponse,
    SummaryResponse
)

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"description": "Note not found"}}
)


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db)
) -> NoteResponse:
    """
    Create a new note.
    
    - **title**: Note title (required, max 255 chars)
    - **content**: Note content (required)
    """
    service = NoteService(db)
    return service.create_note(note)


@router.get("", response_model=list[NoteListResponse])
async def get_all_notes(
    db: Session = Depends(get_db)
) -> list[NoteListResponse]:
    """
    Get all notes with basic information.
    
    Returns a list of all notes with id, title, and timestamps.
    """
    service = NoteService(db)
    return service.fetch_all_notes()


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: UUID,
    db: Session = Depends(get_db)
) -> NoteResponse:
    """
    Get a specific note by ID.
    
    - **note_id**: UUID of the note
    
    Returns full note details including content.
    """
    service = NoteService(db)
    note = service.fetch_note_by_id(note_id)
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    
    return note


@router.put("/{note_id}", response_model=NoteResponse)
async def update_note(
    note_id: UUID,
    note_update: NoteUpdate,
    db: Session = Depends(get_db)
) -> NoteResponse:
    """
    Update an existing note.
    
    - **note_id**: UUID of the note to update
    - **title**: New title (optional)
    - **content**: New content (optional)
    
    Only provided fields will be updated.
    """
    service = NoteService(db)
    updated_note = service.update_note(note_id, note_update)
    
    if not updated_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    
    return updated_note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: UUID,
    db: Session = Depends(get_db)
) -> None:
    """
    Delete a note permanently.
    
    - **note_id**: UUID of the note to delete
    """
    service = NoteService(db)
    success = service.delete_note(note_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )


@router.post("/{note_id}/summary", response_model=SummaryResponse)
async def generate_summary(
    note_id: UUID,
    db: Session = Depends(get_db)
) -> SummaryResponse:
    """
    Generate an AI summary for a note.
    
    - **note_id**: UUID of the note to summarize
    
    Returns 3-5 bullet points summarizing the note content.
    """
    service = NoteService(db)
    note = service.fetch_note_by_id(note_id)
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found"
        )
    
    try:
        ai_service = AIService()
        summary_bullets = ai_service.generate_summary(note.content)
        return SummaryResponse(summary=summary_bullets)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate summary: {str(e)}"
        )
