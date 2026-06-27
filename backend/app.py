from flask import Flask, request, jsonify

from database import get_connection

from fault_manager import (
    get_machines,
    get_faults,
    add_fault
)

app = Flask(__name__)

@app.route("/")
def home():

    return "Factory Maintenance Pro API"


@app.route("/machines", methods=["GET"])
def machines():

    rows = get_machines()

    result = []

    for r in rows:

        result.append({

            "MachineID": r.MachineID,

            "MachineName": r.MachineName,

            "Description": r.Description

        })

    return jsonify(result)


@app.route("/faults", methods=["GET"])
def faults():

    rows = get_faults()

    result = []

    for r in rows:

        result.append({

            "FaultID": r.FaultID,

            "MachineName": r.MachineName,

            "FaultName": r.FaultName,

            "Description": r.Description,

            "StartTime": str(r.StartTime)[:16]

        })

    return jsonify(result)


@app.route("/faults", methods=["POST"])
def new_fault():

    data = request.get_json()

    machine_name = data["MachineName"]
    fault_name = data["FaultName"]
    description = data["Description"]

    conn = get_connection()
    cursor = conn.cursor()

    # 🔥 نحول الاسم إلى ID
    cursor.execute("""
        SELECT MachineID FROM Machines WHERE MachineName = ?
    """, (machine_name,))

    result = cursor.fetchone()

    if not result:
        return jsonify({"error": "Machine not found"}), 400

    machine_id = result[0]

    # 🔥 نضيف العطل بالـ ID
    add_fault(
        machine_id,
        fault_name,
        description
    )

    return jsonify({"message": "Fault Added Successfully"})

if __name__ == '__main__':
    
    app.run(host="0.0.0.0", port=5000, debug=True)