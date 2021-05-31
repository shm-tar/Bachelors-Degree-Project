def test_testing_config(app):
    assert app.config['UPLOAD_PATH'] == 'static/uploads'
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///test_site.db'
