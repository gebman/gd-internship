# 2. Given a list of integers. Remove duplicates from the list and create a tuple.
# Find the minimum and maximum number.


def task(integer_list):
    if type(integer_list) is not list:
        raise TypeError("expected a list of integers")
    unique_list = []
    for x in integer_list:
        if type(x) is not int:
            raise TypeError("expected a list of integers")
        if x not in unique_list:
            unique_list.append(x)

    answer = dict()
    answer["tuple"] = tuple(unique_list)
    answer["max"] = max(unique_list)
    answer["min"] = min(unique_list)
    return answer

        
    
print(task([4,5,2,3,3,5,5,3,10,-23]))

   