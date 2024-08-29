import os

def get_files_info(path=None):
    """
    Generates a list of dictionaries containing file information (path and size).
    
    Parameters:
    path (str): The directory path to search for files. Defaults to the current working directory if not provided.
    
    Returns:
    list: A list of dictionaries, each containing 'path' and 'size' for each file found.
    """
    
    # Use the provided path or default to the current working directory
    if path is None:
        path = os.getcwd()
    
    # Initialize an empty list to store file information
    file_info_list = []

    # Walk through the directory tree
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Get the file size
            file_size = os.path.getsize(file_path)
            
            # Append the file information as a dictionary to the list
            file_info_list.append({
                'path': file_path,
                'size': file_size
            })

    return file_info_list

# Function to format the output to a readable form
def custom_format(file_info_list):
    formatted_str = "[\n"
    for file_info in file_info_list:
        formatted_str += "   {\n"
        formatted_str += "      \"path\": \"" + file_info['path'] + "\",\n"
        formatted_str += "      \"size\": " + str(file_info['size']) + "\n"
        formatted_str += "   },\n"
    formatted_str = formatted_str.rstrip(",\n")  # Remove the last comma and newline
    formatted_str += "\n]"
    return formatted_str

# Specify the path for which to gather file information
specified_path = r"C:\Users\1J8655897\Documents\Email Automation"

# Generate the list of dictionaries for the specified path
files_info = get_files_info(specified_path)

# Print the formatted list of dictionaries
print(custom_format(files_info))
