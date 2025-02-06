# import os

# def check_brackets(filename):
#     with open(filename, "r") as f:
#         s = f.read()
#         stack = []
#         for i, char in enumerate(s):
#             if char == "(":
#                 stack.append(i)
#             elif char == ")":
#                 if stack:
#                     stack.pop()
#                 else:
#                     return False
#         return len(stack) == 0

# def count_files_with_mismatched_brackets(directory):
#     count = 0
#     for filename in os.listdir(directory):
#         if not os.path.isdir(filename):
#             if not check_brackets(os.path.join(directory, filename)):
#                 count += 1
#     return count

# directory = "problem_files"
# count = count_files_with_mismatched_brackets(directory)
# print(f"{count} files in {directory} have mismatched brackets.")

import os

def check_brackets(filename):
    with open(filename, "r") as f:
        s = f.read()
        stack = []
        for i, char in enumerate(s):
            if char == "(":
                stack.append(i)
            elif char == ")":
                if stack:
                    stack.pop()
                else:
                    return False
        return len(stack) == 0

def correct_brackets(filename):
    with open(filename, "r") as f:
        s = f.read()
        stack = []
        for i, char in enumerate(s):
            if char == "(":
                stack.append(i)
            elif char == ")":
                if stack:
                    stack.pop()
                else:
                    s = s[:i] + "(" + s[i:]
                    stack.append(i)
        while stack:
            j = stack.pop()
            s = s[:j+1] + ")" + s[j+1:]
        with open(filename, "w") as f:
            f.write(s)

def correct_files_with_mismatched_brackets(directory):
    count = 0
    for filename in os.listdir(directory):
        print(filename)
        exit()
        if not os.path.isdir(filename):
            if not check_brackets(os.path.join(directory, filename)):
                correct_brackets(os.path.join(directory, filename))
                count += 1
        exit()
    return count

directory = "problem_files"
count = correct_files_with_mismatched_brackets(directory)
print(f"{count} files in {directory} had mismatched brackets and have been corrected.")
