import os
from api import create_app  # Import đúng module create_app từ thư mục library

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api', 'config.py')
    app = create_app(config_path)  # Truyền đường dẫn đầy đủ đến file config.py
    app.run(debug=True)
