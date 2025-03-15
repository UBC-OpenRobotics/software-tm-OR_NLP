import os

DIRECTORY_PATH = "./tasks"

def file_browser():
    # get files (tasks)
    files = os.listdir(DIRECTORY_PATH)
    if len(files) == 0:
        print("No files found!")
        exit() # terminate whole program

    print("Available files:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    
    # select desired file
    input_choice = 0
    while input_choice < 1 or input_choice > len(files):
        try:
            # prompt user to select file
            input_choice = int(input("Task chosen:"))
            if 1 <= input_choice <= len(files):
                chosen_file = files[input_choice - 1]
                print(f"Selected file: {input_choice}. {chosen_file}")
            else:
                print(f"Select a valid file choice. Must be between 1 and {len(files)}") 
        except ValueError:
            print("Invalid input type") 
        
    return chosen_file

if __name__ == "__main__":
    file_browser()