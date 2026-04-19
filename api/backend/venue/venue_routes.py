from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

venue_routes = Blueprint("venue_routes", __name__)

# --- 1. GET ALL VENUES ---
@venue_routes.route("/venues", methods=["GET"])
def get_venues():
    cursor = get_db().cursor(dictionary=True)
    try:
        query = "SELECT v.*, o.FName as OwnerFirstName FROM Venue v JOIN Owner o ON v.OwnerID = o.OwnerID"
        cursor.execute(query)
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# --- 2. GET ALL REQUESTS FOR A SPECIFIC VENUE ---
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
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# --- 3. UPDATE REQUEST STATUS (Confirm/Approve) ---
@venue_routes.route("/venues/<int:venue_id>/requests/<int:request_id>", methods=["PUT"])
def update_venue_request_status(venue_id, request_id):
    db = get_db()
    cursor = db.cursor()
    try:
        data = request.get_json()
        status = data.get("status")
        cursor.execute(
            "UPDATE Requests SET Status = %s WHERE RequestID = %s AND VenueID = %s",
            (status, request_id, venue_id)
        )
        db.commit() 
        return jsonify({"message": "Success"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# --- 4. VENUE CALENDAR ---
@venue_routes.route("/venues/<int:venue_id>/calendar", methods=["GET"])
def get_venue_calendar(venue_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = "SELECT e.Name, e.Date FROM Hosts h JOIN Event e ON h.EventID = e.EventID WHERE h.VenueID = %s"
        cursor.execute(query, (venue_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# --- 5. VENUE REVENUE ---
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
        data = cursor.fetchall()
        return jsonify(data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# --- 6. GET SPECIFIC ORGANIZER PROFILE & HISTORY ---
@venue_routes.route("/organizers/<int:org_id>/history", methods=["GET"])
def get_organizer_history(org_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        # 1. Get basic Organizer info
        cursor.execute("SELECT FName as FirstName, LName as LastName, Email FROM Organizer WHERE OrganizerID = %s", (org_id,))
        organizer = cursor.fetchone()

        # 2. Get their history of requests at your venues
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
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
<<<<<<< HEAD
        cursor.close()

@venue_routes.route("/organizers/<int:org_id>/history", methods=["GET"])
def get_organizer_history(org_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = """
            SELECT e.Date, e.Name AS EventName, e.Size AS Attendance
            FROM Requests r
            JOIN Event e ON r.RequestName = e.Name
            WHERE r.OrganizerID = %s AND r.Status = 'Approved'
            ORDER BY e.Date DESC
        """
        cursor.execute(query, (org_id,))
        return jsonify(cursor.fetchall()), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

@venue_routes.route('/venues/<venue_id>/revenue', methods=['GET'])
def get_venue_revenue(venue_id):
    # This query sums up the 'Price' of all 'Approved' requests for the venue
    # It groups them by week so Streamlit can draw the line chart
    query = f'''
        SELECT 
            CONCAT('Week ', WEEK(Date)) as week,
            SUM(Price) as amount
        FROM Bookings
        WHERE VenueID = {venue_id} AND Status = 'Approved'
        GROUP BY week
        ORDER BY week ASC
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_names = [column[0] for column in cursor.description]
    data = [dict(zip(column_names, row)) for row in cursor.fetchall()]
    
    return jsonify(data)
=======
        cursor.close()
>>>>>>> 91b855d (Merge remote changes)
