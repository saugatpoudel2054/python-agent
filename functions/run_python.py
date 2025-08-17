import os
import subprocess

from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        current_dir = os.path.abspath(os.path.join(working_directory))
        file_path_abs = os.path.abspath(os.path.join(working_directory, file_path))

        if not file_path_abs.startswith(current_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(file_path_abs):
            return f'Error: File "{file_path}" not found.'

        if file_path_abs[-3:] != ".py":
            return f'Error: File "{file_path}" is not a Python file.'
        
        try:
            completed_process = subprocess.run(["python", file_path_abs] + args, timeout=30, capture_output=True, text=True)
            if completed_process.returncode != 0:
                return f"STDERR (Process exited with code {completed_process.returncode}): {completed_process.stderr}"
            if completed_process.stdout == "":
                return "No output produced"
            return f"STDOUT: {completed_process.stdout}"
        except Exception as e:
            return f"Error: executing Python file: {e}"

    except Exception as e:
        return f'Error: {e}'
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the specified Python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Additional arguments to pass to the Python file.",
            ),
        },
    ),
)