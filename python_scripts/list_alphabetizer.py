def user_input():
    print("paste words serperated by spaces here: ")
    list = str(input()).split(" ")
    print("sorted list:")
    list.sort()
    print(list)
    user_input()
user_input()
