import os
from config import MAX_CHARS

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

    
    

