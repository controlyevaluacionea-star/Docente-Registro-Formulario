import reflex as rx
from app.states.auth_state import AuthState


def dashboard_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.image(src="placeholder.svg", width="150px", class_name="mb-8"),
            rx.el.h1(
                f"Bienvenido, {AuthState.logged_in_user_email}",
                class_name="text-2xl font-bold",
            ),
            rx.el.button(
                "Cerrar Sesión",
                on_click=AuthState.logout,
                class_name="mt-4 bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600",
            ),
            class_name="w-full min-h-screen flex flex-col items-center justify-center p-4 sm:p-6 md:p-8 bg-gray-50",
        ),
        class_name="font-['Inter'] bg-white",
    )