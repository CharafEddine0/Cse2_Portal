import flet as ft
import json
import os

# Reusable container for page content
form_container = ft.Container(
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

    # ---------------- LOAD DATA ----------------
    with open("Promo_Info.json", "r") as promo_data_file:
        promo_info = json.load(promo_data_file)
        PROMO_NAME = promo_info["promo_name"]
        PROMO_MAJOR = promo_info["major"]
        UNIVERSITY_NAME = promo_info["university"]
        PROMO_YEAR = promo_info["year"]

    with open("Cse2_Students.json", "r") as students_data_file:
        students_info = json.load(students_data_file)

    DEFAULT_MALE = "male_avatar.png"
    DEFAULT_FEMALE = "female_avatar.png"

    # Add default images if missing
    for s in students_info:
        if not s.get("photo"):
            s["photo"] = DEFAULT_FEMALE if s.get("gender") == "female" else DEFAULT_MALE
        else:
            s["photo"] = os.path.basename(s["photo"])

    # ---------------- FUNCTION: RESET PROFILE PICTURE ----------------
    def reset_pfp(student, student_pfp, students_info, page):
        default_photo = DEFAULT_FEMALE if student.get("gender") == "female" else DEFAULT_MALE
        student["photo"] = default_photo
        student_pfp.src = default_photo
        page.update()
        # Save updated data
        with open("Cse2_Students.json", "w") as students_data_file:
            json.dump(students_info, students_data_file, indent=4)

    # ---------------- ROUTE HANDLER ----------------
    def route_change(e):
        page.views.clear()

        # ---------------- HOME PAGE ----------------
        if page.route == "/":
            logged_in_student = page.session.get("student")

            if logged_in_student:
                # Header for logged-in users
                header_buttons = [
                    ft.ElevatedButton(
                        "Profile",
                        on_click=lambda e: page.go("/profile"),
                        bgcolor="#00A8CC",
                        color=ft.Colors.WHITE,
                        width=100,
                    ),
                    ft.ElevatedButton(
                        "Courses",
                        on_click=lambda e: page.go("/courses"),
                        bgcolor="#007BFF",
                        color=ft.Colors.WHITE,
                        width=100,
                    ),
                    ft.ElevatedButton(
                        "Logout",
                        on_click=lambda e: (page.session.clear(), page.go("/")),
                        bgcolor="#DC3545",
                        color=ft.Colors.WHITE,
                        width=100,
                    ),
                    ft.Text(
                        f"✅ Logged in as {logged_in_student['username']}",
                        color=ft.Colors.BLACK,
                        size=14,
                    ),
                ]
            else:
                # Header for visitors (not logged in)
                header_buttons = [
                    ft.ElevatedButton(
                        "Login",
                        on_click=lambda e: page.go("/login"),
                        bgcolor="#00A8CC",
                        color=ft.Colors.WHITE,
                        width=100,
                    ),
                    ft.ElevatedButton(
                        "University",
                        on_click=lambda e: page.go("/university"),
                        bgcolor="#6C63FF",
                        color=ft.Colors.WHITE,
                        width=100,
                    ),
                    ft.Text(
                        "Support: +213 556 68 85 75 | elearning@univ-guelma.dz",
                        color=ft.Colors.BLACK,
                        size=14,
                    ),
                ]

            header = ft.Row(
                header_buttons,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )

            header_container = ft.Container(
                content=header,
                padding=5,
                bgcolor="#E6E6E6",
                height=40,
                expand=True
            )

            form_container.content = ft.Column(
                [header_container],
                spacing=0,
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH
            )

            page.views.append(
                ft.View(
                    "/",
                    [form_container],
                    bgcolor="#CBD4E0"
                )
            )

        # ---------------- LOGIN PAGE ----------------
        elif page.route == "/login":
            error_message = ft.Text("", color="#DC3545")

            def login_action(e):
                for student in students_info:
                    if student["username"] == username.value and student["password"] == password.value:
                        page.session.set("student", student)
                        page.go("/")
                        return
                error_message.value = "❌ Invalid username or password"
                page.update()

            username = ft.TextField(
                label="Username",
                autofocus=True,
                color=ft.Colors.BLACK,
                label_style=ft.TextStyle(color=ft.Colors.BLACK),
                border_color="#778DA9",
                focused_border_color="#00A8CC",
                bgcolor="#E6E6E6",
                on_submit=lambda e: password.focus()
            )

            password = ft.TextField(
                label="Password",
                password=True,
                can_reveal_password=True,
                color=ft.Colors.BLACK,
                label_style=ft.TextStyle(color=ft.Colors.BLACK),
                border_color="#778DA9",
                focused_border_color="#00A8CC",
                bgcolor="#E6E6E6",
                on_submit=login_action
            )

            form_container.content = ft.Column(
                [
                    ft.Image(
                        src="University_Logo.png",
                        width=300,
                        height=150,
                        fit=ft.ImageFit.CONTAIN
                    ),
                    ft.Text("CSE2 Student Portal", size=24, weight="bold", color=ft.Colors.BLACK),
                    username,
                    password,
                    ft.Container(
                        ft.ElevatedButton(
                            "Login",
                            on_click=login_action,
                            bgcolor="#E6E6E6",
                            color=ft.Colors.BLACK
                        ),
                        alignment=ft.alignment.top_left
                    ),
                    error_message,
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

            page.views.append(
                ft.View(
                    "/login",
                    [form_container],
                    bgcolor="#CBD4E0",
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        # ---------------- PROFILE PAGE ----------------
        elif page.route == "/profile":
            student = page.session.get("student")
            if not student:
                page.go("/login")
                return

            emoji = "👩" if student.get("gender") == "female" else "👨"

            student_pfp = ft.Image(
                src=student["photo"],
                width=150,
                height=150,
                border_radius=75,
                fit=ft.ImageFit.COVER
            )

            def change_photo(e):
                if e.files:
                    new_photo_path = e.files[0].path
                    student["photo"] = os.path.basename(new_photo_path)
                    student_pfp.src = student["photo"]
                    page.update()
                    with open("Cse2_Students.json", "w") as students_data_file:
                        json.dump(students_info, students_data_file, indent=4)

            file_picker = ft.FilePicker(on_result=change_photo)
            page.overlay.append(file_picker)

            profile_header = ft.Row(
                [
                    ft.ElevatedButton(
                        "Home",
                        on_click=lambda e: page.go("/"),
                        bgcolor="#00A8CC",
                        color=ft.Colors.WHITE,
                        width=100,
                    ),
                    ft.ElevatedButton(
                        "Logout",
                        on_click=lambda e: (page.session.clear(), page.go("/")),
                        bgcolor="#DC3545",
                        color=ft.Colors.WHITE,
                        width=100,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.CENTER
            )

            header_container_profile = ft.Container(
                content=profile_header,
                padding=5,
                bgcolor="#E6E6E6",
                height=40,
                expand=True
            )

            form_container.content = ft.Column(
                [
                    header_container_profile,
                    ft.Text(PROMO_NAME, size=18, color=ft.Colors.BLACK),
                    student_pfp,
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Change Profile Picture",
                                on_click=lambda e: file_picker.pick_files(
                                    allow_multiple=False,
                                    allowed_extensions=["png", "jpg", "jpeg"]
                                ),
                                bgcolor="#E6E6E6",
                                color=ft.Colors.BLACK
                            ),
                            ft.ElevatedButton(
                                "Reset to Default",
                                on_click=lambda e: reset_pfp(student, student_pfp, students_info, page),
                                bgcolor="#E6E6E6",
                                color=ft.Colors.BLACK
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(f"{student['full_name']} {emoji}", size=22, weight="bold", color=ft.Colors.BLACK),
                    ft.Text(f"Major: {PROMO_MAJOR}", color=ft.Colors.BLACK),
                    ft.Text(f"University: {UNIVERSITY_NAME}", color=ft.Colors.BLACK),
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

            page.views.append(
                ft.View(
                    "/profile",
                    [form_container],
                    bgcolor="#CBD4E0",
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        # ---------------- UNIVERSITY PAGE ----------------
        elif page.route == "/university":
            # Just a placeholder for now
            form_container.content = ft.Column(
                [
                    ft.Text("🏫 Welcome to the University Page", size=22, weight="bold"),
                    ft.Text("This is where university details will appear.", size=16),
                    ft.ElevatedButton(
                        "Back to Home",
                        on_click=lambda e: page.go("/"),
                        bgcolor="#00A8CC",
                        color=ft.Colors.WHITE
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )

            page.views.append(
                ft.View(
                    "/university",
                    [form_container],
                    bgcolor="#CBD4E0",
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        page.update()

    # Handle routes
    page.on_route_change = route_change
    page.go("/")

# Run the app
ft.app(target=main, view=ft.WEB_BROWSER, assets_dir="User_Data/assets")
