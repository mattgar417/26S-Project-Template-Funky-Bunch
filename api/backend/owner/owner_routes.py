from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for Venue routes
venue_routes = Blueprint("venue_routes", __name__)

# --- 1. GET ALL VENUES ---
# Returns all venues and their owner details for administrative overview
@venue_routes.route("/venues", methods=["GET"])
def get_venues():
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT v.*, o.FName AS OwnerFirstName 
            FROM Venue v 
            JOIN Owner o ON v.OwnerID = o.OwnerID
        """
        cursor.execute(query)
        venues = cursor.fetchall()
        return jsonify(venues), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_venues: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# --- 2. GET ALL REQUESTS FOR A SPECIFIC VENUE ---
# Returns booking requests for a specific venue [Jason-1]
@venue_routes.route("/venues/<int:venue_id>/requests", methods=["GET"])
def get_venue_requests(venue_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT
                r.RequestID,
                r.RequestName,
                r.Status,
                r.Date,
                o.OrganizerID,
                o.FName AS OrganizerFirstName,
                o.LName AS OrganizerLastName
            FROM Requests r
            JOIN Organizer o ON r.OrganizerID = o.OrganizerID
            WHERE r.VenueID = %s
            ORDER BY r.RequestID DESC
        """
        cursor.execute(query, (venue_id,))
        requests_data = cursor.fetchall()
        return jsonify(requests_data), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_venue_requests: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# --- 3. UPDATE REQUEST STATUS ---
# Allows for the approval or rejection of specific venue requests [Jason-5]
@venue_routes.route("/venues/<int:venue_id>/requests/<int:request_id>", methods=["PUT"])
def update_venue_request_status(venue_id, request_id):
    db = get_db()
    cursor = db.cursor()
    try:
        data = request.get_json()
        status = data.get("status")

        if not status:
            return jsonify({"error": "Status is required"}), 400

        query = "UPDATE Requests SET Status = %s WHERE RequestID = %s AND VenueID = %s"
        cursor.execute(query, (status, request_id, venue_id))
        db.commit() 
        return jsonify({"message": "Request status updated successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in update_venue_request_status: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# --- 4. VENUE CALENDAR ---
# Returns a schedule of events hosted at the venue to prevent double-booking [Jason-2]
@venue_routes.route("/venues/<int:venue_id>/calendar", methods=["GET"])
def get_venue_calendar(venue_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT e.Name, e.Date 
            FROM Hosts h 
            JOIN Event e ON h.EventID = e.EventID 
            WHERE h.VenueID = %s
            ORDER BY e.Date ASC
        """
        cursor.execute(query, (venue_id,))
        calendar_data = cursor.fetchall()
        return jsonify(calendar_data), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_venue_calendar: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# --- 5. VENUE REVENUE ---
# Calculates revenue trends for the venue based on approved bookings [Jason-6]
@venue_routes.route("/venues/<int:venue_id>/revenue", methods=["GET"])
def get_venue_revenue(venue_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT 
                DATE_FORMAT(Date, '%Y-%m-%d') as week, 
                COUNT(RequestID) * 500 as amount
            FROM Requests 
            WHERE VenueID = %s AND Status = 'Approved'
            GROUP BY week 
            ORDER BY week ASC
        """
        cursor.execute(query, (venue_id,))
        revenue_data = cursor.fetchall()
        return jsonify(revenue_data), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_venue_revenue: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# --- 6. GET ORGANIZER HISTORY ---
# Provides a profile and history of organizers to ensure reliability [Jason-4]
@venue_routes.route("/organizers/<int:org_id>/history", methods=["GET"])
def get_organizer_history(org_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        # Get Organizer profile info
        cursor.execute("""
            SELECT FName AS FirstName, LName AS LastName, Email 
            FROM Organizer 
            WHERE OrganizerID = %s
        """, (org_id,))
        organizer = cursor.fetchone()

        # Get their request history
        cursor.execute("""
            SELECT RequestName, Status, Date 
            FROM Requests 
            WHERE OrganizerID = %s 
            ORDER BY Date DESC
        """, (org_id,))
        history = cursor.fetchall()

        return jsonify({
            "organizer": organizer if organizer else {"FirstName": "Unknown", "LastName": "", "Email": "N/A"},
            "history": history
        }), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_organizer_history: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()