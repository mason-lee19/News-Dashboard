import tkinter as tk
from tkinter import ttk

class GUI:
    def __init__(self,root):
        self.root = root
        self.root.title('News Dash')

        # Set the background color
        bg_color = "gray50"
        self.root.configure(bg=bg_color)
        
        # Get the dimensions of the root window
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        
        # Define some margins
        margin = 20
        inner_margin = 10

        # Define the widths and heights of the sections
        left_right_width = width // 6
        center_width = width - 2 * left_right_width - 5 * margin
        large_rect_height = (height - 6 * margin) * 3 // 4 - inner_margin
        small_rect_height = (height - 2 * margin) // 4 - inner_margin

        # Define the heights for left and right rectangles
        left_right_large_height = (height - 2 * margin - inner_margin) * 2 // 3
        left_right_small_height = (height - 2 * margin - inner_margin) // 3

        # Create and place the left column larger rectangle
        headline_window = tk.Frame(root, bg=bg_color, width=left_right_width, height=left_right_large_height, highlightbackground="white", highlightthickness=2)
        headline_window.place(x=margin, y=margin)

        # Create and place the left column smaller rectangle
        headline_portfolio = tk.Frame(root, bg=bg_color, width=left_right_width, height=left_right_small_height, highlightbackground="white", highlightthickness=2)
        headline_portfolio.place(x=margin, y=margin + left_right_large_height + inner_margin)

        # Create and place the right column larger rectangle
        keyword_window = tk.Frame(root, bg=bg_color, width=left_right_width, height=left_right_large_height, highlightbackground="white", highlightthickness=2)
        keyword_window.place(x=width - left_right_width - margin, y=margin)

        # Create and place the right column smaller rectangle
        top_keywords = tk.Frame(root, bg=bg_color, width=left_right_width, height=left_right_small_height, highlightbackground="white", highlightthickness=2)
        top_keywords.place(x=width - left_right_width - margin, y=margin + left_right_large_height + inner_margin)

        # Create and place the large rectangle in the center
        stock_history = tk.Frame(root, bg=bg_color, width=center_width, height=large_rect_height, highlightbackground="white", highlightthickness=2)
        stock_history.place(x=left_right_width + margin*2 + inner_margin, y=margin + inner_margin)

        # Create and place the small rectangle below the large rectangle
        personal_portfolio = tk.Frame(root, bg=bg_color, width=center_width, height=small_rect_height, highlightbackground="white", highlightthickness=2)
        personal_portfolio.place(x=left_right_width + margin*2 + inner_margin, y=margin + large_rect_height + 2 * inner_margin)

        '''
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH,expand=1)

        ##### Scrollable window #####
        
        # Create a canvas
        canvas = tk.Canvas(main_frame)
        canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

        # Add a scrollbard to the canvas
        scrollbar = ttk.Scrollbar(main_frame,orient=tk.VERTICAL,command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create another frame inside the canvas
        self.scrollable_frame = tk.Frame(canvas)

        # add that new frame to the window of the canvas
        canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")

        # Fill the frame with items
        for item in items:
            ttk.Label(self.scrollable_frame,text=item).pack(pady=5,padx=10,anchor='w')

        #################################
        '''

    def get_data(self):
        data1 = self.entry1.get()
        data2 = self.entry2.get()

        print(f"Data from box 1: {data1}")
        print(f"Data from box 2: {data2}")