import flet as ft
import json
import os

# Container for content
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

    # Load promo info
    with open("Promo_Info.json", "r") as promo_data_file:
        promo_info = json.load(promo_data_file)
        PROMO_NAME = promo_info["promo_name"]
        PROMO_MAJOR = promo_info["major"]
        UNIVERSITY_NAME = promo_info["university"]
        PROMO_YEAR = promo_info["year"]

    # Load students data
    with open("Cse2_Students.json", "r") as students_data_file:
        students_info = json.load(students_data_file)

    DEFAULT_MALE = "male_avatar.png"
    DEFAULT_FEMALE = "female_avatar.png"

    # Assign default images (ensure filename only for web)
    for s in students_info:
        if not s.get("photo"):
            s["photo"] = DEFAULT_FEMALE if s.get("gender") == "female" else DEFAULT_MALE
        else:
            s["photo"] = os.path.basename(s["photo"])

    # ---------------- FUNCTION TO RESET PFP ----------------
    def reset_pfp(student, student_pfp, students_info, page):
        default_photo = DEFAULT_FEMALE if student.get("gender") == "female" else DEFAULT_MALE
        student["photo"] = default_photo
        student_pfp.src = default_photo
        page.update()
        # Save updated student data
        with open("Cse2_Students.json", "w") as students_data_file:
            json.dump(students_info, students_data_file, indent=4)

    # ---------------- Helper to check login ----------------
    def is_logged_in():
        return page.session.get("student") is not None

    # ---------------- Header factory (now supports status & home button) ----------------
    def make_header(title_text, show_status=False, full_width=False):
        # Left: logo + title
        left = ft.Row(
            [
                ft.Image(src="University_Logo.png", width=32, height=32, fit=ft.ImageFit.CONTAIN),
                ft.Text(title_text, size=18, weight="bold", color="#1B263B"),
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        )

        # Right: (optional) Home button + status
        right_items = []
        if show_status:
            # Home button (goes to / but does not log out)
            home_btn = ft.ElevatedButton(
                "Home",
                on_click=lambda e: page.go("/"),
                bgcolor="#00A8CC",
                color=ft.Colors.WHITE,
                width=90,
            )
            right_items.append(home_btn)

            # Login status text
            student = page.session.get("student")
            if student:
                status = ft.Text(f"✅ Logged in as: {student.get('username')}", color="#198754", size=12)
            else:
                status = ft.Text("❌ Not logged in", color="#DC3545", size=12)
            right_items.append(status)

        right = ft.Row(
            right_items,
            alignment=ft.MainAxisAlignment.END,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8
        )

        # Combine into header row
        header_row = ft.Row(
            [left, right],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return ft.Container(
            content=header_row,
            padding=8,
            bgcolor="#E6E6E6",
            border_radius=ft.border_radius.all(10) if not full_width else 0,
            expand=full_width
        )

    # ---------------- ROUTES ----------------
    def route_change(e):
        page.views.clear()

        # ---------------- HOME PAGE ----------------
        if page.route == "/":
            form_container.content = ft.Column(
                [
                    make_header("CSE2 Student Portal", full_width=True),
                    ft.Text("Welcome to CSE2 Student Portal", size=22, weight="bold", color="#1B263B"),
                    ft.Image(src="University_Logo.png", width=280, height=150, fit=ft.ImageFit.CONTAIN),
                    ft.Row(
                        [
                            ft.ElevatedButton("Login", on_click=lambda e: page.go("/login"), bgcolor="#00A8CC", color=ft.Colors.WHITE),
                            ft.ElevatedButton("Courses", on_click=lambda e: page.go("/courses"), bgcolor="#007BFF", color=ft.Colors.WHITE),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text("Support: +213 556 68 85 75 | elearning@univ-guelma.dz", color="#2E2E2E", size=13),
                ],
                spacing=15,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

            page.views.append(
                ft.View("/", [form_container], bgcolor="#CBD4E0")
            )

        # ---------------- LOGIN PAGE ----------------
        elif page.route == "/login":
            error_message = ft.Text("", color="#DC3545")

            def login_action(e):
                for student in students_info:
                    if student["username"] == username.value and student["password"] == password.value:
                        page.session.set("student", student)
                        page.go("/profile")
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
                    make_header("Login Page", show_status=True),
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

            # Logout action that clears session and navigates to login
            def logout_action(e):
                page.session.remove("student")
                page.go("/login")

            form_container.content = ft.Column(
                [
                    make_header("My Profile", show_status=True),
                    ft.Text(PROMO_NAME, size=18, color=ft.Colors.BLACK),
                    student_pfp,
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Change Picture",
                                on_click=lambda e: file_picker.pick_files(
                                    allow_multiple=False,
                                    allowed_extensions=["png", "jpg", "jpeg"]
                                ),
                                bgcolor="#E6E6E6",
                                color=ft.Colors.BLACK
                            ),
                            ft.ElevatedButton(
                                "Reset",
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
                    ft.ElevatedButton("Logout", on_click=logout_action, bgcolor="#DC3545", color=ft.Colors.WHITE)
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

        page.update()

    # Connect router
    page.on_route_change = route_change
    page.go("/")

# Run the app in web browser with assets_dir pointing to your assets folder
ft.app(target=main, view=ft.WEB_BROWSER, assets_dir="User_Data/assets")
