from src.app import app

@app.route('/shops')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)
