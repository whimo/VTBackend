from app import app

if __name__ == '__main__':
    from config import host, port, debug
    app.run(host=host, port=port, debug=debug)
