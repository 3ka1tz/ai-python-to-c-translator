import os
import sys
import subprocess  # <- Necesario para compilar en segundo plano
import ollama

def generate_cython_and_compile(input_path):
    if not os.path.exists(input_path):
        print(f"❌ Error: {input_path} not found.")
        sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        python_code = f.read()
    
    # 1. Llamar a la IA (Corregido a qwen2.5-coder:7b)
    print(f"🤖 [1/3] Optimizing code for Cython using qwen2.5-coder:7b...")
    
    system_prompt = (
        "You are an expert Cython developer. Optimize the provided Python code by "
        "converting it into valid Cython (.pyx). Add static C types (cdef, cpdef, int, double) "
        "to loops and intensive variables. Keep Python library imports intact. "
        "Return ONLY the raw Cython code inside a markdown code block without explanations."
    )

    try:
        response = ollama.chat(
            model='deepseek-coder:6.7b',  # <- ¡Unificado aquí!
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': python_code}
            ]
        )
        
        cython_code = response['message']['content']
        
        if "```" in cython_code:
            cython_code = cython_code.split("```")[1]
            if cython_code.startswith("cython\n"): cython_code = cython_code[7:]
            elif cython_code.startswith("python\n"): cython_code = cython_code[7:]
            elif cython_code.startswith("pyx\n"): cython_code = cython_code[4:]
            elif cython_code.startswith("c\n"): cython_code = cython_code[2:]

        # Generar rutas y nombres de archivos
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_dir = os.path.dirname(input_path) or "."
        pyx_path = os.path.join(output_dir, f"{base_name}_cython.pyx")
        
        # Guardar el archivo .pyx generado por la IA
        with open(pyx_path, 'w', encoding='utf-8') as f:
            f.write(cython_code.strip())
            
        print(f"📝 [2/3] Cython file saved: {pyx_path}")
        
        # Crear un archivo setup temporal para compilar
        setup_path = os.path.join(output_dir, "setup_temp.py")
        setup_content = f"""from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("{pyx_path}", quiet=True)
)
"""
        with open(setup_path, 'w', encoding='utf-8') as f:
            f.write(setup_content)

        # 2. Compilación automática en segundo plano
        print(f"⚡ [3/3] Compiling Cython extension into a native C binary...")
        
        # Lanza la compilación de forma silenciosa
        result = subprocess.run(
            [sys.executable, setup_path, "build_ext", "--inplace"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE
        )
        
        # Limpieza de archivos intermedios generados para no ensuciar la carpeta del usuario
        if os.path.exists(setup_path):
            os.remove(setup_path)
        c_intermedio = os.path.join(output_dir, f"{base_name}_cython.c")
        if os.path.exists(c_intermedio):
            os.remove(c_intermedio)

        # Verificar si todo salió bien
        if result.returncode == 0:
            print(f"\n🚀 ✨ SUCCESS! ✨")
            print(f"Your optimized extension is ready. In Python, you can now use:")
            print(f"👉 import {base_name}_cython")
        else:
            print(f"\n❌ Compilation Error:")
            print(result.stderr.decode('utf-8'))

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python translator.py <file.py>")
    else:
        generate_cython_and_compile(sys.argv[1])