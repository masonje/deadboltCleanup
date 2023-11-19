import os

def list_all_files_and_folders(directory):
    result = []
    
    def recursive_list(current_directory):
        try:
            with os.scandir(current_directory) as entries:
                for entry in entries:
                    result.append(entry.path)
                    if entry.is_dir():
                        recursive_list(entry.path)
        except FileNotFoundError:
            print(f"The specified directory '{current_directory}' was not found.")

    # Start the recursive listing
    recursive_list(directory)
    return result

# Example usage:
directory_path = "/run/user/1000/gvfs/smb-share:server=nas.local,share=pictures/CameraUploads"
result_list = list_all_files_and_folders(directory_path)
for item in result_list:
    print(item)

