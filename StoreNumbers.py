# Simple python script to store arrays of numbers.
import matplotlib.pyplot as plt

database = {"": []}  # Stored arrays
index = 0
table = [0]


# Saves an array.
def save(file_name, data):
    index.__add__(1)
    database.pop(file_name, data)
    print(file_name + " added at index: " + index.__str__())


# Loads an array.
def load(file_name):
    file_contents = database.get(file_name)
    index.__sub__(1)
    print(file_name + " removed at index: " + index.__str__())
    run(True, file_contents)


# Computes average of array.
def average(data_set):
    sum_of_scores = 0
    for n in table:
        sum_of_scores = sum_of_scores + n

    return sum_of_scores / len(data_set)


# Sorts the array.
def sort_prompt():
    data_sorted_prompt = input("Would you like this data sorted? [ yes / no ]")

    if data_sorted_prompt.__eq__("yes"):
        table.sort()


# Graphs the array.
def graph_prompt():
    data_graphed_prompt = input("Would you like this data graphed? [yes / no]")

    if data_graphed_prompt.__eq__("yes"):
        plt.imsave
        plt.plot(table)
        plt.show()
        plt.fill_between


# Prompts the user to continue or quit.
def loop_prompt():
    run_again = input("Continue?")

    if run_again.__eq__("no"):
        run(False, False)
    else:
        load_prompt = input("Load or begin again? [1]/[0]")
        if load_prompt == "1":
            load(input("Enter file name: "))
        elif load_prompt == "0":
            run(True, True)


# Main function.
def run(running, new):
    if not running:
        return

    if new is True:
        size = int(input("How Long Would You Like Your Array To Be"))

        for i in range(size):
            n = i + 1
            table.append(int(input("#" + n.__str__() + " ")))
    else:
        table.append(new)

    sort_prompt()
    graph_prompt()

    average_prompt = input("Would you like to compute the average?")

    if average_prompt.__eq__("yes"):
        print(average(table))

    save_prompt = input("Save?")

    if save_prompt.__eq__("yes"):
        save(input("enter a file name"), table)

    loop_prompt()


run(True, True)  # new script started.
