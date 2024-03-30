import os

DIRECTORY_PATH = "./tasks"

def file_browser():
    files = os.listdir(DIRECTORY_PATH)
    if len(files) == 0:
        print("No files found in source directory")
        exit()

    print("Available files:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    
    input_choice = 0
    while input_choice < 1 or input_choice > len(files):
        try:
            input_choice = int(input("Task chosen:"))
            if 1 <= input_choice <= len(files):
                chosen_file = files[input_choice - 1]
                print(f"Selected file {input_choice}")
            else:
                print("Select a valid file choice") 
        except ValueError:
            print("Invalid input type") 
        
    return chosen_file

if __name__ == "__main__":
    file_browser()