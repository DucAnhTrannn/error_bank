import sqlite3

# Kết nối tới cơ sở dữ liệu SQLite
conn = sqlite3.connect('errors.db')
cursor = conn.cursor()

# Kiểm tra nếu bảng tạm tồn tại và xóa nó
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='_alembic_tmp_error';")
if cursor.fetchone():
    print("Dropping temporary table '_alembic_tmp_error'.")
    cursor.execute('DROP TABLE IF EXISTS _alembic_tmp_error')

# Đóng kết nối
conn.commit()
conn.close()

print("Temporary tables removed successfully.")
