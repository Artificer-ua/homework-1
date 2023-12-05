###################################################################
# global
# CLI exit flag. Working while False.
exit_flag = False


###################################################################
# greeting function
def say_hello():
    return "How can i help you?"


###################################################################
# add new record
def add_record(name, phone):
    person.append({name: phone})
    return "Record Added"


###################################################################
# change phone in record
def change_record(name, phone):
    for item in person:
        if not item.get(name, None):
            continue
        else:
            old_phone = item[name]
            item[name] = phone
            return f"For record {name} \nold phone: {old_phone} was changed to \nnew phone: {phone} in item {name}"
    return "Nothing to change, try another command"


###################################################################
# show phone number
def show_phone(name):
    for item in person:
        if not item.get(name, None):
            continue
        else:
            return f"Phone number for {name}: {item.get(name)}"
    # print("{}".format(next((item for item in person if item.get(name, None)), False)))
    return "Nothing found, sorry."


###################################################################
# show all records in phonebook
def show_all():
    # if phonebook is empty
    if not len(person):
        return "No records. Try another command."
    result = list()
    result.append("\n\n{:<14}{:<15} ".format("Name", "Phone number"))
    for item in person:
        result.append("{:<14}{:<15} ".format([key for key in item.keys()][0], [val for val in item.values()][0]))
    result.append("\n\tEnd of list\n\n")
    return result


###################################################################
# exit function
def exit_f():
    # access to global value
    global exit_flag
    # turn main - while off.
    exit_flag = True
    return "Good Bye!"


###################################################################
# input error decorator  (KeyError, ValueError, IndexError)
# catch exceptions
def input_error(func):
    def inner(string):
        # test for required arguments
        test_string = string.split(" ")
        if test_string[0] == "add" or test_string[0] == "change":
            # if missed arguments for command
            if len(test_string) < 3:
                return "Give me name and phone please"
            # only numbers accepted in phone number
            elif not test_string[2].isdigit():
                return "Bad phone number. Only digit accepted. Try again"
        # if missed argument for command
        elif test_string[0] == "phone" and len(test_string) < 2:
            return "Enter user name"

        # error_exception = None
        try:
            return func(string)
        except KeyError:
            # error_exception = True
            print("key error")
            return None
        except IndexError:
            # error_exception = True
            print("Index error")
            return None
        except ValueError:
            # error_exception = True
            print("Value error")
            return None
        except TypeError:
            # error_exception = True
            print("Type Error")
            return None
    return inner


###################################################################
# input parser function
@input_error
def parser(input_value):
    # list of commands
    command_data = list()
    command_data = input_value.split(' ')

    # if command == good bye
    if command_data[0] == "good" and command_data[1] == "bye" and len(command_data) == 2:
        return command_list.get("exit")()

    # if command == show all
    if command_data[0] == "show" and command_data[1] == "all":
        return command_list.get("show all")()

    # if command not in list
    if command_data[0] not in command_list.keys():
        return None

    # variants of arguments in command
    if len(command_data) == 3:
        return command_list.get(command_data[0])(command_data[1], command_data[2])
    elif len(command_data) == 2:
        return command_list.get(command_data[0])(command_data[1])
    else:
        return command_list.get(command_data[0])()


# list of available commands proper functions
command_list = {
    "hello": say_hello,
    "add": add_record,
    "change": change_record,
    "phone": show_phone,
    "show all": show_all,
    "good bye": exit_f,
    "close": exit_f,
    "exit": exit_f
}

# sample phone book
# phones as string for leading zeros. All numeric format accepted.
person = [
    {"andrii": "00630001312"},
    {"ambulance": "103"},
    {"admin": "2380001"},
    {"garry": "80678889900"}
]


# main function
def main():
    global command_list
    input_value = ""

    while not exit_flag:
        input_value = input("Enter your command here: ")
        # call commands parser, lower case
        command = parser(input_value.lower())
        # print("Main, while. Command:", command)

        if command is None:
            print("Bad command, try again.")
            continue
        if type(command) is str:
            print(command)
        elif type(command) is list:
            for el in command:
                print(el)


##############
# end of main
##############


if __name__ == '__main__':
    print(f"Hello, i'm your CLI assistant.")
    main()
