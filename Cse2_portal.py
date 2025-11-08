import flet as ft
import json
import os

# Container for login/profile content
form_container = ft.Container(
    width=400,
    padding=20,
    border_radius=14,
    bgcolor="#FFFFFF"
)

def main(page: ft.Page):
    page.title = "CSE2 Student Portal"
    page.window_width = 400
    page.window_height = 500
    page.vertical_alignment = ft.alignment.center
    page.horizontal_alignment = ft.alignment.center

    # Load promo info
    with open("Promo_Info.json", "r") as promo_data_file:
        promo_info = json.load(promo_data_file)
        PROMO_NAME = promo_info["promo_name"]
        PROMO_MAJOR = promo_info["major"]
        UNIVERSITY_NAME = promo_info["university"]

    # Load students data
    with open("Cse2_Students.json", "r") as students_data_file:
        students_info = json.load(students_data_file)

    DEFAULT_MALE = "male_avatar.png"
    DEFAULT_FEMALE = "female_avatar.png"

    for s in students_info:
        if not s.get("photo"):
            s["photo"] = DEFAULT_FEMALE if s.get("gender") == "female" else DEFAULT_MALE
        else:
            s["photo"] = os.path.basename(s["photo"])

    def reset_pfp(student, student_pfp, students_info, page):
        default_photo = DEFAULT_FEMALE if student.get("gender") == "female" else DEFAULT_MALE
        student["photo"] = default_photo
        student_pfp.src = default_photo
        page.update()
        with open("Cse2_Students.json", "w") as f:
            json.dump(students_info, f, indent=4)

    def route_change(e):
        page.views.clear()

        # ---------------- Thin Header (full width, independent) ----------------
        header_container = ft.Container(
            content=ft.Row(
                [
                    ft.ElevatedButton(
                        "Home",
                        on_click=lambda e: page.go("/"),
                        width=80,
                        bgcolor="#00A8CC",
                        color=ft.Colors.WHITE
                    ),
                    ft.ElevatedButton(
                        "Login",
                        on_click=lambda e: page.go("/login"),
                        width=80,
                        bgcolor="#007BFF",
                        color=ft.Colors.WHITE
                    ),
                    ft.ElevatedButton(
                        "Courses",
                        on_click=lambda e: page.go("/courses"),
                        width=80,
                        bgcolor="#28A745",
                        color=ft.Colors.WHITE
                    ),
                    ft.Text(
                        "Support: +213 556 68 85 75 | elearning@univ-guelma.dz",
                        size=12,
                        color=ft.Colors.BLACK
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            ),
            height=30,  # thin header
            expand=True,
            bgcolor="#E6E6E6",
            padding=3
        )

        # ---------------- HOME PAGE ----------------
        if page.route == "/":
            home_content = ft.Column(
                [
                    ft.Text("Welcome to CSE2 Portal!", size=24, weight="bold"),
                    ft.Text(f"Promo: {PROMO_NAME} | Major: {PROMO_MAJOR}", size=16)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
            page.views.append(
                ft.View(
                    "/",
                    [header_container, home_content],
                    bgcolor="#CBD4E0"
                )
            )

        # ---------------- LOGIN PAGE ----------------
        elif page.route == "/login":
            error_message = ft.Text("", color=ft.Colors.RED)

            def login_action(e):
                for student in students_info:
                    if student["username"] == username.value and student["password"] == password.value:
                        page.session.set("student", student)
                        page.go("/profile")
                        return
                error_message.value = "❌ Invalid username or password"
                page.update()

            username = ft.TextField(label="Username", on_submit=lambda e: password.focus())
            password = ft.TextField(label="Password", password=True, on_submit=login_action)

            form_container.content = ft.Column(
                [
                    ft.Text("CSE2 Student Portal", size=24, weight="bold"),
                    username,
                    password,
                    ft.ElevatedButton("Login", on_click=login_action),
                    error_message
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

            page.views.append(
                ft.View(
                    "/login",
                    [header_container, form_container],
                    bgcolor="#CBD4E0",
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER
                )
            )

        # ---------------- PROFILE PAGE ----------------
        elif page.route == "/profile":
            student = page.session.get("student")
            if not student:
                page.go("/login")
                return

            emoji = "👩" if student.get("gender") == "female" else "👨"

            student_pfp = ft.Image(src=student["photo"], width=150, height=150, border_radius=75)

            form_container.content = ft.Column(
                [
                    ft.Text(f"{student['full_name']} {emoji}", size=22, weight="bold"),
                    student_pfp,
                    ft.Text(f"Major: {PROMO_MAJOR}"),
                    ft.Text(f"University: {UNIVERSITY_NAME}"),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Change PFP",
                                on_click=lambda e: page.snack_bar.show("Change photo feature...")
                            ),
                            ft.ElevatedButton(
                                "Reset PFP",
                                on_click=lambda e: reset_pfp(student, student_pfp, students_info, page)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

            page.views.append(
                ft.View(
                    "/profile",
                    [header_container, form_container],
                    bgcolor="#CBD4E0",
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER
                )
            )

        page.update()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main, view=ft.WEB_BROWSER, assets_dir="User_Data/assets")
