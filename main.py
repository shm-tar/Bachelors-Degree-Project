from cvreviewer import create_app

app = create_app()  # already uses Config by default

if __name__ == '__main__':
    app.run(debug=False)
