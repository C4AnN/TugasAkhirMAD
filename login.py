import mysql.connector
from mysql.connector import Error
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# login.py

def login_admin(username, password):
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
            
            # Hash password yang diinput pengguna
            hashed_password = hash_password(password)

            # Query untuk memeriksa username, password, dan role
            query = "SELECT role FROM tbl_admin WHERE username = %s AND password = %s"
            cursor.execute(query, (username, hashed_password))
            result = cursor.fetchone()
            
            if result:
                # Mengembalikan role pengguna jika login berhasil
                return result[0]
            else:
                return None  # Login gagal

    except Error as e:
        print("Error saat login:", e)
        return None

    finally:
        if koneksi_db.is_connected():
            cursor.close()
            koneksi_db.close()

