from domain.repositories.user_repository import UserRepository


class ChangeUserInfoUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def execute(self, username: str, f_name: str, l_name: str):
        self.repo.update(username, f_name, l_name)
