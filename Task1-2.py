# 2. Given a list of integers. Remove duplicates from the list and create a tuple.
# Find the minimum and maximum number.

def task(integer_list):
    int_tuple = tuple(set(integer_list))
    print(int_tuple)
    print(f"Maximum number: {max(int_tuple)}")
    print(f"Minimum number: {min(int_tuple)}")

#Example usage
task([2,4,3,3,3,9,20,-1,0,2,6,5,3])
