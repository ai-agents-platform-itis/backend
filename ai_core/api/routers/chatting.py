from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Query

from chatting import Chatting, get_chatting

app = FastAPI(title="Chatting", version="1.0.0")
router = APIRouter(prefix="/chatting", tags=["CHATTING"])
app.include_router(router)


ChattingDep = Annotated[Chatting, Depends(get_chatting)]


@router.get("/answer_question")
async def answer_question_endpoint(
    chatting: ChattingDep,
    campaign_id: int = Query(..., description="ID кампании"),
    question: str = Query(..., description="Вопрос"),
):
    response = await chatting.answer_question(campaign_id=campaign_id, query=question)

    return response
