import os
import sys
import ollama

def generate_cython(input_path):
    if not os.path.exists(input_path):
        print(f"❌ Error: {input_path} not found.")
        sys.exit(1)

    with open(input_path, 'r', encoding='utf-8') as f:
        python_code = f.read()
    
    print(f"🤖 Optimizing code for Cython using qwen2.5-coder:7b...")
    
    system_prompt = (
        "You are an expert Cython developer. Optimize the provided Python code by "
        "converting it into valid Cython (.pyx). Add static C types (cdef, cpdef, int, double) "
        "to loops and intensive variables. Keep Python library imports intact. "
        "Return ONLY the raw Cython code inside a markdown code block without explanations."
    )

    try:
        response = ollama.chat(
            model='deepseek-coder:6.7b',
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

        # Save as .pyx file
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_dir = os.path.dirname(input_path) or "."
        pyx_path = os.path.join(output_dir, f"{base_name}_cython.pyx")
        
        with open(pyx_path, 'w', encoding='utf-8') as f:
            f.write(cython_code.strip())
            
        print(f"✅ Cython file saved: {pyx_path}")
        
        # Create the required setup.py automatically to compile it
        setup_path = os.path.join(output_dir, "setup.py")
        setup_content = f"""from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("{base_name}_cython.pyx")
)
"""
        with open(setup_path, 'w', encoding='utf-8') as f:
            f.write(setup_content)
        print(f"✅ Setup file saved: {setup_path}")
        print("\n🚀 To compile it, run: python setup.py build_ext --inplace")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python translator.py <file.py>")
    else:
        generate_cython(sys.argv[1])
