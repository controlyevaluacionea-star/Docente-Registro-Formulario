import reflex as rx
from app.states.auth_state import AuthState


def login_form() -> rx.Component:
    return rx.el.div(
        rx.el.form(
            rx.el.div(
                rx.el.h2(
                    "Iniciar Sesión",
                    class_name="text-2xl font-bold text-gray-800 mb-6 text-center",
                ),
                rx.el.div(
                    rx.el.label(
                        "Correo Electrónico",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="email",
                        placeholder="ejemplo@correo.com",
                        type="email",
                        class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors",
                        required=True,
                    ),
                    class_name="w-full mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Contraseña",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="password",
                        placeholder="••••••••",
                        type="password",
                        class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors",
                        required=True,
                    ),
                    class_name="w-full mb-6",
                ),
                rx.el.button(
                    rx.cond(
                        AuthState.is_loading,
                        rx.el.div(
                            rx.spinner(size="1", class_name="text-white"),
                            "Procesando...",
                            class_name="flex items-center gap-2",
                        ),
                        "Iniciar Sesión",
                    ),
                    type="submit",
                    class_name="w-full bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors font-medium shadow-md hover:shadow-lg disabled:bg-gray-400 disabled:cursor-not-allowed",
                    disabled=AuthState.is_loading,
                ),
                class_name="flex flex-col items-center",
            ),
            on_submit=AuthState.login,
        ),
        rx.el.p(
            "¿No tienes una cuenta? ",
            rx.el.a(
                "Regístrate aquí",
                href="/register",
                class_name="text-blue-500 hover:underline font-medium",
            ),
            class_name="text-center text-sm text-gray-600 mt-6",
        ),
        class_name="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 w-full max-w-md mx-auto",
    )