import random

def randomize_list(input_list):
    randomized_list = input_list.copy()
    random.shuffle(randomized_list)
    return randomized_list

# Example usage:
my_list = ["a","b","c"]
randomized_result = randomize_list(my_list)

#print("Original List:", my_list)
#print("Randomized List:", randomized_result)

for term in randomized_result:
    print(term)