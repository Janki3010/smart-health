from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.chatbot import chat_router
from app.controllers.appointment_controller import appointment_router
from app.controllers.authentication_controller import auth_router
from app.controllers.chatbot_controller import chatbot_router
from app.controllers.doctor_controller import dr_router
from app.controllers.prediction_controller import prediction_router
from app.controllers.user_controller import user_router
from app.middleware.auth_middleware import AuthMiddleware
from app.middleware.custom_openapi import CustomOpenAPI
from app.config.settings import settings

limiter = Limiter(key_func=get_remote_address, default_limits=["1/seconds"])

app = FastAPI(title="Smart-Health")

app.state.limiter = limiter

app.add_middleware(AuthMiddleware)

# Add SlowAPI middleware
app.add_middleware(SlowAPIMiddleware)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(dr_router)
app.include_router(appointment_router)
app.include_router(prediction_router)
app.include_router(chatbot_router)

# Initialize and set custom OpenAPI
custom_openapi = CustomOpenAPI(app)
app.openapi = custom_openapi.generate_openapi


@app.exception_handler(RateLimitExceeded)
def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."},
    )

from app.config.settings import settings
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(settings.PORT), reload=True)