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

import json


class MyJson():
    def read_from_file(self, filename):
        ''' Load data from json file. Return data(list of dicts).'''
        with open(filename, 'r') as f:
            data = json.load(f)
        return data

    def write_file(self, filename, data):
        ''' Write data to json file.'''
        with open(filename, 'w') as f:
            f.write(json.dumps(data, indent=4))


class MyStudentsRoomsData():

    def __init__(self, students, rooms, format_file):
        self.students = students
        self.rooms = rooms
        self.format_file = format_file

    def gen_students(self, filename):
        '''Go through the entire students list. Yield dict with data about the student.'''
        students_data = MyJson().read_from_file(filename)
        for student in students_data:
            yield student

    def make_file(self, filename):
        '''
        Form a new rooms list. Add to dict key: value ('students': []). Using students generator (def gen_students()),
        write down each student's name in the appropriate room. Write the received data to json file.
        '''
        rooms_data = MyJson().read_from_file(rooms)
        gen_students_data = self.gen_students(students)
        format_data = [x for x in rooms_data]

        for gen in gen_students_data:
            room_num = gen['room']
            name = gen['name']
            if format_data[room_num].get('students'):
                format_data[room_num]['students'].append(name)
            else:
                format_data[room_num]['students'] = [name]
        MyJson().write_file(filename, format_data)


if __name__ == '__main__':
    rooms = input('Enter rooms list filename (for example rooms.json): ')
    students = input('Enter students lists filename (for example students.json): ')
    format_file = input('Enter output filename (for example format.json): ')

    MyStudentsRoomsData(students, rooms, format_file).make_file(format_file)
