def calc(xs, k):
    k_max = []
    result = []
    for ind, val in enumerate(xs):
        for i in range(len(k_max)):
            if val > k_max[i] :
                k_max[i] = val
        k_max.append(val)
        if ind >= (k-1):
            result.append(k_max[0])
            k_max.pop(0)
    return result
if __name__ =="__main__":
    array_given = [1, 3, 2, 4, 6, 5]
    n = len(array_given)
    final_result_list = []
    for k in range(1,n+1):
        now_value = calc(array_given, k)
        local_result = min(now_value)
        final_result_list.append(local_result)
    print(final_result_list)