# prueba_texto.py

def cifrar_texto(texto_bytes, desplazamiento):
    # Convertimos a bytearray para poder modificar los caracteres in-place de forma eficiente
    resultado = bytearray(texto_bytes)
    
    for i in range(len(resultado)):
        char = resultado[i]
        
        # En un objeto de tipo bytes, 'char' es directamente el número ASCII (int)
        # 65 es 'A', 90 es 'Z'
        if 65 <= char <= 90:
            resultado[i] = (char - 65 + desplazamiento) % 26 + 65
            
        # 97 es 'a', 122 es 'z'
        elif 97 <= char <= 122:
            resultado[i] = (char - 97 + desplazamiento) % 26 + 97
            
    return bytes(resultado)