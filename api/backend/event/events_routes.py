from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for Event routes
event_routes = Blueprint("event_routes", __name__)

# GET /event/events
# Return a list of all events; supports query params for category, date, and location filters
@event_routes.route("/events", methods=["GET"])
def get_events():
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()
        category = data.get("category")
        date = data.get("date")
        location = data.get("location")

        query = '''
            SELECT e.EventID, e.Name. e.Date, e. Location, e.Description, e.Size, e.Category
            FROM Event e
        '''
        params = []

        if category:
            query += " AND Category = %s"
            params.append(category)
        if date:
            query += " AND DATE(Date) = %s"
            params.append(date)
        if location:
            query += " AND Location LIKE %s"
            params.append(f"%{location}%")

        cursor.execute(query, params)
        events = cursor.fetchall()
        return jsonify(events), 200
    except Error as e:
        current_app.logger.error(f"Database error in get_events: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# POST /event/events/
# Post a new event visible to potential attendees
@event_routes.route("/events/<int:event_id>", methods=["POST"])
def post_event():
    cursor = get_db().cursor()
    try:
        data = request.get_json()
        event_id = data.get("event_id")
        name = data.get("name")
        date = data.get("date")
        location = data.get("location")
        description = data.get("description")
        size = data.get("size")
        category = data.get("category")

        cursor.execute("SELECT * FROM Event WHERE EventID = %s", (event_id))
        existing_event = cursor.fetchone()

        if existing_event:
            cursor.execute("UPDATE Event (Name, Date, Location, Description, Size, Category) VALUES (%s, %s, %s, %s, %s, %s) WHERE EventID = %s", (name, date, location, description, size, category, event_id))
        else:
            cursor.execute("INSERT INTO Event (EventID, Name, Date, Location, Description, Size, Category) VALUES (%s, %s, %s, %s, %s, %s, %s)", (event_id, name, date, location, description, size, category))
        
        get_db.commit()
        return jsonify({"message": "Event updates successful"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in post_event: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# GET /event/events/<id>
# Return full event detail: date/time, venue, description, performer info, price, and size 
@event_routes.route("/events/<int:event_id>", methods=["GET"])
def get_event_id(event_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = '''
            SELECT e.EventID, e.Name, e.Date, e.Location, e.Description, e.Size, e.Category
            FROM Event e
            WHERE e.EventID = %s
        '''
        cursor.execute(query, (event_id,))
        events = cursor.fetchall()
        return jsonify(events), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_event_id: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# PUT /event/events/<id>
# Edit an existing event's details such as title, date, and descriptio
@event_routes.route("/events/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    cursor = get_db().cursor()
    try:
        data = request.get_json()

        cursor.execute("SELECT EventId FROM Event WHERE EventId = %s", (event_id,))
        if not cursor.fetchone():
            return jsonify({"error": "review not found"}), 404
        
        allowed_fields = ["Name", "Date", "Location", "Description", "Size", "Category"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        params.append(event_id)
        query = f"UPDATE Event SET {', '.join(update_fields)} WHERE EventId = %s"
        cursor.execute(query, params)

        get_db().commit()
        return jsonify({"message": "Event updates successful"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in update_event: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# DELETE /event/events/<id>
# Delete or unpublish an event
@event_routes.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    cursor = get_db().cursor()
    try:
        cursor.execute("SELECT EventID FROM Event WHERE EventID = %s", (event_id))
        if not cursor.fetchone():
            return jsonify({"error": "Review not found"}), 404

        cursor.execute("DELETE FROM Event WHERE EventID = %s", (event_id))
        get_db.commit()
        return jsonify({"message": "Event deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in delete_event: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# GET /event/events/<id>/attendees
# Returns list and count of confirmed attendees for an event  
@event_routes.route("/events/<int:event_id>/attendees", methods=["GET"])
def get_event_attendees(event_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = '''
            SELECT COUNT(a.AttendeeID) AS TotalAttendees, a.FName, a.LName
            FROM Attendee a JOIN Attends ae ON a.AttendeeID == ae.AttendeeID
            FROM Attends ae JOIN Event e ON ae.AttendeeID == e.EventsID
            WHERE ae.Status = 'Confirmed'
            GROUP BY a.FName, a.LName
        '''
        cursor.execute(query, (event_id,))
        events = cursor.fetchall()
        return jsonify(events), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_event_attendees: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# GET /event/events/<id>/reviews
# Return all reviews and average rating for a specific event
@event_routes.route("/events/<int:event_id>/reviews", methods=["GET"])
def get_event_reviews(event_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = '''
            SELECT AVG(r.Rating), r.ReviewID, r.Rating, r.Comment
            FROM Events e JOIN Reviews r ON e.EventID == r.EventID
            GROUP BY r.ReviewID, r.Rating, r.Comment
        '''
        cursor.execute(query, (event_id,))
        events = cursor.fetchall()
        return jsonify(events), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_event_reviews: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# POST /event/events/<id>/reviews
# Submit a rating and written review for an attended event
@event_routes.route("/events/<int:event_id>/reviews", methods=["POST"])
def post_event_review(event_id):
    cursor = get_db().cursor()
    try:
        data = request.get_json()
        attendee_id = data.get("attendee_id")
        rating = data.get("rating")
        comment = data.get("comment")

        cursor.execute("INSERT INTO Review (EventID, AttendeeID, Rating, Comment) VALUES (%s, %s, %s, %s)", (event_id, attendee_id, rating, comment),)
        
        get_db.commit()
        return jsonify({"message": "Review updated successful"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in post_event: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# GET /event/events/<id>/matched-users
# Return attendees whose interests match the event's category, ranked by relevance for amplification
@event_routes.route("/events/<int:event_id>/matched-users", methods=["GET"])
def get_event_matches(event_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        query = '''
            SELECT a.AttendeeID, a.FName, a.LName
            FROM Attendee a JOIN Interests i ON a.AttendeeID == i.AttendeeID
            FROM Interests i JOIN Event e ON i.EventID == e.EventID
            ORDER BY i.Interest
        '''
        cursor.execute(query, (event_id,))
        events = cursor.fetchall()
        return jsonify(events), 200
    except Error as e:
        current_app.logger.error(f'Database error in get_event_matches: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()