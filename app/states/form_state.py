import reflex as rx
from typing import Optional, TypedDict


class SpecialistAssignment(TypedDict):
    grade: str
    section: str
    area: str


class HighSchoolAssignment(TypedDict):
    grade: str
    section: str
    subject: str


class FormState(rx.State):
    form_data: dict = {}
    first_name: str = ""
    second_name: str = ""
    first_last_name: str = ""
    second_last_name: str = ""
    cedula: str = ""
    birth_date: str = ""
    gender: str = ""
    ethnicity: str = ""
    residence: str = ""
    email: str = ""
    password: str = ""
    confirm_password: str = ""
    position: str = ""
    education_level: str = ""
    image_preview_url: Optional[str] = None
    uploaded_file_name: Optional[str] = None
    uploading: bool = False
    is_submitting: bool = False
    genders: list[str] = ["Masculino", "Femenino", "Otro"]
    ethnicities: list[str] = [
        "Mestizo",
        "Afrodescendiente",
        "Indígena",
        "Blanco",
        "Otro",
    ]
    positions: list[str] = ["Docente", "Administrativo", "Obrero", "Directivo"]
    education_levels: list[str] = [
        "Educación Inicial",
        "Educación Primaria",
        "Educación Media General",
    ]
    teacher_type: str = ""
    teacher_types: list[str] = ["Maestra de Aula", "Especialista"]
    initial_grades: list[str] = ["Grupo 1", "Grupo 2"]
    primary_grades: list[str] = [
        "1er Grado",
        "2do Grado",
        "3er Grado",
        "4to Grado",
        "5to Grado",
        "6to Grado",
    ]
    high_school_grades: list[str] = [
        "1er Año",
        "2do Año",
        "3er Año",
        "4to Año",
        "5to Año",
    ]
    high_school_sections: list[str] = ["A", "B", "Ambas"]
    high_school_subjects: list[str] = [
        "Lengua y Literatura",
        "Idiomas",
        "Matemática",
        "Física",
        "Biología",
        "Educación en Valores",
    ]
    specialist_assignments: list[SpecialistAssignment] = []
    current_specialist_grade: str = ""
    current_specialist_section: str = "U"
    current_specialist_area: str = ""
    high_school_assignments: list[HighSchoolAssignment] = []
    current_high_school_grade: str = ""
    current_high_school_section: str = ""
    current_high_school_subject: str = ""

    @rx.var
    def current_grades(self) -> list[str]:
        if self.education_level == "Educación Inicial":
            return self.initial_grades
        if self.education_level == "Educación Primaria":
            return self.primary_grades
        return []

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        if not files:
            return
        self.uploading = True
        file = files[0]
        upload_data = await file.read()
        upload_dir = rx.get_upload_dir()
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / file.name
        with file_path.open("wb") as f:
            f.write(upload_data)
        self.uploaded_file_name = file.name
        self.image_preview_url = file.name
        self.uploading = False

    def _validate_form(self, form_data: dict) -> list[str]:
        errors = []
        required_fields = {
            "first_name": "Primer Nombre",
            "first_last_name": "Primer Apellido",
            "cedula": "Cédula",
            "birth_date": "Fecha de Nacimiento",
            "gender": "Género",
            "ethnicity": "Etnia",
            "residence": "Lugar de Residencia",
            "position": "Cargo",
            "email": "Correo Electrónico",
            "password": "Contraseña",
            "confirm_password": "Confirmar Contraseña",
        }
        for field, label in required_fields.items():
            if not form_data.get(field):
                errors.append(f"El campo '{label}' es requerido.")
        if form_data.get("password") != form_data.get("confirm_password"):
            errors.append("Las contraseñas no coinciden.")
        if form_data.get("cedula") and (not form_data["cedula"].startswith("V-")):
            errors.append("El formato de la Cédula debe ser V-########.")
        position = form_data.get("position")
        if position == "Docente":
            education_level = self.education_level
            if not education_level:
                errors.append("El campo 'Nivel Educativo' es requerido.")
            elif education_level in ["Educación Inicial", "Educación Primaria"]:
                teacher_type = self.teacher_type
                if not teacher_type:
                    errors.append("El campo 'Tipo de Docente' es requerido.")
                elif teacher_type == "Maestra de Aula":
                    if not form_data.get("grade") or not form_data.get("section"):
                        errors.append(
                            "Debe seleccionar Grado y Sección para Maestra de Aula."
                        )
                elif teacher_type == "Especialista":
                    if not self.specialist_assignments:
                        errors.append(
                            "Debe agregar al menos una asignación de especialista."
                        )
            elif education_level == "Educación Media General":
                if not self.high_school_assignments:
                    errors.append(
                        "Debe agregar al menos una asignación de media general."
                    )
        return errors

    def _reset_fields(self):
        self.image_preview_url = None
        self.uploaded_file_name = None
        self.position = ""
        self.education_level = ""
        self.teacher_type = ""
        self.email = ""
        self.password = ""
        self.confirm_password = ""
        self.specialist_assignments = []
        self.high_school_assignments = []
        self.current_specialist_grade = ""
        self.current_specialist_area = ""
        self.current_high_school_grade = ""
        self.current_high_school_section = ""
        self.current_high_school_subject = ""

    @rx.event
    async def handle_submit(self, form_data: dict):
        self.is_submitting = True
        yield
        errors = self._validate_form(form_data)
        if errors:
            for error in errors:
                yield rx.toast.error(error, duration=5000)
            self.is_submitting = False
            return
        from app.db import get_docentes_collection
        from app.states.auth_state import AuthState

        auth_state = await self.get_state(AuthState)
        email = form_data.get("email")
        password = form_data.get("password")
        docentes_collection = get_docentes_collection()
        if docentes_collection.find_one({"email": email}):
            yield rx.toast.error("El correo electrónico ya está registrado.")
            self.is_submitting = False
            return
        docente_data = {key: value for key, value in form_data.items()}
        if self.uploaded_file_name:
            docente_data["photo"] = self.uploaded_file_name
        docente_data["specialist_assignments"] = list(self.specialist_assignments)
        docente_data["high_school_assignments"] = list(self.high_school_assignments)
        try:
            docentes_collection.insert_one(docente_data)
        except Exception as e:
            import logging

            logging.exception(f"Error inserting data into MongoDB: {e}")
            yield rx.toast.error("Error al guardar los datos en la base de datos.")
            self.is_submitting = False
            return
        yield AuthState.register(email, password)
        import time

        time.sleep(2)
        self.is_submitting = False
        self._reset_fields()
        yield rx.clear_selected_files("photo_upload")
        yield rx.call_script("document.querySelector('form').reset()")

    @rx.event
    def clear_image(self):
        self.image_preview_url = None
        self.uploaded_file_name = None

    @rx.event
    def add_specialist_assignment(self):
        if self.current_specialist_grade and self.current_specialist_area:
            self.specialist_assignments.append(
                {
                    "grade": self.current_specialist_grade,
                    "section": self.current_specialist_section,
                    "area": self.current_specialist_area,
                }
            )
            self.current_specialist_grade = ""
            self.current_specialist_area = ""

    @rx.event
    def remove_specialist_assignment(self, assignment: SpecialistAssignment):
        self.specialist_assignments = [
            a for a in self.specialist_assignments if a != assignment
        ]

    @rx.event
    def add_high_school_assignment(self):
        if (
            self.current_high_school_grade
            and self.current_high_school_section
            and self.current_high_school_subject
        ):
            self.high_school_assignments.append(
                {
                    "grade": self.current_high_school_grade,
                    "section": self.current_high_school_section,
                    "subject": self.current_high_school_subject,
                }
            )
            self.current_high_school_grade = ""
            self.current_high_school_section = ""
            self.current_high_school_subject = ""

    @rx.event
    def remove_high_school_assignment(self, assignment: HighSchoolAssignment):
        self.high_school_assignments = [
            a for a in self.high_school_assignments if a != assignment
        ]