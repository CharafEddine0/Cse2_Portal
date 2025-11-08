import flet as ft
import json
import os
# Container for content
form_container = ft.Container(
    width=400,
    height=500,
    padding=20,
    border_radius=14,
    bgcolor="#FFFFFF"  # Snow white container
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
            # Only use filename to ensure web loads from assets_dir
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
    # ---------------- ROUTES ----------------
    def route_change(e):
        page.views.clear()
        # Home Page
        if page.route == "/":
            header = ft.Row(
                [
                    ft.ElevatedButton(
                        "Login",
                        on_click=lambda e: page.go("/login"),
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
                    ft.Text(
                        "Support: +213 556 68 85 75 | elearning@univ-guelma.dz",
                        color=ft.Colors.BLACK,
                        size=14,
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )

            header_container = ft.Container(
                content=header,
                padding=10,
                bgcolor="#E6E6E6",
                height=60
            )

            background_container = ft.Container(
                expand=True,
                image=ft.Image(
                    src="University_Background.png",
                    fit=ft.ImageFit.COVER
                )
            )

            form_container.content = ft.Column(
                [
                    header_container,
                    background_container
                ],
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
        if page.route == "/login":

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

            # Container content for login (Login button top-left)
            form_container.content = ft.Column(
                [
                    ft.Image(
                        src="University_Logo.png",  # filename in assets_dir
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
                src=student["photo"],  # filename only, loads from assets_dir
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

            form_container.content = ft.Column(
                [
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
                    # Logout stays centered
                    ft.ElevatedButton(
                        "Logout",
                        on_click=lambda e: page.go("/login"),
                        bgcolor="#E6E6E6",
                        color=ft.Colors.BLACK
                    )
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

    page.on_route_change = route_change
    page.go("/")

# Run the app in web browser with assets_dir pointing to your assets folder
ft.app(target=main, view=ft.WEB_BROWSER, assets_dir="User_Data/assets")
