from database.i_db_comm import IDbComm
from pojos.event import Event
from pojos.force import Force
import sqlite3


class SqlLiteDbComm(IDbComm):

    def __init__(self):
        x = 0

   def get_all_events(self):



if __name__ == '__main__':

    con = sqlite3.connect(r".\medical_db.db")
    cur = con.cursor()
    cur.execute('''
        SELECT force_id, force_name, force_latitude, force_longitude, force_type_name, event_name
        FROM forces
        LEFT JOIN force_types
        ON forces.force_type_id = force_types.force_type_id
        LEFT JOIN events
        ON events.event_id = forces.force_id
        ''')
    records = cur.fetchall()
    print(records)
    con.close()
