import os

# Initialize an empty list to hold the file information dictionaries
files_info = []

# Get the current working directory
current_directory = os.getcwd()

# List all files and directories in the current directory
all_entries = os.listdir(current_directory)

# Iterate over each entry
for entry in all_entries:
    # Construct full path
    full_path = os.path.join(current_directory, entry)
    
    # Check if it's a file
    if os.path.isfile(full_path):
        # Get the file size
        file_size = os.path.getsize(full_path)
        
        # Create a dictionary with file path and size
        file_info = {'path': full_path, 'size': file_size}
        
        # Append the dictionary to the list
        files_info.append(file_info)

# Print the list of dictionaries
print(files_info)
