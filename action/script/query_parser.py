import pandas as pd
from typing import Tuple


def parenthesis_checker(query: list) -> bool:
    """
    Description, it checks if the parenthesis are balanced
    """
    stack = []
    balanced = True
    index = 0
    while index < len(query) and balanced:
        symbol = query[index]
        if symbol in ['(', ')']:
            if symbol == "(":
                stack.append(symbol)
            else:
                if not stack:
                    balanced = False
                else:
                    stack.pop()
        index += 1

    if balanced and not stack:
        return True
    else:
        return False


def check_back_and_fore(query: list) -> bool:
    """
    Description, it checks if some and/or are near to each other, and same with tables
    """
    pointer = 1
    while pointer < len(query) - 1:
        if query[pointer] == 'TABLE':
            if query[pointer - 1] == 'TABLE' or query[pointer - 1] == 'TABLE':
                return False
        elif query[pointer] == 'and' or query[pointer] == 'or':
            if query[pointer - 1] in ['and', 'or'] or query[pointer + 1] in ['and', 'or']:
                return False
        pointer += 1
    return True


def query_checker(query: list) -> Tuple[bool, str]:
    """
    Description, it checks if a query is correct
    """

    # Check beginnings and endings of the query
    if query[0] in ['and', 'or', '=', '>', '<', ')']:
        return False, 'The query is not correct, you cant start with an operator or a closed parenthesis'
    elif query[-1] in ['and', 'or', '=', '>', '<', '(']:
        return False, 'The query is not correct, you cant end with an operator or an opened  parenthesis'
    elif query.count('(') != query.count(')'):
        return False, 'The query is not correct, the number of parenthesis is not equal'
    elif parenthesis_checker(query) is False:
        return False, 'The query is not correct, the parenthesis are not balanced'

    feature_types = ['open_to_tag', 'status_tag', 'n_meeting', 'n_matches', 'subscription_datetime', 'city', 'company',
                     'role', 'gender', 'age']
    integer_types = ['age', 'n_meetings', 'n_matches']

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
                if query[pointer - 1] not in integer_types or query[pointer + 1] in ['(', ')'] or \
                        type(int(query[pointer + 1])) != int:
                    return False, "Error in the query, check attribute names and parenthesis"
                else:
                    table_list.append('TABLE')
            elif query[pointer] in ['and', 'or', '(', ')']:
                table_list.append(query[pointer])

        except ValueError:
            return False, "Error in the query, check attribute names and parenthesis"

        pointer += 1

    print(table_list)

    # Check if the query execution is correctly achievable
    while table_list != ['TABLE']:
        pointer = 0
        while pointer < len(table_list):
            if table_list[pointer] in ['and', 'or']:
                if table_list[pointer - 1] == '(' or table_list[pointer + 1] == ')':
                    return False, "Error in the query, check parenthesis"
                elif table_list[pointer + 1] == 'TABLE' and table_list[pointer - 1] == 'TABLE':
                    table_list[pointer] = 'TABLE'
                    try:
                        if table_list[pointer + 2] == ')' and table_list[pointer - 2] == '(':
                            table_list.pop(pointer + 2)
                            table_list.pop(pointer + 1)
                            table_list.pop(pointer - 1)
                            table_list.pop(pointer - 2)
                            pointer -= 2
                        else:
                            table_list.pop(pointer + 1)  # erase the old table 1
                            table_list.pop(pointer - 1)  # erase the old table 2
                            pointer -= 1
                    except IndexError:
                        table_list.pop(pointer + 1)  # erase the old table 1
                        table_list.pop(pointer - 1)  # erase the old table 2
                        pointer -= 1
                else:
                    return False, "Error in the query, check to not have and or not near to each other"

            if table_list.count('TABLE') == len(table_list) and len(table_list) > 1:
                return False, "Error in the query, some tables are not connected with and/or relations"

            if check_back_and_fore(table_list) is False:
                return False, "Error in the query, check the order of the tables"

            pointer += 1

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
            if table_list[pointer] in ['and', 'or'] and table_list[pointer + 1] != '(' and table_list[pointer - 1] \
                    != ')':
                # Execute the query, performing and/or operation of the given attributes, store the result in the
                # list, erasing tables, operation and eventual parenthesis
                try:
                    table_list[pointer] = 'table'  # put the table that resulted
                    if table_list[pointer - 2] == '(' and table_list[pointer - 2] == ')':
                        table_list.pop(pointer + 2)  # erase the parenthesis
                        table_list.pop(pointer + 1)  # erase the old table 1
                        table_list.pop(pointer - 1)  # erase the old table 2
                        table_list.pop(pointer - 2)  # erase the parenthesis

                        pointer -= 2  # move the pointer back one position

                    else:
                        table_list.pop(pointer + 1)  # erase the old table 1
                        table_list.pop(pointer - 1)  # erase the old table 2
                        pointer -= 1

                except IndexError:
                    table_list.pop(pointer + 1)  # erase the old table 1
                    table_list.pop(pointer - 1)  # erase the old table 2
                    pointer -= 1

            pointer += 1

    return table_list[0]
