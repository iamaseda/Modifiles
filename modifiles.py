import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import fileinput
# import subprocess
# import platform


class GetText:
    def __init__(self, old="", new=""):
        self.old_content = old
        self.new_content = new
        self.old_text = None
        self.new_text = None
        self.nw_close = False
        if old=="" or new=="":
            # Initialize new window and designate title
            self.get_text = tk.Tk() # Using 'self' here will allow for later access to this object
            self.get_text.title("Modifiles - Batch Directory Level Find and Replace")
            self.get_text.protocol("WM_DELETE_WINDOW", self.on_close)
            self.get_text.withdraw()

            # self.get_text.withdraw()

            # Create frame to contain old info
            old_frame = tk.Frame(self.get_text)
            old_frame.pack(fill=tk.X, expand=True)

            # Create input label and input textbox
            old_text_label = tk.Label(old_frame, text="Please input the exact text you would like to replace:")
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
            # print("Click button")
            enter = tk.Button(self.get_text, text="Submit", command=self.get_text_input).pack(pady=5)

        return
    def on_close(self):
        if messagebox.askokcancel("Quit", "Would you like to end the program?"):
            self.get_text.destroy()
            self.nw_close = True
    def get_text_input(self):
            self.old_content = self.old_text.get("1.0", "end-1c")
            self.new_content = self.new_text.get("1.0", "end-1c")
            
            def reset_text(event):  # This event parameter is required by tkinter to accept the KeyPress event
                self.old_text.delete("1.0", tk.END)
                self.new_text.delete("1.0", tk.END)

                # Unbind the keypress event to prevent continuous triggering
                self.old_text.unbind("<KeyPress>")
                self.new_text.unbind("<KeyPress>")

                self.old_text.tag_remove("no_old_input", "1.0", tk.END)
                self.new_text.tag_remove("no_new_input", "1.0", tk.END)
                return
            
            def red_text():
                if self.old_content == "":
                    self.old_text.tag_configure("no_old_input", foreground="red")
                    self.old_text.insert(tk.END, "Please input text to be replaced.", "no_old_input")
                if self.new_content == "":
                    self.new_text.tag_configure("no_new_input", foreground="red")
                    self.new_text.insert(tk.END, "Please input replacement text.", "no_new_input")
                return
            
            red_text()
            self.old_text.bind("<KeyPress>", reset_text)
            self.new_text.bind("<KeyPress>", reset_text)
            if self.old_content != "":
                self.get_text.destroy()
            # print("Got Text")
            return
    
    def show_updates(self, edited):
        # print("Begin update")
        
        self.uwindow = tk.Tk() # Using 'self' here will allow for later access to this object
        self.uwindow.title("Modifiles - Batch Directory Level Find and Replace")
        self.uwindow.minsize(400, 150)
        self.modifiles = tk.Toplevel()
        self.modifiles.title("Modifiles - Batch Directory Level Find and Replace")
        self.modifiles.minsize(200, 150)
        # Create input label and input textbox
        message = tk.Label(self.modifiles, text=f"All files modified. Thank you for your patronage!\n\n The specified text below has been replaced in all files of your chosen directory:\n\n")
        message.pack(pady=5)
        changes = tk.Label(self.modifiles, text=f"Previous Text:\n{self.old_content}\n\nNew Text:\n{self.new_content}", justify="left", anchor="w")
        changes.pack(pady=5)
        allfiles = tk.Label(self.uwindow, text=f"Below are all the files that were modified:\n\n{edited}", justify="left")
        allfiles.pack(pady=5)

        tk.Button(self.uwindow, text="Close", command=self.uwindow.destroy).pack(pady=5)
        tk.Button(self.modifiles, text="Close", command=self.modifiles.destroy).pack(pady=5)
        self.modifiles.focus_force()
        self.uwindow.mainloop()
        # print("End update")
        return

    def choose_directory(self):
            choose = tk.Toplevel()
            choose.withdraw()
            def close_choose(window):
                window.destroy()
                self.get_text.destroy()
                return
            # Open directory selection
            selected = filedialog.askdirectory()
            if selected == "":
                choose.deiconify()
                choose.lift()
                choose.minsize(250, 100)

                frame = tk.Frame(choose)
                frame.pack(expand=True)

                tk.Label(choose, text="No directory was selected").pack(expand=True)
                tk.Button(choose, text="Close", command=lambda: close_choose(choose)).pack(expand=True)
                choose.mainloop()
                # print("No directory was selected")
                return ""
            else:
                choose.destroy()
            return selected
edited_files = []
def directory_filetext_replace(directory=None, old="", new="", root=True):
    # machine = platform.system() # No longer need to check for machine platform
    # print(f"Directory function started: {directory}")
    input_text = GetText(old, new)
    
    if directory == None:
        # print(f"choose directory")
        directory = input_text.choose_directory()
        # print("Directory done")
        if directory == "": # TODO: fix this!!!
            return
        
        # print(f"done choosing, Now popup")
        input_text.get_text.deiconify()

    print(f"[{input_text.old_content} -> {input_text.new_content}]")
    if input_text.old_content == "" and input_text.new_content == "":
        input_text.get_text.mainloop()
        if input_text.nw_close:
            return
    global edited_files

    # print("Start for in directory")
    # print(f"{input_text.old_content} -> {input_text.new_content}")
    for file in os.listdir(directory):
        # print(f"File/folder {file}")
        filepath = os.path.join(directory, file)
        has_text = False

        if os.path.isfile(filepath):
            '''TODO: implement ability to select what types of files the user wants to edit rather than hardcoding the three main ones
            if xyz is checked:
                valid_extensions.add(xyz)
            '''
            all_text = {'.txt', '.docx', '.pdf', '.html', '.md', '.csv', '.xml'}
            valid_extensions = {}
            _, extension = os.path.splitext(file)

            if extension not in valid_extensions:
                continue

            try:
                
                with fileinput.FileInput(filepath, inplace=True, backup='.bak') as filetext:
                    for line in filetext:
                        print(line.replace(input_text.old_content, input_text.new_content), end="")
                        if not has_text:
                            if input_text.old_content in line:
                                edited_files.append(file)
                                has_text = True
                # print("Checked for text")
            except FileNotFoundError:
                print(f"Error: File not found: {filepath}")

        elif os.path.isdir(filepath):
            # print(filepath)
            directory_filetext_replace(filepath, input_text.old_content, input_text.new_content, False)

    # print("All files parsed")
    allfiles = ""
    try:
        # print(f"Start edited files log: {edited_files}")
        with open("log-files-replaced.txt", "w") as editedFiles:
            count = 1
            for elem in edited_files:
                allfiles += f"{count}. {str(elem)}\n"
                count += 1
            editedFiles.write(allfiles)
        print(f"Successss: {allfiles}")
    except Exception as e:
        print(f"An error has occcured: {e}")
    if root:
        # print("Update window here")
        input_text.show_updates(edited=allfiles)

    return

if __name__ == "__main__":
    directory_filetext_replace()