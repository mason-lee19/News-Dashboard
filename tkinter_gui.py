import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

class GUI:
    def __init__(self,root):
        self.root = root
        self.root.title('News Dash')

        # Set the background color
        self.root.configure()
        
        # Get the dimensions of the root window
        root.update_idletasks()
        self.width = root.winfo_width()
        self.height = root.winfo_height()
        
        # Define some margins
        margin = 20
        inner_margin = 10

        # Define the widths and heights of the sections
        left_right_width = self.width // 6
        center_width = self.width - 2 * left_right_width - 5 * margin
        large_rect_height = (self.height - 6 * margin) * 3 // 4 - inner_margin
        small_rect_height = (self.height - 2 * margin) // 4 - inner_margin

        # Define the heights for left and right rectangles
        left_right_large_height = (self.height - 2 * margin - inner_margin) * 2 // 3
        left_right_small_height = (self.height - 2 * margin - inner_margin) // 3

        ### Headline scroll window
        # Create and place the left column larger rectangle
        headline_window = ctk.CTkScrollableFrame(root, width=left_right_width, height=left_right_large_height, border_color='red')
        headline_window.place(x=margin, y=margin)
  
        # Fill the frame with headlines
        self.fill_with_headlines(headline_window)

        # Create and place the left column smaller rectangle
        headline_portfolio = tk.Frame(root, width=left_right_width, height=left_right_small_height, highlightbackground="white", highlightthickness=2)
        headline_portfolio.place(x=margin, y=margin + left_right_large_height + inner_margin)

        # Create and place the right column larger rectangle
        keyword_window = tk.Frame(root, width=left_right_width, height=left_right_large_height, highlightbackground="white", highlightthickness=2)
        keyword_window.place(x=self.width - left_right_width - margin, y=margin)

        # Create and place the right column smaller rectangle
        top_keywords = tk.Frame(root, width=left_right_width, height=left_right_small_height, highlightbackground="white", highlightthickness=2)
        top_keywords.place(x=self.width - left_right_width - margin, y=margin + left_right_large_height + inner_margin)

        # Create and place the large rectangle in the center
        stock_history = tk.Frame(root, width=center_width, height=large_rect_height, highlightbackground="white", highlightthickness=2)
        stock_history.place(x=left_right_width + margin*2 + inner_margin, y=margin + inner_margin)

        # Create and place the small rectangle below the large rectangle
        personal_portfolio = tk.Frame(root, width=center_width, height=small_rect_height, highlightbackground="white", highlightthickness=2)
        personal_portfolio.place(x=left_right_width + margin*2 + inner_margin, y=margin + large_rect_height + 2 * inner_margin)

        # Bottom toolbar
        toolbar = tk.Frame(root,background='gray15')
        toolbar.pack(side=tk.BOTTOM)

        buttons = ['1D', '1W', '1M', '3M', '6M', '1Y', '5Y']

        for button_label in buttons:
            button = HighlightButton(toolbar, text=button_label,fg_color='transparent',width=12)
            button.pack(side=tk.LEFT,padx=10,pady=15)

    def fill_with_headlines(self,frame):
        headlines = [
            'BA\nBoeing goes the absolute moon thank god',
            'printing money just go easier with insurance fraud',
            'Magnificent 7 is still a great investment even though we are headed for recession',
            'Im hoping this tkinter thing works with long headlines',
            'TSLA\nTesla is absolutely goated with the sauce',
            'printing money just go easier with insurance fraud',
            'Magnificent 7 is still a great investment even though we are headed for recession',
            'Im hoping this tkinter thing works with long headlines',
            'JD\nJohn Deer goes the absolute moon thank god',
        ]

        for item in headlines:
            ctk.CTkLabel(frame,text=item,justify='left',wraplength=self.width//6).pack(pady=4,anchor='w')


class HighlightButton(ctk.CTkButton):
    def __init__(self,master=None,**kwargs):
        super().__init__(master,**kwargs)
        self.master = master
        self.default_bg = 'gray15'
        self.highlight_bg = 'gray25'

        self.configure(fg_color=self.default_bg)

        self.bind("<Button-1>", self.on_press)

    def on_press(self,event):
        for button in self.master.winfo_children():
                button.configure(fg_color=self.default_bg)
        self.configure(fg_color=self.highlight_bg)