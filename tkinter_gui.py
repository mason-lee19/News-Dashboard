import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

BORDER_COLOR = 'White'
BORDER_THICKNESS = 2
BG_COLOR = 'gray15'
BG_WINDOW_COLOR = 'gray17'


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
        headline_window = HeadlineScrollWindow(root, width=left_right_width-inner_margin, height=left_right_large_height-inner_margin, 
                                               border_width=BORDER_THICKNESS, border_color=BORDER_COLOR)
        headline_window.place(x=margin, y=margin)
        headline_window.fill_with_headlines(headline_window)

        ### Portfolio based on headline ticker activity
        headline_portfolio = tk.Frame(root, width=left_right_width, height=left_right_small_height, 
                                      highlightthickness=BORDER_THICKNESS, highlightbackground=BORDER_COLOR)
        headline_portfolio.place(x=margin, y=margin + left_right_large_height + inner_margin)

        ### Keyword monitor window
        keyword_window = tk.Frame(root, width=left_right_width, height=left_right_large_height,
                                  highlightthickness=BORDER_THICKNESS, highlightbackground=BORDER_COLOR)
        keyword_window.place(x=self.width - left_right_width - margin, y=margin)

        ### Call Volume or top keyword window
        top_keywords = tk.Frame(root, width=left_right_width, height=left_right_small_height,
                                highlightthickness=BORDER_THICKNESS, highlightbackground=BORDER_COLOR)
        top_keywords.place(x=self.width - left_right_width - margin, y=margin + left_right_large_height + inner_margin)

        ### Ticker history viewer
        stock_history = tk.Frame(root, width=center_width, height=large_rect_height,
                                 highlightthickness=BORDER_THICKNESS, highlightbackground=BORDER_COLOR)
        stock_history.place(x=left_right_width + margin*2 + inner_margin, y=margin + inner_margin)

        ### Personal portfolio window
        personal_ticker_window = TickerGrid(root,width=center_width, height=small_rect_height,
                                            border_width=BORDER_THICKNESS, border_color=BORDER_COLOR)
        personal_ticker_window.place(x=left_right_width + margin*2 + inner_margin, y=margin + large_rect_height + 2 * inner_margin)
        personal_ticker_window.create_grid(personal_ticker_window)

        ### Bottom toolbar
        toolbar = tk.Frame(root,background=BG_COLOR)
        toolbar.pack(side=tk.BOTTOM)

        buttons = ['1D','1W','1M','3M','6M','1Y','5Y']

        for button_label in buttons:
            button = HighlightButton(toolbar, text=button_label,fg_color='transparent',width=12)
            button.pack(side=tk.LEFT,padx=10,pady=15)


class HeadlineScrollWindow(ctk.CTkScrollableFrame):
    def __init__(self,master=None,**kwargs):
        super().__init__(master,**kwargs)

        self.master = master

    def fill_with_headlines(self,frame):
        ### Will replace with db pull of headline data
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
            'TSLA\nTesla is absolutely goated with the sauce',
            'printing money just go easier with insurance fraud',
            'Magnificent 7 is still a great investment even though we are headed for recession',
            'Im hoping this tkinter thing works with long headlines',
            'JD\nJohn Deer goes the absolute moon thank god',
        ]

        for item in headlines:
            ctk.CTkLabel(frame,text=item,justify='left',wraplength=self.master.winfo_width()//6).pack(pady=4,anchor='w')


class HighlightButton(ctk.CTkButton):
    def __init__(self,master=None,**kwargs):
        super().__init__(master,**kwargs)
        self.master = master
        self.default_bg = BG_COLOR
        self.highlight_bg = 'gray25'

        self.configure(fg_color=self.default_bg)

        self.bind("<Button-1>", self.on_press)

    def on_press(self,event):
        ### Update to change time frame on press depending on button
        for button in self.master.winfo_children():
                button.configure(fg_color=self.default_bg)
        self.configure(fg_color=self.highlight_bg)

class TickerGrid(ctk.CTkFrame):
    def __init__(self,master=None,**kwargs):
        super().__init__(master,**kwargs)

    def create_grid(self,frame):
        ### Will replace with ticker pulling function
        tickers = {
            'AAPL': 1.23,
            'BA': -0.40,
            'GOOGL': 4.56,
            'TSLA': -3.87,
        }

        for i, (ticker,percentage) in enumerate(tickers.items()):
            ticker_label = tk.Label(frame, text=ticker,fg='white',padx=10,pady=5,bg=BG_WINDOW_COLOR)
            ticker_label.grid(row=i,column=0,sticky='w',padx=5,pady=5)

            percentage_label=tk.Label(frame,text=f'{percentage:.2f}%', fg=self.get_color(percentage),bg=BG_WINDOW_COLOR)
            percentage_label.grid(row=i, column=1,stick='w',padx=5,pady=5)

    def get_color(self, percentage) -> str:
        if percentage >= 0:
            return 'green'
        return 'red'
