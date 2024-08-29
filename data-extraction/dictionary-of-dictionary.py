import os

def get_files_info(path=None):
    """
    Generates a dictionary of dictionaries containing file information (path and size).
    
    Parameters:
    path (str): The directory path to search for files. Defaults to the current working directory if not provided.
    
    Returns:
    dict: A dictionary where each key is the file path and value is another dictionary with file details like 'size'.
    """
    
    # Use the provided path or default to the current working directory
    if path is None:
        path = os.getcwd()
    
    # Initialize an empty dictionary to store file information
    file_info_dict = {}

    # Walk through the directory tree
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Get the file size
            file_size = os.path.getsize(file_path)
            
            # Store the file information in a nested dictionary
            file_info_dict[file_path] = {
                'size': file_size
            }

    return file_info_dict

# Function to format the output to a readable form
def custom_format(file_info_dict):
    formatted_str = "{\n"
    for path, info in file_info_dict.items():
        formatted_str += f"   '{path}': {{\n"
        formatted_str += f"      'size': {info['size']}\n"
        formatted_str += "   },\n"
    formatted_str = formatted_str.rstrip(",\n")  # Remove the last comma and newline
    formatted_str += "\n}"
    return formatted_str

# Specify the path for which to gather file information
specified_path = r"C:\Users\1J8655897\Documents\Email Automation"

# Generate the dictionary of dictionaries for the specified path
files_info = get_files_info(specified_path)

# Print the formatted dictionary of dictionaries
print(custom_format(files_info))
