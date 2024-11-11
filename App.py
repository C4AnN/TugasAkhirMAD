import flet as ft
import re
from login import login_admin
from register import register_admin

def main(page: ft.Page):
    page.title = "Aplikasi Penyewaan Mobil"
    page.window_width = 375
    page.window_height = 612
    page.window_resizable = True
    page.window_maximizable = True
    page.window_minimizable = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT  # Default ke mode terang

    page.add(
        ft.Text("Selamat Datang di Aplikasi Penyewaan Mobil", size=15, weight=ft.FontWeight.BOLD)
    )

    images = ft.Row(expand=1, wrap=False, scroll="always")
    page.add(images)
    
    # Menambahkan gambar secara dinamis
    for i in range(1, 4):  # Loop untuk menambahkan gambar dari Asset folder
        images.controls.append(
            ft.Image(
                src=f"Asset/{i}.png",  # Gunakan f-string untuk nama file
                width=200,
                height=200,
                fit=ft.ImageFit.CONTAIN,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            )
        )
    page.update()

    # Variabel untuk melacak status login dan registrasi
    is_logged_in = False
    in_registration = False

    # Fungsi untuk memperbarui AppBar sesuai status login atau registrasi
    def update_appbar():
        page.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.CAR_RENTAL),
            leading_width=50,
            title=ft.Text("Sistem Penyewaan Mobil", size=20, weight=ft.FontWeight.BOLD),
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click=toggle_theme_mode),
                ft.IconButton(ft.icons.ARROW_BACK, on_click=go_back) if in_registration else None,
                ft.IconButton(ft.icons.LOGOUT_OUTLINED, on_click=handle_logout) if is_logged_in else None
            ]
        )
        page.appbar.actions = [action for action in page.appbar.actions if action is not None]
        page.update()

    # Fungsi untuk menangani logout
    def handle_logout(e):
        nonlocal is_logged_in
        is_logged_in = False
        page.clean()
        main(page)

    # Fungsi untuk kembali ke halaman utama dari halaman registrasi
    def go_back(e):
        nonlocal in_registration
        in_registration = False
        page.clean()
        main(page)

    # Fungsi untuk mengganti mode terang/gelap
    def toggle_theme_mode(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        page.update()

    # Fungsi untuk menangani login
    def handle_login(e):
        nonlocal is_logged_in
        username = username_field.value
        password = password_field.value

        role = login_admin(username, password)
        if role:
            is_logged_in = True
            page.clean()
            
            if role == "admin":
                main_menu(page, role="admin")
            elif role == "pemilik":
                main_menu(page, role="pemilik")

            update_appbar()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Login gagal. Username atau password salah."))
            page.snack_bar.open = True
            page.update()

    # Fungsi untuk membuka halaman registrasi
    def open_registration(e):
        nonlocal in_registration
        in_registration = True
        page.clean()
        registration_page(page)
        update_appbar()

    # Form login dengan fitur can_reveal_password
    username_field = ft.TextField(label="Username", width=350)
    password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=350)
    login_button = ft.ElevatedButton("Login", on_click=handle_login, width=350)
    register_button = ft.TextButton("Belum punya akun? Registrasi", on_click=open_registration)

    page.add(
        ft.Column(
            [
                username_field,
                password_field,
                login_button,
                register_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )
    update_appbar()

# Halaman registrasi dengan fitur can_reveal_password
def registration_page(page: ft.Page):
    def handle_register(e):
        nama_admin = nama_admin_field.value
        email = email_field.value
        username = username_field.value
        password = password_field.value
        role = role_field.value

        if not nama_admin or not email or not username or not password:
            page.snack_bar = ft.SnackBar(ft.Text("Semua field harus diisi."))
            page.snack_bar.open = True
            page.update()
            return
        
        # Validasi password: minimal 8 karakter, mengandung huruf kapital, angka, dan simbol
        if not re.fullmatch(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            page.snack_bar = ft.SnackBar(
                ft.Text("Password minimal 8 karakter dan harus mengandung huruf kapital, angka, dan simbol.")
            )
            page.snack_bar.open = True
            page.update()
            return

        # Validasi untuk format email harus mengandung "@gmail.com"
        if not email.endswith("@gmail.com"):
            page.snack_bar = ft.SnackBar(ft.Text("Email harus berformat @gmail.com."))
            page.snack_bar.open = True
            page.update()
            return

        if register_admin(nama_admin, email, username, password, role):
            page.snack_bar = ft.SnackBar(ft.Text("Registrasi berhasil! Silakan login."))
            page.snack_bar.open = True
            page.clean()
            main(page)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Registrasi gagal. Username atau email sudah terdaftar."))
            page.snack_bar.open = True
        page.update()

    # Field input registrasi dengan can_reveal_password
    nama_admin_field = ft.TextField(label="Nama Lengkap", width=350)
    email_field = ft.TextField(label="Email", width=350)
    username_field = ft.TextField(label="Username", width=350)
    password_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=350)
    
    # Dropdown untuk memilih role
    role_field = ft.Dropdown(
        label="Role",
        options=[
            ft.dropdown.Option("admin"),
            ft.dropdown.Option("pemilik")
        ],
        width=350,
        value="admin"
    )

    register_button = ft.ElevatedButton("Daftar", on_click=handle_register, width=350)

    page.add(
        ft.Column(
            [
                ft.Text("Registrasi Akun Baru", size=20, weight=ft.FontWeight.BOLD),
                nama_admin_field,
                email_field,
                username_field,
                password_field,
                role_field,
                register_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )

# Menu utama setelah login
def main_menu(page: ft.Page, role="admin"):
    if role == "admin":
        page.add(
            ft.Text("Selamat datang di dashboard, Admin di aplikasi penyewaan mobil!", size=20, weight=ft.FontWeight.BOLD)
        )
    elif role == "pemilik":
        page.add(
            ft.Text("Selamat datang di dashboard pemilik, Pemilik di aplikasi penyewaan mobil!", size=20, weight=ft.FontWeight.BOLD)
        )

# Menjalankan aplikasi
if __name__ == "__main__":
    ft.app(target=main)
