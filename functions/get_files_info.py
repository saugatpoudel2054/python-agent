import os
from config import MAX_CHARS
from google.genai import types

def get_files_info(working_directory, directory):
    working_path = os.path.abspath(working_directory)
    working_dir_contents = os.listdir(working_path)
    working_dir_contents.append(".")
    if directory not in working_dir_contents:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    path = os.path.join(working_path, directory)
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'

    dir_contents = os.listdir(path)
    if len(dir_contents) == 0:
        return f'Error: "{directory}" is empty'

    try:
        files_info: list[str] = []
        for entry in dir_contents:
            entry_path = os.path.join(path, entry)
            file_size = os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)
            files_info.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_path = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_path, file_path))

        if not full_path.startswith(working_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(full_path, 'r') as f:
            file_contents = f.read(MAX_CHARS)

        if len(file_contents) == 10_000:
            file_contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_contents
    except Exception as e:
        return f"Error: {e}"

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_path = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_path, file_path))

        if not full_path.startswith(working_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(os.path.dirname(full_path)):
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'w') as f:
            _ = f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description='The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself (use ".").',
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write the content to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content you want to write into a file.",
            ),
        },
        required=["file_path", "content"],
    ),
)
