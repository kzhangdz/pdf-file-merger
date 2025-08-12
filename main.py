import tkinter.font as tkFont
import tkinter as tk
from tkinter import ttk, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD # used to allow drag and drop
import sv_ttk # styling package

from widgets.entry_with_placeholder import EntryWithPlaceholder

from collections.abc import Callable
from functools import partial # for callback functions in buttons, with arguments
from pathlib import Path
from pypdf import PdfWriter
from typing import List, Dict

#https://www.youtube.com/watch?v=VEdaDzI9rJM

DEFAULT_PADDING = 20
DEFAULT_BUTTON_WIDTH = 7
DEFAULT_FONT = "Arial"

def main():
    app = Application()
    app.mainloop()

class Application(TkinterDnD.Tk): # can inherit, so our application itself is a tkinter Tk instance

    def __init__(self):
        super().__init__()

        self.title("PDF File Merger")
        sv_ttk.set_theme("dark")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.main_frame = MainPage(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.geometry("900x500")
    
class MainPage(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.list_frame = ttk.Frame(self)
        self.file_names_listbox = FileNamesListbox(self.list_frame)
        self.file_names_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.button_section = ButtonSection(
            self.list_frame, 
            on_add_click=self.browse_files,
            on_remove_click=self.remove_files
        )
        self.button_section.pack(side=tk.RIGHT, padx=DEFAULT_PADDING)
        self.list_frame.pack(fill=tk.BOTH, expand=True)

        self.bottom_frame = ttk.Frame(self)
        self.target_file_selection_box = TargetFileSelectionBox(self.bottom_frame)
        self.target_file_selection_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.merge_section = MergeSection(self.bottom_frame, callback=lambda: self.merge_files(self.file_names_listbox.get_content(), self.target_file_selection_box.get_save_path()))
        self.merge_section.pack(side=tk.RIGHT)
        self.bottom_frame.pack(fill=tk.BOTH)

        self.message = tk.StringVar()
        self.message.set("")
        self.message_section = MessageSection(self, message=self.message, height=100)
        self.message_section.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def browse_files(self):
        files = filedialog.askopenfilenames(
            title="Select PDF files to merge",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if files:
            for file in files:
                self.file_names_listbox.file_names_listbox.insert(tk.END, file)
                print("Adding", file)

    def remove_files(self):
        selected = self.file_names_listbox.get_selected_indices()
        print(selected)
        self.file_names_listbox.delete_items(selected)

    def merge_files(self, files: List[str], save_path: str):

        if len(files) == 0:
            self.message.set("Please add PDF files to merge")
            return

        if save_path == "":
            self.message.set("Please specify a save path")
            return

        if not save_path.lower().endswith('.pdf'):
            self.message.set("Must save to a pdf file")
            return
        
        print("Merging Files")
        
        merger = PdfWriter()

        for file in files:
            merger.append(file)
            print("Appending", file)

        try:
            merger.write(save_path)
            print("Written to", save_path)

            # modify the display message
            self.message.set(f"Successfully written to {save_path}")
        except:
            self.message.set("Error occurred when merging")

        merger.close()

class ButtonSection(ttk.Frame):

    def __init__(self, parent, on_add_click: Callable[..., None]=None, on_remove_click: Callable[..., None]=None):
        super().__init__(parent)

        self.add_button = ttk.Button(self, text="Add", command=on_add_click)

        self.delete_button = ttk.Button(self, text="Remove", command=on_remove_click)

        buttons = [self.add_button, self.delete_button]
        for button in buttons:
            button.config(width=DEFAULT_BUTTON_WIDTH)
            button.pack(pady=DEFAULT_PADDING/4)

class MessageSection(ttk.Frame):

    def __init__(self, parent, message, **kwargs):
        super().__init__(parent, **kwargs)

        title_font = tkFont.Font(font=DEFAULT_FONT, size=12)
        self.message_section = tk.Message(self, textvariable=message, width=600, font=title_font)
        self.message_section.pack(fill=tk.BOTH, pady=DEFAULT_PADDING/5)

class MergeSection(ttk.Frame):

    def __init__(self, parent, callback):
        super().__init__(parent)

        self.merge_button = ttk.Button(self, text="Merge", command=callback)
        self.merge_button.config(width=DEFAULT_BUTTON_WIDTH)
        self.merge_button.pack()

class TargetFileSelectionBox(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        # entry + Browse Button
        self.entry = EntryWithPlaceholder(self, placeholder="Choose Save Path")
        self.browse_button = ttk.Button(self, text="Browse", command=self.browse_file)
        self.browse_button.config(width=DEFAULT_BUTTON_WIDTH)

        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.browse_button.pack(side=tk.RIGHT)

    def browse_file(self):
        file_path = filedialog.asksaveasfilename(
            title="Select PDF file to write to",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")]
            )
        
        if file_path:
            # Place the file path in the widget
            print("Selected save path:", file_path)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, file_path)

    def get_save_path(self):
        return self.entry.get()

class FileNamesListbox(ttk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        # main listbox
        title_font = tkFont.Font(font=DEFAULT_FONT, size=12)
        self.file_names_listbox = tk.Listbox(self, selectmode=tk.MULTIPLE, font=title_font)
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)

        # connect listbox and scrollbar
        self.file_names_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.file_names_listbox.yview)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y) # fill vertically
        self.file_names_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # fill horizontally and vertically

        self.file_names_listbox.drop_target_register(DND_FILES)
        self.file_names_listbox.dnd_bind('<<Drop>>', self.drop_inside_list_box)

    def drop_inside_list_box(self, event):
        # get a list of file names. Helps handle cases with space in the file name
        files = self.tk.splitlist(event.data)

        #TODO: logic to not allow duplicates?

        for file in files:

            file_extension = Path(file).suffix

            if file_extension == ".pdf":
                self.file_names_listbox.insert(tk.END, file)
                print("Adding", file)
            else:
                print("Skipping", file)

    def get_content(self):
        return self.file_names_listbox.get(0, tk.END)
    
    def get_selected_indices(self):
        selected = []

        for i in self.file_names_listbox.curselection():
            selected.append(i)

        return selected
    
    def get_selected(self):
        
        selected = []

        for i in self.file_names_listbox.curselection():
            selected.append(self.file_names_listbox.get(i))

        return selected
    
    def delete_items(self, indices=None):
        
        # delete all
        if indices == None:
            self.file_names_listbox.delete(0, tk.END)
        
        # delete specific indices
        elif indices:
            # indices can change, so iterate from highest to lowest index
            sorted_indices = sorted(indices, reverse=True)

            for i in sorted_indices:
                self.file_names_listbox.delete(i)

        # delete nothing on an empty list
        

if __name__ == "__main__":
    main()
