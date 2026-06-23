import time
import os
import sys

# Asegurar que el usuario tiene el archivo de prueba normal
try:
    import prueba
except ImportError:
    print("❌ Error: No se encuentra 'prueba.py'. Asegúrate de que existe en esta carpeta.")
    sys.exit(1)

# Intentar importar la versión acelerada por tu IA
try:
    import prueba_cython
except ImportError:
    print("❌ Error: No se encuentra la extensión compilada 'prueba_cython'.")
    print("👉 Recuerda ejecutar primero: python translator.py prueba.py")
    sys.exit(1)

def run_benchmark():
    # Definimos un límite muy alto para poner a prueba el procesador (50 millones de vueltas)
    # Si notas que tarda demasiado en tu máquina, puedes bajarlo a 10000000
    iterations = 50_000_000
    
    print("=" * 60)
    print("⚡ PYTHON VS CYTHON (AI-OPTIMIZED) SPEED BENCHMARK ⚡")
    print(f"Testing a loop with {iterations:,} operations...")
    print("=" * 60)
    
    # ---------------------------------------------------------
    # TEST 1: Python Puro (Lento)
    # ---------------------------------------------------------
    print("⏳ Running Standard Python version... Please wait.")
    start_py = time.perf_counter()
    result_py = prueba.calcular_suma_pesada(iterations)
    end_py = time.perf_counter()
    
    time_py = end_py - start_py
    print(f"🔴 Standard Python Time: {time_py:.6f} seconds")
    print(f"   Result: {result_py}")
    print("-" * 60)
    
    # ---------------------------------------------------------
    # TEST 2: Versión Optimizada por la IA + Cython (Rápido)
    # ---------------------------------------------------------
    print("🚀 Running AI-Optimized Cython version...")
    start_cy = time.perf_counter()
    result_cy = prueba_cython.calcular_suma_pesada(iterations)
    end_cy = time.perf_counter()
    
    time_cy = end_cy - start_cy
    print(f"🟢 Cython (AI) Time:     {time_cy:.6f} seconds")
    print(f"   Result: {result_cy}")
    print("-" * 60)
    
    # ---------------------------------------------------------
    # COMPARATIVA Y CONCLUSIÓN
    # ---------------------------------------------------------
    # Validación de que ambos algoritmos dieron exactamente el mismo resultado matemático
    if result_py != result_cy:
        print("⚠️ Warning: Results do not match! Check the AI translation logic.")
        return

    # Calcular el factor de aceleración
    speedup = time_py / time_cy
    
    print("📊 FINAL VERDICT:")
    print(f"The AI-Optimized Cython extension is {speedup:.2f}x FASTER than Standard Python.")
    
    # Calcular el porcentaje de tiempo ahorrado
    time_saved = ((time_py - time_cy) / time_py) * 100
    print(f"Total processing time reduced by {time_saved:.2f}%")
    print("=" * 60)

if __name__ == "__main__":
    run_benchmark()
