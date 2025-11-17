import reflex as rx
from app.states.form_state import FormState, SpecialistAssignment, HighSchoolAssignment
from typing import Optional


def text_input(
    label: str,
    name: str,
    placeholder: str,
    type: str = "text",
    on_change: Optional[rx.event.EventType] = None,
    value: Optional[rx.Var[str]] = None,
    required: bool = False,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            rx.cond(required, rx.el.span(" *", class_name="text-red-500"), ""),
            class_name="block text-sm font-medium text-gray-700 mb-1",
        ),
        rx.el.input(
            name=name,
            placeholder=placeholder,
            type=type,
            on_change=on_change,
            class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors",
            default_value=value,
            required=required,
        ),
        class_name="w-full",
    )


def select_input(
    label: str,
    name: str,
    options: rx.Var[list[str]],
    placeholder: str,
    on_change: rx.event.EventType | None = None,
    value: Optional[rx.Var[str]] = None,
    required: bool = False,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            rx.cond(required, rx.el.span(" *", class_name="text-red-500"), ""),
            class_name="block text-sm font-medium text-gray-700 mb-1",
        ),
        rx.el.select(
            rx.el.option(placeholder, value="", disabled=True),
            rx.foreach(options, lambda option: rx.el.option(option, value=option)),
            name=name,
            on_change=on_change,
            value=value,
            class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors",
            default_value="",
            required=required,
        ),
        class_name="w-full",
    )


def photo_uploader() -> rx.Component:
    return rx.el.div(
        rx.el.label(
            "Foto del Docente",
            class_name="block text-sm font-medium text-gray-700 mb-2",
        ),
        rx.el.div(
            rx.cond(
                FormState.image_preview_url,
                rx.el.div(
                    rx.el.image(
                        src=rx.get_upload_url(FormState.image_preview_url),
                        class_name="h-32 w-32 rounded-full object-cover",
                    ),
                    rx.el.button(
                        rx.icon(tag="x", class_name="h-4 w-4"),
                        on_click=FormState.clear_image,
                        class_name="absolute top-0 right-0 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors",
                        type="button",
                    ),
                    class_name="relative",
                ),
                rx.upload.root(
                    rx.el.div(
                        rx.icon(tag="camera", class_name="h-8 w-8 text-gray-500"),
                        rx.el.p("Subir foto", class_name="text-sm text-gray-600 mt-1"),
                        class_name="flex flex-col items-center justify-center border-2 border-dashed border-gray-300 rounded-full h-32 w-32 cursor-pointer hover:bg-gray-50 transition-colors",
                    ),
                    id="photo_upload",
                    accept={"image/png": [".png"], "image/jpeg": [".jpg", ".jpeg"]},
                    max_files=1,
                    on_drop=FormState.handle_upload(
                        rx.upload_files(upload_id="photo_upload")
                    ),
                ),
            ),
            class_name="flex items-center justify-center w-full",
        ),
        rx.el.div(
            rx.foreach(
                rx.selected_files("photo_upload"),
                lambda file: rx.el.div(
                    file,
                    class_name="p-2 bg-gray-100 rounded border text-sm mt-2 w-full text-center",
                ),
            )
        ),
        class_name="flex flex-col items-center col-span-1 sm:col-span-2 md:col-span-4",
    )


def classroom_teacher_fields() -> rx.Component:
    return rx.el.div(
        select_input("Grado", "grade", FormState.current_grades, "Seleccione grado"),
        text_input("Sección", "section", "U", type="text"),
        class_name="contents",
    )


def specialist_fields() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Asignaciones de Especialista",
            class_name="text-lg font-medium text-gray-800 mt-4 col-span-1 sm:col-span-2 md:col-span-4",
        ),
        select_input(
            "Grado",
            "current_specialist_grade",
            FormState.current_grades,
            "Seleccione grado",
            on_change=FormState.set_current_specialist_grade,
            value=FormState.current_specialist_grade,
        ),
        text_input(
            "Área de Formación",
            "current_specialist_area",
            "Ej: Educación Física",
            on_change=FormState.set_current_specialist_area,
            value=FormState.current_specialist_area,
        ),
        rx.el.div(
            rx.el.label(
                "Sección", class_name="block text-sm font-medium text-gray-700 mb-1"
            ),
            rx.el.input(
                name="current_specialist_section",
                is_disabled=True,
                class_name="w-full px-4 py-2 rounded-lg border border-gray-300 bg-gray-50",
                default_value="U",
                key="U",
            ),
            class_name="w-full",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon(tag="circle_plus", class_name="mr-2"),
                "Añadir Asignación",
                on_click=FormState.add_specialist_assignment,
                type="button",
                class_name="flex items-center justify-center w-full bg-blue-100 text-blue-800 px-4 py-2 rounded-lg hover:bg-blue-200 transition-colors font-medium",
            ),
            class_name="flex items-end h-full",
        ),
        rx.el.div(
            rx.foreach(FormState.specialist_assignments, specialist_assignment_card),
            class_name="col-span-1 sm:col-span-2 md:col-span-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-4",
        ),
        class_name="col-span-1 sm:col-span-2 md:col-span-4 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 items-end",
    )


def specialist_assignment_card(assignment: SpecialistAssignment) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(f"Grado: {assignment['grade']}", class_name="font-semibold"),
            rx.el.p(f"Sección: {assignment['section']}"),
            rx.el.p(f"Área: {assignment['area']}"),
            class_name="flex-grow",
        ),
        rx.el.button(
            rx.icon(tag="trash-2", class_name="h-4 w-4"),
            on_click=lambda: FormState.remove_specialist_assignment(assignment),
            type="button",
            class_name="bg-red-100 text-red-600 p-2 rounded-full hover:bg-red-200 transition-colors",
        ),
        class_name="bg-gray-50 p-4 rounded-lg border border-gray-200 flex items-center justify-between",
    )


def high_school_fields() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Asignaciones de Media General",
            class_name="text-lg font-medium text-gray-800 mt-4 col-span-1 sm:col-span-2 md:col-span-4",
        ),
        select_input(
            "Año",
            "current_high_school_grade",
            FormState.high_school_grades,
            "Seleccione año",
            on_change=FormState.set_current_high_school_grade,
            value=FormState.current_high_school_grade,
        ),
        select_input(
            "Sección",
            "current_high_school_section",
            FormState.high_school_sections,
            "Seleccione sección",
            on_change=FormState.set_current_high_school_section,
            value=FormState.current_high_school_section,
        ),
        select_input(
            "Área de Formación",
            "current_high_school_subject",
            FormState.high_school_subjects,
            "Seleccione área",
            on_change=FormState.set_current_high_school_subject,
            value=FormState.current_high_school_subject,
        ),
        rx.el.div(
            rx.el.button(
                rx.icon(tag="circle_plus", class_name="mr-2"),
                "Añadir Asignación",
                on_click=FormState.add_high_school_assignment,
                type="button",
                class_name="flex items-center justify-center w-full bg-blue-100 text-blue-800 px-4 py-2 rounded-lg hover:bg-blue-200 transition-colors font-medium",
            ),
            class_name="flex items-end h-full",
        ),
        rx.el.div(
            rx.foreach(FormState.high_school_assignments, high_school_assignment_card),
            class_name="col-span-1 sm:col-span-2 md:col-span-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-4",
        ),
        class_name="col-span-1 sm:col-span-2 md:col-span-4 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6 items-end",
    )


def high_school_assignment_card(assignment: HighSchoolAssignment) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(f"Año: {assignment['grade']}", class_name="font-semibold"),
            rx.el.p(f"Sección: {assignment['section']}"),
            rx.el.p(f"Área: {assignment['subject']}"),
            class_name="flex-grow",
        ),
        rx.el.button(
            rx.icon(tag="trash-2", class_name="h-4 w-4"),
            on_click=lambda: FormState.remove_high_school_assignment(assignment),
            type="button",
            class_name="bg-red-100 text-red-600 p-2 rounded-full hover:bg-red-200 transition-colors",
        ),
        class_name="bg-gray-50 p-4 rounded-lg border border-gray-200 flex items-center justify-between",
    )


def registration_form() -> rx.Component:
    return rx.el.div(
        rx.el.form(
            rx.el.div(
                rx.el.h2(
                    "Registro de Docente",
                    class_name="text-2xl font-bold text-gray-800 mb-6 col-span-1 sm:col-span-2 md:col-span-4",
                ),
                photo_uploader(),
                text_input("Primer Nombre", "first_name", "Ej: Juan", required=True),
                text_input("Segundo Nombre", "second_name", "Ej: Carlos"),
                text_input(
                    "Primer Apellido", "first_last_name", "Ej: Pérez", required=True
                ),
                text_input("Segundo Apellido", "second_last_name", "Ej: Gómez"),
                text_input(
                    "Cédula de Identidad", "cedula", "V-12345678", required=True
                ),
                text_input(
                    "Fecha de Nacimiento", "birth_date", "", type="date", required=True
                ),
                select_input(
                    "Género",
                    "gender",
                    FormState.genders,
                    "Seleccione género",
                    required=True,
                ),
                select_input(
                    "Etnia",
                    "ethnicity",
                    FormState.ethnicities,
                    "Seleccione etnia",
                    required=True,
                ),
                rx.el.div(
                    text_input(
                        "Lugar de Residencia",
                        "residence",
                        "Ej: Caracas, D.C.",
                        required=True,
                    ),
                    class_name="col-span-1 sm:col-span-2 md:col-span-4",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Información de la Cuenta",
                        class_name="text-lg font-medium text-gray-800 mt-4 col-span-1 sm:col-span-2 md:col-span-4",
                    ),
                    text_input(
                        "Correo Electrónico",
                        "email",
                        "ejemplo@correo.com",
                        type="email",
                        required=True,
                    ),
                    text_input(
                        "Contraseña",
                        "password",
                        "••••••••",
                        type="password",
                        required=True,
                    ),
                    text_input(
                        "Confirmar Contraseña",
                        "confirm_password",
                        "••••••••",
                        type="password",
                        required=True,
                    ),
                    class_name="col-span-1 sm:col-span-2 md:col-span-4 grid grid-cols-1 sm:grid-cols-2 gap-6 items-end",
                ),
                rx.el.div(
                    select_input(
                        "Cargo",
                        "position",
                        FormState.positions,
                        "Seleccione cargo",
                        on_change=FormState.set_position,
                        required=True,
                    ),
                    class_name="col-span-1 sm:col-span-2",
                ),
                rx.cond(
                    FormState.position == "Docente",
                    rx.el.div(
                        select_input(
                            "Nivel Educativo",
                            "education_level",
                            FormState.education_levels,
                            "Seleccione nivel",
                            on_change=FormState.set_education_level,
                            required=True,
                        ),
                        class_name="col-span-1 sm:col-span-2",
                    ),
                    None,
                ),
                rx.cond(
                    (FormState.position == "Docente")
                    & (
                        (FormState.education_level == "Educación Inicial")
                        | (FormState.education_level == "Educación Primaria")
                    ),
                    rx.el.div(
                        select_input(
                            "Tipo de Docente",
                            "teacher_type",
                            FormState.teacher_types,
                            "Seleccione tipo",
                            on_change=FormState.set_teacher_type,
                            required=True,
                        ),
                        class_name="col-span-1 sm:col-span-2 md:col-span-4",
                    ),
                    None,
                ),
                rx.cond(
                    (FormState.teacher_type == "Maestra de Aula")
                    & (
                        (FormState.education_level == "Educación Inicial")
                        | (FormState.education_level == "Educación Primaria")
                    ),
                    classroom_teacher_fields(),
                    None,
                ),
                rx.cond(
                    (FormState.teacher_type == "Especialista")
                    & (
                        (FormState.education_level == "Educación Inicial")
                        | (FormState.education_level == "Educación Primaria")
                    ),
                    specialist_fields(),
                    None,
                ),
                rx.cond(
                    FormState.education_level == "Educación Media General",
                    high_school_fields(),
                    None,
                ),
                rx.el.div(
                    rx.el.button(
                        rx.cond(
                            FormState.is_submitting,
                            rx.el.div(
                                rx.spinner(size="1", class_name="text-white"),
                                "Procesando...",
                                class_name="flex items-center gap-2",
                            ),
                            "Guardar Registro",
                        ),
                        type="submit",
                        class_name="w-full bg-blue-500 text-white px-6 py-3 rounded-lg hover:bg-blue-600 transition-colors font-medium shadow-md hover:shadow-lg disabled:bg-gray-400 disabled:cursor-not-allowed",
                        disabled=FormState.is_submitting,
                    ),
                    class_name="col-span-1 sm:col-span-2 md:col-span-4 pt-4",
                ),
                class_name="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-6",
            ),
            on_submit=FormState.handle_submit,
            reset_on_submit=False,
        ),
        rx.el.p(
            "¿Ya tienes una cuenta? ",
            rx.el.a(
                "Inicia sesión aquí",
                href="/login",
                class_name="text-blue-500 hover:underline font-medium",
            ),
            class_name="text-center text-sm text-gray-600 mt-6",
        ),
        class_name="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 w-full max-w-4xl mx-auto",
    )