import os
from config import MAX_CHARS
from google.genai import types
from functions.run_python import schema_run_python_file

def get_files_info(working_directory, directory="."):
    try:
        created_dir = os.path.abspath(os.path.join(working_directory, directory))
        current_dir = os.path.abspath(os.path.join(working_directory))

        if not created_dir.startswith(current_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(created_dir):
            return f'Error: "{directory}" is not a directory'
        
        files_in_dict = os.listdir(created_dir)
        file_description_list = []

        for file in files_in_dict:
            full_path = created_dir + '/' + file
            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            file_description_list.append(f"- {file}: {file_size}, is_dir={is_dir}")
    except Exception as e:
        return f'Error: {e}'


    return '\n'.join(file_description_list)

def get_file_content(working_directory, file_path):
    try:
        current_dir = os.path.abspath(os.path.join(working_directory))
        file_path_abs = os.path.abspath(os.path.join(working_directory, file_path))

        if not file_path_abs.startswith(current_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(file_path_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file_path_abs, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) == MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
    

    except Exception as e:
        return f'Error: {e}'

    return file_content_string

def write_file(working_directory, file_path, content):

    try:
        current_dir = os.path.abspath(os.path.join(working_directory))
        file_path_abs = os.path.abspath(os.path.join(working_directory, file_path))

        if not file_path_abs.startswith(current_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(file_path_abs):
            os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)

        with open(file_path_abs, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'

    
schema_get_files_info = types.FunctionDeclaration(
name="get_files_info",
description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
        "directory": types.Schema(
            type=types.Type.STRING,
            description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
        ),
    },
),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the content of the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the specified content to the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)
