from flask import Flask, request, jsonify
import traceback

from database import get_connection
from fault_manager import (
    get_machines,
    get_faults,
    add_fault,
    close_fault
)

app = Flask(__name__)

# -------------------------
# Home
# -------------------------
@app.route("/")
def home():
    return "Factory Maintenance Pro API"


# -------------------------
# Machines
# -------------------------
@app.route("/machines", methods=["GET"])
def machines():
    try:

        rows = get_machines()

        result = []

        for r in rows:
            result.append({
                "MachineID": r[0],
                "MachineName": r[1],
                "Description": r[2]
            })

        return jsonify(result)

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


# -------------------------
# Faults GET
# -------------------------
@app.route("/faults", methods=["GET"])
def faults():
    try:

        rows = get_faults()

        result = []

        for r in rows:

            result.append({

                "FaultID": r[0],
                "MachineID": r[1],
                "MachineName": r[2],
                "FaultName": r[3],
                "Description": r[4],
                "StartTime": str(r[5]) if r[5] else None,
                "EndTime": str(r[6]) if r[6] else None,
                "Duration": r[7],
                "Status": r[8]

            })

        return jsonify(result)

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


# -------------------------
# Add Fault
# -------------------------
@app.route("/faults", methods=["POST"])
def new_fault():
    try:

        data = request.get_json()

        machine_name = data["MachineName"]
        fault_name = data["FaultName"]
        description = data["Description"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT MachineID
            FROM Machines
            WHERE MachineName = ?
        """, (machine_name,))

        result = cursor.fetchone()

        conn.close()

        if not result:
            return jsonify({"error": "Machine not found"}), 400

        machine_id = result[0]

        add_fault(
            machine_id,
            fault_name,
            description
        )

        return jsonify({
            "message": "Fault Added Successfully"
        })

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


# -------------------------
# Close Fault
# -------------------------
@app.route("/faults/<int:fault_id>/close", methods=["PUT"])
def close_fault_api(fault_id):
    try:

        close_fault(fault_id)

        return jsonify({
            "message": "Fault Closed Successfully"
        })

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


# -------------------------
# Global Error Handler
# -------------------------
@app.errorhandler(500)
def internal_error(e):
    print(traceback.format_exc())
    return jsonify({
        "error": "Internal Server Error"
    }), 500


# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )