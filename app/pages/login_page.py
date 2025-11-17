import reflex as rx
from app.components.login_form import login_form


def login_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.image(src="placeholder.svg", width="150px", class_name="mb-8"),
            login_form(),
            class_name="w-full min-h-screen flex flex-col items-center justify-center p-4 sm:p-6 md:p-8 bg-gray-50",
        ),
        class_name="font-['Inter'] bg-white",
    )