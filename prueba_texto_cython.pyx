def cifrar_texto(bytes texto_bytes, int desplazamiento):
    cdef bytearray resultado = bytearray(texto_bytes)
    
    for i in range(len(resultado)):
        char = resultado[i]
        
        if 65 <= char <= 90:
            resultado[i] = (char - 65 + desplazamiento) % 26 + 65
            
        elif 97 <= char <= 122:
            resultado[i] = (char - 97 + desplazamiento) % 26 + 97
            
    return bytes(resultado)