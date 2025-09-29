import os
import shutil
import glob
import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db.sqlite3")

def remove_db():
    if os.path.exists(DB_PATH):
        print("🗑 Menghapus database lama...")
        os.remove(DB_PATH)

def remove_migrations():
    print("🗑 Menghapus file migrasi lama...")
    apps = [d for d in os.listdir(BASE_DIR) if os.path.isdir(d)]
    for app in apps:
        migrations_path = os.path.join(BASE_DIR, app, "migrations")
        if os.path.exists(migrations_path):
            for file in glob.glob(os.path.join(migrations_path, "[0-9]*.py")):
                os.remove(file)
            for file in glob.glob(os.path.join(migrations_path, "*.pyc")):
                os.remove(file)

def run_migrate():
    print("⚙️ Membuat migrasi baru...")
    os.system("python manage.py makemigrations")
    os.system("python manage.py migrate")

if __name__ == "__main__":
    remove_db()
    remove_migrations()
    run_migrate()
    print("✅ Database berhasil direset!")
