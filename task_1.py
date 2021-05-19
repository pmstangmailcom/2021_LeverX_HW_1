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


class MyReader():

    def read_json_file(self, filename):
        ''' Load data from json file. Return data(list of dicts).'''
        with open(filename, 'r') as f:
            data = json.load(f)
        return data


class MyWriter():

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


class StudentsAndRoomsData():

    def __init__(self, students_data, rooms_data):
        self.students_data = students_data
        self.rooms_data = rooms_data

    def gen_students(self, students_data):
        '''Go through the entire students list. Yield dict with data about the student.'''
        for student in students_data:
            yield student

    def make_data(self, rooms_data):
        '''
        Form a new rooms list. Add to dict key: value ('students': []). Using students generator (def gen_students()),
        write down each student's name in the appropriate room. Write the received data to json file.
        '''
        gen_students_data = self.gen_students(self.students_data)
        format_data = [x for x in rooms_data]

        for gen in gen_students_data:
            room_num = gen['room']
            name = gen['name']
            if format_data[room_num].get('students'):
                format_data[room_num]['students'].append(name)
            else:
                format_data[room_num]['students'] = [name]

        return format_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('students', type=argparse.FileType('r'), help='json file with info about students')
    parser.add_argument('rooms', type=argparse.FileType('r'), help='json file with info about rooms')
    parser.add_argument('output', type=argparse.FileType('w'), help='json or xml file for output results')

    args = parser.parse_args()
    rooms_file, students_file, output_file = (args.rooms.name, args.students.name, args.output.name)

    students_data = MyReader().read_json_file(students_file)
    rooms_data = MyReader().read_json_file(rooms_file)
    output_data = StudentsAndRoomsData(students_data, rooms_data).make_data(rooms_data)

    if args.output.name.lower().endswith(('.json')):
        MyWriter().write_json_file(output_file, output_data)
    elif args.output.name.lower().endswith(('.xml')):
        MyWriter().write_xml_file(output_file, output_data)
    else:
        print('Output file type must be json or xml')


if __name__ == '__main__':
    main()
