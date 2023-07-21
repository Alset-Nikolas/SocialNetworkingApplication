from app.factory import PASSWORD_CONTEXT

class PasswordService:
    @staticmethod
    def get_hashed_password(password: str) -> str:
        return PASSWORD_CONTEXT.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_pass: str) -> bool:
        return PASSWORD_CONTEXT.verify(password, hashed_pass)