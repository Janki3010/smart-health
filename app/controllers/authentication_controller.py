from fastapi import Depends, APIRouter, Request
from fastapi_restful.cbv import cbv
from fastapi import BackgroundTasks
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from app.config.settings import settings

from app.schemas.authentication import (
    UserCreate,
    Login,
    TokenResponse,
    ForgotPasswordRequest,
    ResetPassword
)

from app.services.authentication_service import AuthenticationService
from app.services.oatuh_service import oauth

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@cbv(auth_router)
class AuthenticationController:
    def __init__(self, auth_service: AuthenticationService = Depends()):
        self.auth_service = auth_service

    @auth_router.post("/register", status_code=HTTP_201_CREATED, summary="Register a new user")
    def register(
            self,
            background_tasks: BackgroundTasks,
            user: UserCreate,
    ):
        self.auth_service.register(user, background_tasks)
        return {"message": "User created! Please check your email to verify your account."}

    @auth_router.post("/login", response_model=TokenResponse, status_code=HTTP_200_OK, summary="Login user")
    def login(
        self,
        user: Login,
    ):
        access_token = self.auth_service.login(user)
        return {"access_token": access_token, "token_type": "bearer"}

    @auth_router.get("/verify-email/{token}", summary="Verify email with token", include_in_schema=False)
    def verify_email(self, token: str):
        self.auth_service.verify_email(token)
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/login", status_code=303)

    @auth_router.post("/forgot-password", summary="Request password reset")
    def forgot_password(
        self,
        background_tasks: BackgroundTasks,
        request: ForgotPasswordRequest
    ):
        self.auth_service.forgot_password(request, background_tasks)
        return {"message": "Password reset email sent."}

    @auth_router.post("/reset-password/{token}", summary="Reset password")
    def reset_password(
        self,
        token: str,
        request: ResetPassword
    ):
         self.auth_service.reset_password(token, request)
         return {"message": "Password reset successfully"}
    #
    # @auth_router.get("/google-login")
    # async def google_login(self, request: Request):
    #     redirect_uri = request.url_for("auth")
    #     return await oauth.myApp.authorize_redirect(request, redirect_uri)
    #
    # @auth_router.get("/signin-google")
    # async def auth(self, request: Request):
    #     try:
    #         token = await oauth.myApp.authorize_access_token(request)
    #     except:
    #         pass
    #     request.session["user"] = token

    # @auth_router.get("/google-login", summary="Redirect to Google for login")
    # async def signin_google(self, request: Request):
    #     redirect_uri = str(request.base_url) + "auth/signin-google"
    #     return await oauth.google.authorize_redirect(request, redirect_uri)
    #
    # @auth_router.get("/signin-google", summary="Googles login callback")
    # async def auth(self, request: Request):
    #     token = await oauth.google.authorize_access_token(request)
    #     user_info = await oauth.google.parse_id_token(request, token)
    #
    #     # user = self.auth_service.google_login(user_info)
    #     return JSONResponse(content={"user": user_info})
    #
