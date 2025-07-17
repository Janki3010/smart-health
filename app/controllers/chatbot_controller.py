from fastapi import APIRouter
from fastapi_restful.cbv import cbv
from starlette.status import HTTP_200_OK

from app.schemas.ChatRequest import ChatRequest
from app.services.chat_service import ChatService

chatbot_router = APIRouter(prefix="/chat", tags=["Chatbot"])

@cbv(chatbot_router)
class ChatBotController:
    def __init__(self):
        self.chat_service = ChatService()

    @chatbot_router.post(
         "/",
         status_code=HTTP_200_OK,
         summary="Ask you health related question"
     )
    def get_chat_response(self, user_query: ChatRequest):
         return self.chat_service.get_ai_response(user_query)