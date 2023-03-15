from typing import List, Optional
from fastapi import Request


class RegisterForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.email: Optional[str] = None
        self.password: Optional[str] = None
        self.confirm_password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.email = form.get("email")
        self.password = form.get("password")
        self.confirm_password = form.get("confirm_password")

    async def is_valid(self):
        if not self.username or not (self.username):
            self.errors.append("Username is required")
        if not self.email or not (self.email.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        if not (self.confirm_password == self.password):
            self.errors.append("Confirmation of password is incorrect") 
        if not self.errors:
            return True
        return False