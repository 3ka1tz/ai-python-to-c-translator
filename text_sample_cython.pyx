def cipher_text(bytes text_bytes, int shift):
    cdef bytearray result = bytearray(text_bytes)
    cdef int length = len(result)
    cdef int i
    cdef int char_val

    for i in range(length):
        char_val = result[i]

        if 65 <= char_val <= 90:
            result[i] = (char_val - 65 + shift) % 26 + 65
 
        elif 97 <= char_val <= 122:
            result[i] = (char_val - 97 + shift) % 26 + 97

    return bytes(result)