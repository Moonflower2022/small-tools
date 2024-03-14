import time

map = {
    0: "\\",
    1: "|",
    2: "/",
    3: "-",
}

length = 150

for i in range(0, length):
    print("{}/{} {}".format(i, length, map[i % 4]), end="\r")
    time.sleep(0.10)