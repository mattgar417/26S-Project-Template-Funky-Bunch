from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for Owner routes
owner_routes = Blueprint("owner_routes", __name__)

# Returns a list of all event requests with details so the owner can make informed decisions [Jason-1]
@owner_routes.route("/owners/<int:owner_id>/requests", methods=["GET"])
def get_owner_requests(owner_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT 
                r.RequestID, 
                r.RequestName, 
                r.Status, 
                e.Date, 
                e.Size, 
                o.FName AS OrganizerFirstName, 
                o.LName AS OrganizerLastName
            FROM Requests r
            JOIN Organizer o ON r.OrganizerID = o.OrganizerID
            LEFT JOIN Event e ON r.RequestName LIKE CONCAT('%%', e.Name, '%%')
            JOIN Venue v ON r.VenueID = v.VenueID
            WHERE v.OwnerID = %s
        """
        cursor.execute(query, (owner_id,))
        requests = cursor.fetchall()
        return jsonify(requests), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_owner_requests: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()