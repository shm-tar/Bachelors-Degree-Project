class TestConfig:
    # print(os.urandom(16).hex())
    SECRET_KEY = '6c2396e3492c2b4ac74bd0021e7bd25f'

    # SQLite database path
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_site.db'

    # Max CV file size ~4 MBs
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024

    # The only supported CV file extensions
    UPLOAD_EXTENSIONS = ['.doc', '.docx', '.pdf']

    # Uploads folder
    UPLOAD_PATH = 'static/uploads'
