import uuid

from app.models.authentication import User
from app.repository.base_repository import BaseRepository
from app.schemas.authentication import RoleEnum


class AuthenticationRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email: str):
        return self.get_by_filters({"email": email})

    def create_user(self,name: str, email: str, hashed_password: str, role: str):
        new_user = User(
            name=name,
            email=email,
            hashed_password=hashed_password,
            role=role,
            is_verified=False
        )
        return self.save(new_user)

    def verify_user(self, user_id: uuid.UUID):
        return self.update_by_id(user_id, {"is_verified": True})

    def update_user_password(self, user_id: uuid.UUID, hashed_password: str):
        return self.update_by_id(user_id, {"hashed_password": hashed_password})

    def update_data(self, user_id: uuid.UUID, name: str, email: str, hashed_password: str, role:str):
        return self.update_by_id(user_id, {"name": name,"email": email,"hashed_password": hashed_password, "role": role})

    def get_user_by_id(self, user_id: str):
        user_data = self.get_by_id(user_id)
        current_user_data = {"Name": user_data.name, "email": user_data.email, "created_at": str(user_data.created_at), "updated_at": str(user_data.updated_at)}
        return current_user_data

    def update_role(self, uid: str):
        return self.update_by_id(uid, {"role": RoleEnum.doctor})