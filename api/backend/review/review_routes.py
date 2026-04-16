from flask import Blueprint, jsonify, request, current_app
from backend.db_connection import get_db
from mysql.connector import Error

# Create a Blueprint for Event routes
review_routes = Blueprint("review_routes", __name__)

# GET /review/reviews/<id>
# Edit an existing review's rating or comment tex
@review_routes.route("/reviews/<int:review_id>", methods=["PUT"])
def update_reviews(review_id):
    cursor = get_db().cursor(dictionary=True)
    try:
        data = request.get_json()

        cursor.execute("SELECT ReviewId FROM Review WHERE ReviewId = %s", (review_id,))
        if not cursor.fetchone():
            return jsonify({"error": "review not found"}), 404

        allowed_fields = ["Rating", "Comment"]
        update_fields = [f"{f} = %s" for f in allowed_fields if f in data]
        params = [data[f] for f in allowed_fields if f in data]

        if not update_fields:
            return jsonify({"error": "No valid fields to update"}), 400

        params.append(review_id)
        query = f"UPDATE Review SET {', '.join(update_fields)} WHERE ReviewId = %s"
        cursor.execute(query, params)
        get_db().commit()

        return jsonify({"message": "reviews updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()

# DELETE /review/reviews/<id>
# Delete a review the attendee submitted
@review_routes.route("/reviews/<int:review_id>", methods=["DELETE"])
def delete_review(review_id):
    cursor = get_db().cursor()
    try:
        cursor.execute("SELECT ReviewID FROM Review WHERE ReviewID = %s", (review_id))
        if not cursor.fetchone():
            return jsonify({"error": "Review not found"}), 404
        
        cursor.execute("DELETE FROM Review WHERE ReviewID = %s", (review_id))
        get_db.commit()
        return jsonify({"message": "Review deleted successfully"}), 200
    except Error as e:
        current_app.logger.error(f'Database error in delete_review: {e}')
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()