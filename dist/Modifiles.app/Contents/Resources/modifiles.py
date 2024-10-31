import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import fileinput
# import subprocess
import platform


os_type = platform.system()
'''
GetText is a class created to handle the communication of user input to the main function. Within this class, all GUI interface
work is done.
'''
class GetText:
    def __init__(self, old="", new=""):
        self.old_content = old
        self.new_content = new
        self.old_text = None
        self.new_text = None
        self.nw_close = False
        self.types = []

        if old=="" or new=="":
            # Initialize new window and designate title
            self.get_text = tk.Tk() # Using 'self' here will allow for later access to this object
            self.get_text.title("Modifiles - Batch Directory Level Find and Replace")
            self.get_text.protocol("WM_DELETE_WINDOW", self.on_close)
            self.get_text.withdraw()
            
            notice = tk.Label(self.get_text, text="If you would like to delete a word, follow the example below:" +
                              "\n\nOld Text: super duper difficult\nNew Text: super difficult")
            notice.pack(pady=5)
            # Create frame to contain old info
            old_frame = tk.Frame(self.get_text)
            old_frame.pack(fill=tk.X, expand=True)

            # Create input label and input textbox
            old_text_label = tk.Label(old_frame, text="Please input the exact text you would like to replace:")
            old_text_label.pack(pady=5)
            self.old_text = tk.Text(old_frame, height=10, wrap=tk.WORD, borderwidth=2)
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
            self.new_text = tk.Text(new_frame, height=10, wrap=tk.WORD, borderwidth=2)
            self.new_text.pack(side=tk.LEFT, fill=tk.X, expand=True)  # Fill horizontal space and grow/shrink if window resized

            # Create new_text textbox scroll bar
            newt_sroller = tk.Scrollbar(new_frame, command=self.new_text.yview)
            newt_sroller.pack(side=tk.RIGHT, fill=tk.Y)

            # Configure textbox to respond to scrollbar
            self.new_text.config(yscrollcommand=newt_sroller.set)
            # print("Click button")
            enter = tk.Button(self.get_text, text="Submit", command=self.get_text_input).pack(pady=5)

        return
    
    '''
    Select the file extensions of desired files to be edited
    '''
    def select_type(self):
        self.choose_types = tk.Toplevel(self.get_text)
        self.choose_types.title("Modifiles - Type Selection")

        self.type_prompt = tk.Label(self.choose_types, text=f"Please select the file types in which you would like to replace text:")
        self.type_prompt.pack(pady=5)

        global all_text

        for type in all_text:
            file_type_var = tk.IntVar()
            self.types.append(file_type_var)
            file_type = tk.Checkbutton(self.choose_types, text=type, variable=file_type_var).pack(pady=5)
        
        tk.Button(self.choose_types, text="Submit", command=self.get_type_input).pack(pady=5)
        self.get_text.wait_window(self.choose_types)
        return

    '''
    If the user closes the window using the 'X' instead of selecting a directory, ask for confirmation of program cancellation
    '''
    def on_close(self):
        if messagebox.askokcancel("Quit", "Would you like to end the program?"):
            self.get_text.destroy()
            self.nw_close = True

    '''
    Get the user's checkbox inputs
    '''
    def get_type_input(self):
        global all_text
        global valid_extensions
        for type in range(len(self.types)):
            checkbox_id = self.types[type]
            if checkbox_id.get() == 1:
                extension = all_text[type]
                valid_extensions.add(extension)
        
        self.choose_types.destroy()
        print(valid_extensions)
        
    '''
    Get the old and new text inputs of the user for the program
    '''
    def get_text_input(self):
        self.old_content = self.old_text.get("1.0", "end-1c")
        self.new_content = self.new_text.get("1.0", "end-1c")
        
        '''
        Reset the text boxes to delete the red message text in the textboxes when the user begins to type.
        '''
        def reset_text(event):  # This event parameter is required by tkinter to accept the KeyPress event
            self.old_text.delete("1.0", tk.END)
            self.new_text.delete("1.0", tk.END)

            # Unbind the keypress event to prevent continuous triggering
            self.old_text.unbind("<KeyPress>")
            self.new_text.unbind("<KeyPress>")

            self.old_text.tag_remove("no_old_input", "1.0", tk.END)
            self.new_text.tag_remove("no_new_input", "1.0", tk.END)
            return
        
        '''
        If no old text is input, display a message to the user to input before submission. Allows empty input for new text
        TODO: deal with cases in which a user wants to delete the old text by having no input
        '''
        def red_text():
            if (self.old_content == "") or (self.old_content == "Please input text to be replaced by Modifiles."):
                self.old_text.tag_configure("no_old_input", foreground="red")
                self.old_text.delete("1.0", tk.END)
                self.old_text.insert(tk.END, "Please input text to be replaced by Modifiles.", "no_old_input")
            if (self.new_content == "") or (self.new_content == "Please input replacement text for Modifiles."):
                self.new_text.tag_configure("no_new_input", foreground="red")
                self.new_text.delete("1.0", tk.END)
                self.new_text.insert(tk.END, "Please input replacement text for Modifiles.", "no_new_input")
            return
        
        self.old_text.bind("<KeyPress>", reset_text)
        self.new_text.bind("<KeyPress>", reset_text)
        red_text()
        
        if (self.old_content != "") and (self.old_content != "Please input text to be replaced by Modifiles."):
            print("Got Text")
            self.get_text.destroy()
        
        return
    
    '''
    Display to the user what files have been edited by the application.
    '''
    def show_updates(self, edited):
        # print("Begin update")
        def label_wraplength():
            message_width = message.winfo_width()
            changes.config(wraplength=message_width)
        
        def _on_mouse_wheel(event):
            os_type = platform.system()
        
            # Bind mouse wheel events for scrolling
            if (os_type == "Windows"):
                canvas.yview_scroll(int(-1 * (event.delta/120)), "units")
            elif (os_type == "Darwin"):
                canvas.yview_scroll(int(-1 * (event.delta)), "units")
            elif os_type == "Linux":
                if event.num == 5:
                    canvas.yview_scroll(1, "units")
                elif event.num == 4:
                    canvas.yview_scroll(-1, "units")

        self.uwindow = tk.Tk() # Using 'self' here will allow for later access to this object
        self.uwindow.title("Modifiles - Batch Directory Level Find and Replace")
        self.uwindow.minsize(400, 150)
        self.modifiles = tk.Toplevel()
        self.modifiles.title("Modifiles - Batch Directory Level Find and Replace")
        self.modifiles.minsize(200, 150)
        
        canvas = tk.Canvas(self.modifiles)
        cscrollbar = tk.Scrollbar(self.modifiles, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=cscrollbar.set)
        cframe = tk.Frame(canvas)

        cframe.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
                         add="+")
        cframe.bind("<Configure>", lambda e: canvas.config(width=e.width), add="+")

        canvas.create_window((0, 0), window=cframe, anchor="nw", tags="cframe")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        
        # Create input label and input textbox
        message = tk.Label(cframe, text=f"All files modified. Thank you for your patronage!\n\n The specified text below has been replaced in all files of your chosen directory:\n")
        message.pack(pady=5)
        changes = tk.Label(cframe, text=f"Previous Text:\n{self.old_content}\n\nNew Text:\n{self.new_content}",
                            justify="left", anchor="w", wraplength=message.winfo_width())
        self.modifiles.after(100, label_wraplength)
        changes.pack(pady=5, padx=10)
        self.modifiles.update_idletasks()
        canvas.config(width=cframe.winfo_width())

        os_type = platform.system()
        
        # Bind mouse wheel events for scrolling
        if (os_type == "Windows") or (os_type == "Darwin"):
            canvas.bind_all("<MouseWheel>", _on_mouse_wheel)  # For Windows and macOS
        elif os_type == "Linux":
            canvas.bind_all("<Button-4>", _on_mouse_wheel)
            canvas.bind_all("<Button-5>", _on_mouse_wheel)
        else:
            pass

        allfiles = tk.Label(self.uwindow, text=f"Below are all the files that were modified:\n\n{edited}", justify="left")
        allfiles.pack(pady=5)

        tk.Button(self.uwindow, text="Close", command=self.uwindow.destroy).pack(pady=5)
        tk.Button(cframe, text="Close", command=self.modifiles.destroy).pack(pady=5)
        self.modifiles.focus_force()
        self.uwindow.mainloop()
        print("End update")
        return
    
    '''
    Prompt and enable the user to select the folder they want to conduct a find and replace on.
    '''
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
    
''' Global Variables'''
edited_files = []
all_text = ['.csv', '.docx', '.html', '.md', '.pdf', '.py', '.txt', '.xml']
valid_extensions = set()

'''
The main function of modifiles that conducts the directory-level find and replace.
'''
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
        input_text.select_type()
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
            
            global valid_extensions
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
        print("Update window here")
        input_text.show_updates(edited=allfiles)
    valid_extensions.clear
    return

if __name__ == "__main__":
    directory_filetext_replace()