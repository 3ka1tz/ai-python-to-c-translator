cdef long long calculate_heavy_sum(long long limit):
    cdef long long total = 0
    cdef int i
    for i in range(limit):
        total += i
    return total

print("Result:", calculate_heavy_sum(10000000))