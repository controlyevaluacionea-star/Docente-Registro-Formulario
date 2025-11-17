import reflex as rx
from pydantic import BaseModel, EmailStr
import logging
from typing import Optional
from app.db import get_users_collection


class User(BaseModel):
    email: EmailStr
    password_hash: str


class AuthState(rx.State):
    logged_in_user_email: str = rx.LocalStorage("", name="logged_in_user")
    is_loading: bool = False

    @rx.var
    def is_authenticated(self) -> bool:
        return self.logged_in_user_email != ""

    @rx.event
    def register(self, email: str, password: str) -> rx.event.EventSpec:
        self.is_loading = True
        yield
        try:
            users_collection = get_users_collection()
            if users_collection.find_one({"email": email}):
                self.is_loading = False
                return rx.toast.error("El correo electrónico ya está registrado.")
            new_user = User(email=email, password_hash=password)
            users_collection.insert_one(new_user.model_dump())
            self.is_loading = False
            yield rx.toast.success(
                "¡Cuenta creada exitosamente! Ahora puede iniciar sesión."
            )
            return rx.redirect("/login")
        except Exception as e:
            logging.exception(f"Error during registration: {e}")
            self.is_loading = False
            return rx.toast.error(
                "Ocurrió un error durante el registro. Intente de nuevo."
            )

    @rx.event
    def login(self, form_data: dict):
        self.is_loading = True
        yield
        email = form_data.get("email")
        password = form_data.get("password")
        if not email or not password:
            self.is_loading = False
            return rx.toast.error("Correo y contraseña son requeridos.")
        try:
            users_collection = get_users_collection()
            user_data = users_collection.find_one({"email": email})
            import time

            time.sleep(1)
            if not user_data or user_data["password_hash"] != password:
                self.is_loading = False
                return rx.toast.error("Correo o contraseña inválidos.")
            self.logged_in_user_email = user_data["email"]
            self.is_loading = False
            yield rx.toast.success("¡Inicio de sesión exitoso!")
            return rx.redirect("/")
        except Exception as e:
            logging.exception(f"Error during login: {e}")
            self.is_loading = False
            return rx.toast.error(
                "Ocurrió un error al iniciar sesión. Intente de nuevo."
            )

    @rx.event
    def logout(self):
        self.logged_in_user_email = ""
        yield rx.toast.info("Sesión cerrada.")
        return rx.redirect("/login")

    @rx.event
    def check_login(self):
        if not self.is_authenticated:
            return rx.redirect("/login")