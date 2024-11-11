import mysql.connector
from mysql.connector import Error
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# register.py

def register_admin(nama_admin, email, username, password, role):  # Tambahkan parameter role
    try:
        koneksi_db = mysql.connector.connect(
            host="localhost",
            user="root",
            port=3308,
            password="",
            database="penyewaan"
        )

        if koneksi_db.is_connected():
            cursor = koneksi_db.cursor()

            # Cek apakah username atau email sudah terdaftar
            cursor.execute("SELECT * FROM tbl_admin WHERE username = %s OR email = %s", (username, email))
            result = cursor.fetchone()
            if result:
                return False  # Username atau email sudah terdaftar

            # Hash password sebelum menyimpan ke database
            hashed_password = hash_password(password)
            
            # Tambahkan data admin/pemilik baru dengan password yang di-hash dan role
            query = "INSERT INTO tbl_admin (nama_admin, email, username, password, role) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (nama_admin, email, username, hashed_password, role))
            koneksi_db.commit()
            return True  # Registrasi berhasil

    except Error as e:
        print("Error saat registrasi:", e)
        return False

    finally:
        if koneksi_db.is_connected():
            cursor.close()
            koneksi_db.close()
