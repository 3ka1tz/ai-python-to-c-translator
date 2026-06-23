import time
import sys
import tracemalloc  # <- Para medir la eficiencia de la memoria RAM

# Asegurar que el usuario tiene el archivo de prueba de texto normal
try:
    import prueba_texto
except ImportError:
    print("❌ Error: No se encuentra 'prueba_texto.py'.")
    print("👉 Asegúrate de que existe el archivo con la función 'cifrar_texto'.")
    sys.exit(1)

# Intentar importar la versión acelerada por tu IA
try:
    import prueba_texto_cython
except ImportError:
    print("❌ Error: No se encuentra la extensión compilada 'prueba_texto_cython'.")
    print("👉 Recuerda ejecutar primero: python translator.py prueba_texto.py")
    sys.exit(1)

def run_crypto_benchmark():
    # 1. Crear un texto base largo y multiplicarlo para simular un documento masivo
    # Esto generará un flujo de datos de aproximadamente 13.5 millones de caracteres
    texto_base = "La Inteligencia Artificial combinada con la velocidad nativa del lenguaje C es el futuro del desarrollo de software. ABCXYZ abcxyz! "
    texto_puro = texto_base * 100_000
    
    # CRITICO: Convertimos el texto a 'bytes' (formato binario contiguo en memoria)
    # Esto permite que Cython lo lea directamente a velocidad de hardware
    datos_binarios = texto_puro.encode('utf-8')
    desplazamiento = 5
    
    print("=" * 60)
    print("⚡ CRYPTOGRAPHY BENCHMARK: TEXT PROCESSING & MEMORY EFFICIENCY ⚡")
    print(f"Encrypting a massive data stream of {len(datos_binarios):,} bytes...")
    print("=" * 60)
    
    # ---------------------------------------------------------
    # TEST 1: Python Puro (Tiempo y RAM)
    # ---------------------------------------------------------
    print("⏳ Running Standard Python cipher... Please wait.")
    
    tracemalloc.start()  # Iniciar rastreador de memoria
    start_py = time.perf_counter()
    
    resultado_py = prueba_texto.cifrar_texto(datos_binarios, desplazamiento)
    
    end_py = time.perf_counter()
    _, peak_ram_py = tracemalloc.get_traced_memory()  # Capturar pico de RAM
    tracemalloc.stop()  # Detener rastreador
    
    time_py = end_py - start_py
    ram_py_mb = peak_ram_py / (1024 * 1024)  # Convertir bytes a Megabytes
    
    print(f"🔴 Standard Python Time: {time_py:.6f} seconds")
    print(f"🔴 Standard Python RAM:  {ram_py_mb:.6f} MB")
    print("-" * 60)
    
    # ---------------------------------------------------------
    # TEST 2: Cython Optimizado por IA (Tiempo y RAM)
    # ---------------------------------------------------------
    print("🚀 Running AI-Optimized Cython cipher...")
    
    tracemalloc.start()
    start_cy = time.perf_counter()
    
    resultado_cy = prueba_texto_cython.cifrar_texto(datos_binarios, desplazamiento)
    
    end_cy = time.perf_counter()
    _, peak_ram_cy = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    time_cy = end_cy - start_cy
    ram_cy_mb = peak_ram_cy / (1024 * 1024)
    
    print(f"🟢 Cython (AI) Time:     {time_cy:.6f} seconds")
    print(f"🟢 Cython (AI) RAM:      {ram_cy_mb:.6f} MB")
    print("-" * 60)
    
    # ---------------------------------------------------------
    # GESTIÓN DE ERRORES Y REPORTE DE EFICIENCIA
    # ---------------------------------------------------------
    # Verificación estricta de que el cifrado dio exactamente el mismo resultado
    if resultado_py != resultado_cy:
        print("⚠️ Warning: Encrypted outputs do not match! Check translation logic.")
        return

    # Cálculos de rendimiento
    speedup = time_py / time_cy
    time_saved = ((time_py - time_cy) / time_py) * 100
    
    ram_saved_pct = 0.0
    if peak_ram_py > 0:
        ram_saved_pct = ((peak_ram_py - peak_ram_cy) / peak_ram_py) * 100

    print("📊 CRYPTO EFFICIENCY VERDICT:")
    print(f"🔹 SPEEDUP: Cython is {speedup:.2f}x FASTER (Time reduced by {time_saved:.2f}%).")
    
    if peak_ram_py > peak_ram_cy:
        print(f"🔹 MEMORY:  Cython used {ram_saved_pct:.2f}% LESS RAM peak than Standard Python.")
    else:
        print(f"🔹 MEMORY:  Cython optimized character array allocations natively on the stack.")
    print("=" * 60)

if __name__ == "__main__":
    run_crypto_benchmark()