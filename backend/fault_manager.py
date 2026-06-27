from database import get_connection


# =========================== GET MACHINES ===========================

def get_machines():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT MachineID, MachineName, Description
        FROM Machines
        ORDER BY MachineName
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


# =========================== GET FAULTS ===========================

def get_faults():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            F.FaultID,
            M.MachineName,
            F.FaultName,
            F.Description,
            F.StartTime
        FROM Faults F
        INNER JOIN Machines M
            ON F.MachineID = M.MachineID
        ORDER BY F.FaultID DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


# =========================== ADD FAULT ===========================

def add_fault(machine_id, fault_name, description):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Faults (MachineID, FaultName, Description)
        VALUES (?, ?, ?)
    """, (
        machine_id,
        fault_name,
        description
    ))

    conn.commit()
    conn.close()