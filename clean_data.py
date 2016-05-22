'''
Measure how consistent data is

given a csv, check:
    shape consistency: for every row, does the row have the same number of 
        columns as the rest of the rows?
    type consistency: for each row, does the data have the same type as most of
        the rest of the data (boolean, int, float, text?)
'''
import csv
import itertools
import sys

from collections import defaultdict

class ShapeCheck(object):
    def __init__(self):
        self.line_length_index = defaultdict(list)

    def next_line(self, line, line_number):
        self.line_length_index[len(line)].append(line_number)

    def report(self):
        if len(self.line_length_index) == 1:
            return '=== ShapeCheck Report ===\nThe shape of the data is consistent'
        
        max_category_quantity = len(self.line_length_index[0])
        max_category_index = 0
        
        total_line_count = 0

        for line_length in self.line_length_index:
            line_category_quantity = len(self.line_length_index[line_length])
            total_line_count += line_category_quantity

            if max_category_quantity < line_category_quantity:
                max_category_quantity = line_category_quantity
                max_category_index = line_length

        print(('\n=== ShapeCheck Report ===\nThe most common size was %d. ' % max_category_index)+ 
            ('It represented %d/%d (%f percent) of the data.' % 
                (max_category_quantity, total_line_count, 
                    100.0*max_category_quantity/total_line_count,)
            )
        )
        
        iii = input('print exceptions? y/n ')
        if iii == 'y':
            excepts = []
            for line_length in self.line_length_index:
                if not line_length == max_category_index:
                    excepts.extend(self.line_length_index[line_length])
            excepts.sort()
            print(excepts)
        return ''


class TypeCheck(object):
    def __init__(self, first_is_special=True):
        self.columns = []
        self.first_is_special = first_is_special

    def next_line(self, line, line_number):
        if self.first_is_special and line_number <= 0:
            return None
        column_index = 0
        for column in line:
            while len(self.columns) < column_index + 1:
                self.columns.append(defaultdict(list))
            type_ = 'String'
            if len(column) == 0:
                type_ = 'Empty'
            if len(column.strip()) == 4 and column.strip() == 'None':
                type_ = 'None'
            else:
                try:
                    int(column)
                    type_ = 'Integer'
                except ValueError:
                    try:
                        float(column)
                        type_ = 'Float'
                    except ValueError:
                        pass
            
            self.columns[column_index][type_].append(line_number)

            column_index += 1

    def report(self):
        print('=== Type Checker ===')
        col_index = 0
        for column in self.columns:
            if len(column) > 1:
                most_common_type = 'String'
                most_common_count = 0

                total_entries = 0

                for type_ in column:
                    # print('type: %s %d' % (type_, len(column[type_])))
                    total_entries += len(column[type_])
                    if len(column[type_]) > most_common_count:
                        most_common_count = len(column[type_])
                        most_common_type = type_
                if most_common_type == 'String':
                    # print('possible inconsistent types in column %d' % col_index)
                    # print('probably not an issue, just treat the column as a string')
                    pass
                else:
                    print('possible inconsistent types in column %d' % col_index)
                    print('The column is mostly %s, with %d/%d entries' % (most_common_type, most_common_count, total_entries))
                    for type_ in column:
                        if type_ is 'Empty':
                            print('type: Empty (%d entries) Default value recommended.' % len(column[type_]))
                            continue
                        if not type_ == most_common_type:
                            if type_ == 'String':
                                if len(column[type_]) <= 10:
                                    print('type: String has only %d entries in column %d. Consider checking these by hand.' % (len(column[type_]), col_index,))
                                    print('>>> %s <<<' % column[type_])
                                else:
                                    print('type: %s %s' % (type_, column[type_]))
                            else:
                                print('type: %s %s' % (type_, column[type_]))

            col_index += 1

        return ''

def consistency_report(csv_filename):
    shapec = ShapeCheck()
    typec = TypeCheck()

    line_number = 0

    with open(csv_filename, 'r') as csv_file:
        data_reader = csv.reader(csv_file)
        for line in data_reader:
            shapec.next_line(line, line_number)
            typec.next_line(line, line_number)
            line_number += 1

        print(shapec.report())
        print(typec.report())

if __name__ == '__main__':
    if len(sys.argv) >= 2:
        file_to_check = sys.argv[1]
        
        consistency_report(file_to_check)
