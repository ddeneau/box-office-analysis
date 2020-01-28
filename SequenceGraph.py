import time

import matplotlib.pyplot as plt

# Graphics the sequence defined below. 
table = [0]
table2 = [0]
table3 = [0]

intensity = 2
t1 = 0
t2 = 0
t3 = 0


def my_seq(n):
    if n is 0:
        return 1
    elif n % 2 == 0:
        return n / 2
    else:
        return (3 * n) + 1


def graphs(sequence, t, intensity_in):
    t = time.process_time_ns()

    for i in range(intensity_in):
        sequence.append(my_seq(i))

    t = time.process_time_ns() - t
    print(sequence)
    print("\n")
    print(t)
    print("\n")
    plt.plot(sequence)


graphs(table, t1, intensity)
graphs(table2, t2, intensity * 10)
graphs(table3, t3, intensity * 100)

plt.imsave
plt.plot(table)
plt.show()
plt.fill_between
