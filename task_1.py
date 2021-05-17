'''
Даны 2 файла (смотрите в прикрепленных файлах):
- students.json
- rooms.json

Необходимо написать скрипт, целью которого будет загрузка этих двух файлов, объединения их в список комнат где
каждая комната содержит список студентов которые
находятся в этой комнате, а также последующую выгрузку их в формате JSON или XML.

Необходима поддержка следующих входных параметров:
- students # путь к файлу студентов
- rooms # путь к файлу комнат
- format # выходной формат (xml или json)

Ожидается использование ООП и SOLID
'''

import argparse
import json

from xml.dom.minidom import parseString
from dicttoxml import dicttoxml


class MyStudentsRoomsData():

    def __init__(self, students, rooms, format_file):
        self.students = students
        self.rooms = rooms
        self.format_file = format_file

    def read_json_file(self, filename):
        ''' Load data from json file. Return data(list of dicts).'''
        with open(filename, 'r') as f:
            data = json.load(f)
        return data

    def write_json_file(self, filename, data):
        ''' Write data to json file.'''
        with open(filename, 'w') as f:
            f.write(json.dumps(data, indent=4))

    def write_xml_file(self, filename, data):
        ''' Write data to xml file.'''
        xml = dicttoxml(data, attr_type=False)
        dom = parseString(xml)
        data_to_file = dom.toprettyxml()

        with open(filename, 'w') as f:
            f.write(str(data_to_file))

    def gen_students(self, filename):
        '''Go through the entire students list. Yield dict with data about the student.'''
        students_data = self.read_json_file(filename)
        for student in students_data:
            yield student

    def make_file(self):
        '''
        Form a new rooms list. Add to dict key: value ('students': []). Using students generator (def gen_students()),
        write down each student's name in the appropriate room. Write the received data to json file.
        '''
        rooms_data = self.read_json_file(self.rooms)
        gen_students_data = self.gen_students(self.students)
        format_data = [x for x in rooms_data]

        for gen in gen_students_data:
            room_num = gen['room']
            name = gen['name']
            if format_data[room_num].get('students'):
                format_data[room_num]['students'].append(name)
            else:
                format_data[room_num]['students'] = [name]

        return format_data


if __name__ == '__main__':
    print('Enter filenames (for example  students.json rooms.json format.json (or format.xml)')
    parser = argparse.ArgumentParser()
    parser.add_argument('students', type=argparse.FileType('r'), help='json file with info about students')
    parser.add_argument('rooms', type=argparse.FileType('r'), help='json file with info about rooms')
    parser.add_argument('output', type=argparse.FileType('w'), help='json or xml file for output results')

    args = parser.parse_args()
    rooms_file, students_file, output_file = (args.rooms.name, args.students.name, args.output.name)
    data = MyStudentsRoomsData(rooms_file, students_file, output_file).make_file()

    if args.output.name.lower().endswith(('.json')):
        MyStudentsRoomsData(rooms_file, students_file, output_file).write_json_file(output_file, data)
    elif args.output.name.lower().endswith(('.xml')):
        MyStudentsRoomsData(rooms_file, students_file, output_file).write_xml_file(output_file, data)
    else:
        print('Output file type must be json or xml')
