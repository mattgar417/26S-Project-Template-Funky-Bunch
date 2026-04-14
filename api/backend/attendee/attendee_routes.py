from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for Attendee routes
attendee_routes = Blueprint("attendee_routes", __name__)

# GET /attendee/attendees/<id>/feed
# Returns personalized event feed based on attendee's interests + location [Sarah-1]
@attendee_routes.route("/attendees/<int:attendee_id>/feed", methods=["GET"])
def get_attendee_feed(attendee_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT e.Event_ID, e.Name, e.Description, e.Date, e.Location
            FROM Events e
            JOIN Attendee_Interests ai ON e.Focus_Area = ai.Interest
            JOIN Attendees a ON ai.Attendee_ID = a.Attendee_ID
            WHERE a.Attendee_ID = %s AND e.Location = a.Location
            ORDER BY e.Date ASC
        """
        cursor.execute(query, (attendee_id,))
        events = cursor.fetchall()
        return jsonify(events), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_attendee_feed: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        
# GET /attendee/attendees/<id>/rsvps
# Returns all events the attendee has RSVPed to [Sarah-2]
@attendee_routes.route("/attendees/<int:attendee_id>/rsvps", methods=["GET"])
def get_attendee_rsvps(attendee_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT e.Event_ID, e.Name, e.Description, e.Date, e.Location, a.Status
            FROM Events e
            JOIN Attends a ON e.Event_ID = a.Event_ID
            WHERE a.AttendeeID = %s
            ORDER BY e.Date ASC
        """
        cursor.execute(query, (attendee_id,))
        events = cursor.fetchall()
        return jsonify(events), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_attendee_rsvps: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

