import os

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