# from app.repository.base_repository import BaseRepository
# from app.models.authentication import User
#
# class UserRepository(BaseRepository):
#     def __init__(self):
#         super().__init__(User)
#
#     def get_user_by_id(self, user_id: str):
#         user_data = self.get_by_id(user_id)
#         current_user_data = {"Name": user_data.name, "email": user_data.email, "created_at": str(user_data.created_at), "updated_at": str(user_data.updated_at)}
#         return current_user_data