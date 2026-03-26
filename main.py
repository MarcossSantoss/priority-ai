from flask import Flask
from app.routes.ticket_routes import ticket_bp
from app.database.db import create_table

app = Flask(__name__)

app.register_blueprint(ticket_bp)

if __name__ == "__main__":
    create_table()
    app.run(debug=True)
