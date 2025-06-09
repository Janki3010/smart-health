import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload

from app.models.authentication import EmailToken
from app.repository.base_repository import BaseRepository

class EmailTokenRepository(BaseRepository):
    def __init__(self):
        super().__init__(EmailToken)

    def save_token(self, user_id: uuid.UUID, token: str, token_type: str):
        """Save an email verification or password reset token."""
        expires_at = datetime.utcnow() + timedelta(hours=1)  # 1-hour expiry
        db_token = EmailToken(
            user_id=user_id,
            token=token,
            type=token_type,
            expires_at=expires_at,
            created_at=datetime.utcnow(),
        )
        return self.save(db_token)

    def get_token(self, token: str, token_type: str):
        """Retrieve a token from the database."""
        return self.get_by_filters(
            {"token": token, "type": token_type},
            options=joinedload(EmailToken.user)
        )[0]

    def delete_existing_password_reset_tokens(self, user_id: uuid.UUID):
        """Delete all previous reset password tokens for a user."""
        self.delete_by_filters({"user_id": user_id, "type": "password_reset"})

    def delete_existing_email_verification_tokens(self, user_id: uuid.UUID):
        """Delete all previous email verification tokens for a user."""
        self.delete_by_filters({"user_id": user_id, "type": "email_verification"})
