import os
import json

def get_files_info():
    # Get the current working directory
    current_directory = os.getcwd()
    
    # Initialize an empty list to store file information
    file_info_list = []

    # Loop through all items in the current directory
    for item in os.listdir(current_directory):
        item_path = os.path.join(current_directory, item)
        
        # Check if the item is a file (not a directory)
        if os.path.isfile(item_path):
            # Get the file size
            file_size = os.path.getsize(item_path)
            
            # Append the file information as a dictionary to the list
            file_info_list.append({
                'path': item_path,
                'size': file_size
            })

    return file_info_list

# Generate the list of dictionaries
files_info = get_files_info()

# Custom formatting function to print each dictionary on a single line
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

# Print the formatted list as a 'Dictionary'.
print(custom_format(files_info))
