from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for Attendee routes
owner_routes = Blueprint("owner_routes", __name__)
