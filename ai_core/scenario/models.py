from typing import Literal

from pydantic import BaseModel, Field


class TTS(BaseModel):
    voice: str = Field(..., description="Voice name")
    rate: int = Field(
        ..., ge=-100, le=100, description="Rate in percentage (-100 to 100)"
    )
    pitch: int = Field(..., ge=-100, le=100, description="Pitch in Hz (-100 to 100)")


class VoiceOver(BaseModel):
    text: str = Field(..., description="Text to convert to speech")
    tts: TTS = Field(..., description="TTS settings")


class Visual(BaseModel):
    type: Literal["stock_video", "stock_image", "generated_image"]
    query: str = Field(
        ..., description="Query for stock media or prompt for generated image"
    )
    fallback_image_prompt: str = Field(
        ...,
        description="Prompt for generate a fallback image if stock media is not found",
    )
    shot: str = Field(..., description="Shot type (e.g., close-up, wide shot, etc.)")
    mood: str = Field(
        ..., description="Mood of the visual (e.g., happy, dramatic, etc.)"
    )


class Caption(BaseModel):
    text: str = Field(..., description="Caption text")
    position: str = Field(
        ...,
        description="Position of the caption on the screen (e.g., top, bottom, center)",
    )
    style: str = Field(
        ..., description="Style of the caption (e.g., font size, color, etc.)"
    )


class Scene(BaseModel):
    id: str = Field(..., description="Scene ID")
    duration_sec: int = Field(..., description="Duration of the scene in seconds")
    visual: Visual = Field(..., description="Visual elements for the scene")
    caption: Caption = Field(..., description="Caption for the scene")
    voice_over: VoiceOver = Field(..., description="Voice-over for the scene")


class Scenario(BaseModel):
    title: str = Field(..., description="Title of the scenario")
    duration_sec: int = Field(..., description="Duration of the scenario in seconds")
    scenes: list[Scene] = Field(..., description="List of scenes in the scenario")
    style: str = Field(
        ..., description="Style of the scenario (e.g., cinematic, documentary, etc.)"
    )
