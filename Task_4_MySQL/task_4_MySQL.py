import argparse
import json
from decimal import Decimal

import mysql.connector

from xml.dom.minidom import parseString
from dicttoxml import dicttoxml

from .config import host_name, user_name, user_password, db_name


class CustomJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(CustomJsonEncoder, self).default(obj)


class OutputDataWriter:

    def __init__(self, f_name, f_type, data):
        self.f_name = f_name
        self.f_type = f_type
        self.data = data

    def output_filename(self):
        return (self.f_name + '.' + self.f_type)

    def write_json_file(self, filename):
        ''' Write data to json file.'''
        with open(filename, 'w') as f:
            f.write(json.dumps(self.data, indent=4, cls=CustomJsonEncoder))

    def write_xml_file(self, filename):
        ''' Write data to xml file.'''
        xml = dicttoxml(self.data, attr_type=False)
        dom = parseString(xml)
        data_to_file = dom.toprettyxml()
        with open(filename, 'w') as f:
            f.write(str(data_to_file))

    def choose_output_file_writer(self):
        ''' Choose json or xml file type.'''
        filename = self.output_filename()

        if self.f_type == 'json':
            self.write_json_file(filename)
        elif self.f_type == 'xml':
            self.write_xml_file(filename)
        else:
            print('Output file type must be json or xml')


class WorkerWithMySQL:

    def __init__(self, students_data, rooms_data):
        self.students_data = students_data
        self.rooms_data = rooms_data

    def create_connection(self, host_name, user_name, user_password, db_name):
        """Create connection to database"""
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name
            )
            print('Connection to MySQL DB is successful')
        except Exception as ex:
            print('Connection refused. The exception {} occurred'.format(ex))
        return connection

    def create_database(self, connection, query):
        """Create database"""
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            print('Database created successfully')
        except Exception as ex:
            print('CREATE DATABASE refused. The exception as {} occurred'.format(ex))

    def execute_query(self, connection, query):
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(query)
            connection.commit()
            print('Query executed successfully')
        except Exception as ex:
            print('The exception {} occurred'.format(ex))

    def execute_read_query(self, connection, query):
        cursor = connection.cursor(dictionary=True)
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as ex:
            print('The exception {} occurred'.format(ex))


def read_json_file(filename):
    ''' Load data from json file. Return data(list of dicts).'''
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def main():
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    parser.add_argument('students', type=argparse.FileType('r'), help='json file with info about students')
    parser.add_argument('rooms', type=argparse.FileType('r'), help='json file with info about rooms')
    parser.add_argument('output', type=str, default='json', help='json or xml file extension for output results')

    args = parser.parse_args()
    rooms_file, students_file, output_file_type = (args.rooms.name, args.students.name, args.output)

    students_data = read_json_file(students_file)
    rooms_data = read_json_file(rooms_file)

    w1 = WorkerWithMySQL(students_data, rooms_data)

    connection = w1.create_connection(host_name, user_name, user_password, db_name)
    create_database_query = "CREATE DATABASE IF NOT EXISTS {}".format(db_name)
    w1.create_database(connection, create_database_query)

    create_rooms_table = """CREATE TABLE IF NOT EXISTS rooms (
                            id INT PRIMARY KEY, 
                            name VARCHAR(20))
                        """
    w1.execute_query(connection, create_rooms_table)

    cursor = connection.cursor(dictionary=True)

    # Write json into table rooms
    for room in rooms_data:
        room_number = room['id']
        room_name = room['name']
        sql = "INSERT INTO rooms ( id, name ) VALUES ( %s, %s )"
        val = [(room_number, room_name), ]

        cursor.executemany(sql, val)
        connection.commit()

    create_students_table = """
        CREATE TABLE IF NOT EXISTS students (
          birthday DATE,
          id INT PRIMARY KEY,
          name VARCHAR(30),
          room_id INT,
          sex VARCHAR(10),
          FOREIGN KEY (room_id) REFERENCES rooms (id) ON DELETE SET NULL)
        """
    w1.execute_query(connection, create_students_table)

    # Write json into table students
    for student in students_data:
        birthday = student['birthday']
        stud_id = student['id']
        stud_name = student['name']
        room_num = student['room']
        stud_sex = student['sex']
        sql = "INSERT INTO students (birthday, id, name, room_id, sex ) VALUES (%s, %s, %s, %s, %s)"
        val = [(birthday, stud_id, stud_name, room_num, stud_sex), ]

        cursor.executemany(sql, val)
        connection.commit()

    # Rooms and students_number in room
    rooms_with_stud_number = """
        SELECT rooms.id, rooms.name, COUNT(*) as num_students
        FROM rooms INNER JOIN students ON rooms.id = students.room_id
        GROUP BY room_id
    """
    rooms = w1.execute_read_query(connection, rooms_with_stud_number)
    OutputDataWriter('rooms_with_stud_number', output_file_type, rooms).choose_output_file_writer()

    # Top 5 rooms with the smallest mean students age
    top5_rooms_smallest_mean_age = """
       SELECT rooms.id, rooms.name, AVG((YEAR(CURRENT_DATE)-YEAR(`birthday`))-
                                        (RIGHT(CURRENT_DATE,5)<RIGHT(`birthday`,5))) as avg_age
       FROM students INNER JOIN rooms ON rooms.id = students.room_id
       GROUP BY room_id
       ORDER BY avg_age
       LIMIT 5
    """
    rooms = w1.execute_read_query(connection, top5_rooms_smallest_mean_age)
    for room in rooms:
        print(room)
    print('eee', rooms)
    OutputDataWriter('top5_rooms_smallest_mean_age', output_file_type, rooms).choose_output_file_writer()

    # Top 5 rooms with max age difference
    top5_rooms_max_age_diff = """
      SELECT rooms.id, rooms.name, MAX((YEAR(CURRENT_DATE)-YEAR(`birthday`))-
                                        (RIGHT(CURRENT_DATE,5)<RIGHT(`birthday`,5))) - 
                                    MIN((YEAR(CURRENT_DATE)-YEAR(`birthday`))-
                                        (RIGHT(CURRENT_DATE,5)<RIGHT(`birthday`,5))) as max_age_difference
      FROM students INNER JOIN rooms ON rooms.id = students.room_id
      GROUP BY room_id
      ORDER BY max_age_difference DESC
      LIMIT 5
    """
    rooms = w1.execute_read_query(connection, top5_rooms_max_age_diff)
    OutputDataWriter('top5_rooms_max_age_diff', output_file_type, rooms).choose_output_file_writer()

    # Rooms with opposite students sex
    rooms_opposite_sex = """
     SELECT rooms.id, rooms.name, COUNT(DISTINCT students.sex) as count_sex
     FROM rooms INNER JOIN  students ON rooms.id = students.room_id
     GROUP BY room_id
     HAVING COUNT(DISTINCT students.sex) = 2
    """
    rooms = w1.execute_read_query(connection, rooms_opposite_sex)
    OutputDataWriter('rooms_opposite_sex', output_file_type, rooms).choose_output_file_writer()

    create_idx_room_num = """
           CREATE INDEX room_num_idx ON students (room_id) 
           """
    w1.execute_read_query(connection, create_idx_room_num)



    cursor.close()
    connection.close()


if __name__ == '__main__':
    main()
