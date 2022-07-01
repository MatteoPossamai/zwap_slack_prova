import pandas as pd
from typing import Tuple


def query_checker(query: list) -> Tuple[bool, str]:
    """
    Description, it checks if a query is correct
    """
    if query[0] in ['and', 'or', '=', '>', '<', '(', ')']:
        return False, 'The query is not correct, you cant start with an operator or a parenthesis'
    elif query[-1] in ['and', 'or', '=', '>', '<', '(', ')']:
        return False, 'The query is not correct, you cant end with an operator or a parenthesis'
    elif query.count('(') != query.count(')'):
        return False, 'The query is not correct, the number of parenthesis is not equal'


    feature_types = ['open_to_tag', 'status_tag', 'n_meeting', 'n_matches', 'subscription_datetime', 'city', 'company',
                     'role', 'gender', 'age']
    integer_types = ['age', 'n_meeting', 'n_matches']

    table_list = []
    pointer = 0

    # Only check tables are fine
    while pointer < len(query):
        try:
            if query[pointer] == '=':
                if query[pointer - 1] not in feature_types or query[pointer + 1] in ['(', ')']:
                    return False, "Error in the query, check attribute names and parenthesis"
                else:
                    table_list.append('TABLE')
            elif query[pointer] in ['>', '<']:
                if query[pointer - 1] not in integer_types or query[pointer + 1] in ['(', ')']:
                    return False, "Error in the query, check attribute names and parenthesis"
            elif query[pointer] in ['AND', 'OR', '(', ')']:
                table_list.append(query[pointer])

        except ValueError:
            return False, "Error in the query, check attribute names and parenthesis"

    print(table_list)


    return True, 'The query is valid'


def query_executor(query: list) -> pd.DataFrame:
    """
    Description, it executes a query
    """

    integer_types = ['age', 'n_meeting', 'n_matches']

    table_list = []
    pointer = 0

    # First circle, inserts tables in the new table_list
    while pointer < len(query):
        if query[pointer] == '=':
            # Execute the query, checking attribute query[pointer - 1] is equal to query[pointer + 1]
            # and put it to the table_list
            pass
        elif query[pointer] == '>' and query[pointer - 1] in integer_types:
            # Execute the query, checking attribute query[pointer - 1] is greater than query[pointer + 1]
            # and put it to the table_list
            pass
        elif query[pointer] == '<' and query[pointer - 1] in integer_types:
            # Execute the query, checking attribute query[pointer - 1] is less than query[pointer + 1]
            # and put it to the table_list
            pass

    # Second circle, to perform the rest of the operations
    while len(table_list) > 1:
        pointer = 0

        while pointer < len(table_list):
            if table_list[pointer] in ['and', 'or'] and table_list[pointer + 1] not in ['(', ')'] and \
                    table_list[pointer - 1] not in ['(', ')']:
                # Execute the query, performing and/or operation of the given attributes, store the result in the
                # list, erasing tables, operation and eventual parenthesis
                try:
                    table_list[pointer] = 'table'  # put the table that resulted
                    if table_list[pointer - 2] == '(' and table_list[pointer - 2] == ')':
                        table_list.pop(pointer + 2)  # erase the parenthesis
                        table_list.pop(pointer + 1)  # erase the old table 1
                        table_list.pop(pointer - 1)  # erase the old table 2
                        table_list.pop(pointer - 2)  # erase the parenthesis

                        pointer -= 1  # move the pointer back one position

                    else:
                        table_list.pop(pointer + 1)  # erase the old table 1
                        table_list.pop(pointer - 1)  # erase the old table 2

                except IndexError:
                    table_list.pop(pointer + 1)  # erase the old table 1
                    table_list.pop(pointer - 1)  # erase the old table 2

    return table_list[0]
