import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "packages": ["os", "llama_parse", "langchain_openai", "dotenv", "pydantic"],
    #"includes": ["os", "llama_parse", "langchain-openai", "dotenv"]   
    "include_files": ["utils", "notas"]
}

#Checking base
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="EmissorAutomatic",
    version="0.1",
    description="Cria notas a partir de um pdf",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base="gui")],
)