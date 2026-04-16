from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for Event routes
organizer_routes = Blueprint("organizer_routes", __name__)

# GET /organizer/organizers/<id>
# Return organizer profile with reliability stats such as total requests and approval count
@organizer_routes.route("/organizers/<int:organizer_id>", methods=["GET"])
def get_organizer_by_id(organizer_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = '''
            SELECT COUNT (r.RequestID) as TotalRequests, SUM(CASE WHEN r.Status = 'Approved' THEN 1 ELSE 0 END) AS ApprovedCount, o.OrganizerID, o.FName, o.LName, o.Email, o.Location
            FROM Organizer o JOIN requests r ON o.OrganizerID == r.OrganizerID
            WHERE o.OrganizerID = %s
            GROUP BY o.OrganizerID, o.FName, o.LName, o.Email, o.Location
        '''
        cursor.execute(query, (organizer_id,))
        organizer = cursor.fetchall()
        return jsonify(organizer), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_organizer_by_id: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()