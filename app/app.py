import reflex as rx
from app.pages.login_page import login_page
from app.pages.register_page import register_page
from app.pages.dashboard_page import dashboard_page
from app.states.auth_state import AuthState

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(dashboard_page, route="/", on_load=AuthState.check_login)
app.add_page(login_page, route="/login")
app.add_page(register_page, route="/register")