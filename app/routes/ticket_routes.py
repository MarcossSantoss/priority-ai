from flask import Blueprint, render_template, request, jsonify
from app.services.ai_service import get_priority
from app.database.db import save_ticket, get_tickets

ticket_bp = Blueprint("ticket", __name__)


@ticket_bp.route("/")
def home():
    return render_template("index.html")


@ticket_bp.route("/ticket", methods=["POST"])
def create_ticket():
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")

    priority = get_priority(description)

    save_ticket(title, description, priority)

    return jsonify({"priority": priority})


@ticket_bp.route("/tickets", methods=["GET"])
def list_tickets():
    tickets = get_tickets()

    result = []
    for t in tickets:
        result.append({
            "id": t[0],
            "title": t[1],
            "description": t[2],
            "priority": t[3]
        })

    return jsonify(result)
