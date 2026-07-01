from database import get_connection


# =========================== GET MACHINES ===========================

def get_machines():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            MachineID,
            MachineName,
            Description
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
            FaultID,
            MachineID,
            MachineName,
            FaultName,
            Description,
            StartTime,
            EndTime,
            Duration,
            Status
        FROM dbo.vwFaults
        ORDER BY FaultID DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows


# =========================== ADD FAULT ===========================

def add_fault(machine_id, fault_name, description):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Faults
        (
            MachineID,
            FaultName,
            Description
        )
        VALUES (?, ?, ?)
    """, (
        machine_id,
        fault_name,
        description
    ))

    conn.commit()
    conn.close()


# =========================== CLOSE FAULT ===========================

def close_fault(fault_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Faults
        SET
            EndTime = GETDATE(),
            Status = 'Closed'
        WHERE FaultID = ?
          AND Status = 'Open'
    """, (fault_id,))

    conn.commit()
    conn.close()