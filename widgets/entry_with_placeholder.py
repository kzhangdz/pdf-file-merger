import tkinter as tk
from tkinter import ttk

DEFAULT_STYLE_NAME = "TEntry"

class EntryWithPlaceholder(ttk.Entry):

    def __init__(self, parent=None, placeholder="PLACEHOLDER", color='grey'):

        self.parent = parent

        self.placeholder = placeholder
        self.placeholder_color = color

        # configure the ttk.Entry colors using Style
        self.style_name = ".".join([color, DEFAULT_STYLE_NAME]) #i.e. grey.TEntry. Must follow a pattern of descriptor.Widget
        self.entry_style = ttk.Style()
        self.entry_style.configure(self.style_name, foreground=self.placeholder_color)
        self.current_style = self.style_name

        # set up the Entry using the created style.
        super().__init__(parent, style=self.style_name)

        # TODO: the style seems to get overwritten by sv_ttk. doing a config on the foreground allows it to change
        # self.config(foreground=color)

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        # use the placeholder style, and input the placeholders
        self.current_style = self.style_name
        self.config(style=self.style_name)

        self.insert(0, self.placeholder)

    def foc_in(self, *args):
        # if using the placeholder style, switch to the default style for text entry
        if self.current_style == self.style_name:
            self.current_style = DEFAULT_STYLE_NAME
            self.config(style=DEFAULT_STYLE_NAME)
            # self.config(foreground='white')

            self.delete('0', 'end')

    def foc_out(self, *args):
        # if no text in the entry box, add the placeholder
        if not self.get():
            self.put_placeholder()

if __name__ == "__main__": 
    root = tk.Tk() 
    username = EntryWithPlaceholder(root, "username")
    password = EntryWithPlaceholder(root, "password", 'blue')
    username.pack()
    password.pack()  
    root.mainloop()