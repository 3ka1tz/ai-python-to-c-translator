# prueba.pyx
cpdef int calcular_suma_pesada(int limite):
    cdef int i, total = 0
    for i in range(limite):
        total += i
    return total