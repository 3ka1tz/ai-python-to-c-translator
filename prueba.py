# prueba.py
def calcular_suma_pesada(limite):
    total = 0
    for i in range(limite):
        total += i
    return total

print("Resultado:", calcular_suma_pesada(10000000))