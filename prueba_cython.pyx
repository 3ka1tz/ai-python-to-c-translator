# prueba.pyx
def calcular_suma_pesada(long long limite):
    cdef long long total = 0
    cdef int i
    for i in range(limite):
        total += i
    return total

cpdef main():
    print("Resultado:", calcular_suma_pesada(10000000))

if __name__ == "__main__":
    main()