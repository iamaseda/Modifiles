import os
import tkinter as tk
from tkinter import filedialog
import fileinput
# import subprocess
# import platform


class GetText:
    def __init__(self):
        self.old_content = ""
        self.new_content = ""
        self.old_text = None
        self.new_text = None
    
    def text_popup(self):
        # Initialize new window and designate title
        self.get_text = tk.Tk() # Using 'self' here will allow for later access to this object
        self.get_text.title("Find and Replace")

        # Create frame to contain old info
        old_frame = tk.Frame(self.get_text)
        old_frame.pack(fill=tk.X, expand=True)

        # Create input label and input textbox
        old_text_label = tk.Label(old_frame, text="Please input the text you would like to replace:")
        old_text_label.pack(pady=5)
        self.old_text = tk.Text(old_frame, wrap=tk.WORD, borderwidth=2)
        self.old_text.pack(side=tk.LEFT, fill=tk.X, expand=True)  # Fill horizontal space and grow/shrink if window resized

        # Create old_text textbox scroll bar
        oldt_sroller = tk.Scrollbar(old_frame, command=self.old_text.yview)
        oldt_sroller.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure textbox to respond to scrollbar
        self.old_text.config(yscrollcommand=oldt_sroller.set)

        # Create frame to contain new info
        new_frame = tk.Frame(self.get_text)
        new_frame.pack(fill=tk.X, expand=True)

        # Create input label and input textbox
        new_text_label = tk.Label(new_frame, text="Please input your updated text:")
        new_text_label.pack(pady=5)
        self.new_text = tk.Text(new_frame, wrap=tk.WORD, borderwidth=2)
        self.new_text.pack(side=tk.LEFT, fill=tk.X, expand=True)  # Fill horizontal space and grow/shrink if window resized

        # Create new_text textbox scroll bar
        newt_sroller = tk.Scrollbar(new_frame, command=self.new_text.yview)
        newt_sroller.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure textbox to respond to scrollbar
        self.new_text.config(yscrollcommand=newt_sroller.set)
        
        submit_info = tk.Button(self.get_text, text="Submit", command=self.get_text_input)
        self.get_text.mainloop()

        return submit_info
    
    def get_text_input(self):
            self.old_content = self.old_text.get("1.0", "end-1c")
            self.new_content = self.new_text.get("1.0", "end-1c")
            self.get_text.destroy()
            return

def choose_directory():
        root = tk.Tk()
        root.withdraw()

        # Open directory selection
        selected = filedialog.askdirectory()

        return selected

def directory_filetext_replace(directory=None):
    # machine = platform.system() # No longer need to check for machine platform
    input_text = GetText()
    if directory == None:
        directory = choose_directory()
        input_text.text_popup()

    for file in os.listdir(directory):
        filepath = os.path.join(directory, file)

        if os.path.isfile(filepath):
            valid_extensions = {'.txt', '.docx', '.pdf'}
            _, extension = os.path.splitext(file)

            if extension not in valid_extensions:
                return

            try:
                
                with fileinput.FileInput(file, inplace=True, backup='.bak') as filetext:
                    for line in filetext:
                        print(line.replace(input_text.old_content, input_text.new_content), end="")

            except FileNotFoundError:
                print(f"Error: File not found: {filepath}")

        elif os.path.isdir(filepath):
            directory_text_replace(filepath)