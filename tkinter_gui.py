import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

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
        headline_window = ScrollWindow(root, label_text='Headlines', width=left_right_width-inner_margin, height=left_right_large_height-(inner_margin*6), 
                                               border_width=BORDER_THICKNESS, border_color=BORDER_COLOR)
        headline_window.place(x=margin, y=margin)
        headline_window.fill_with_headlines(headline_window)

        ### Portfolio based on headline ticker activity
        headline_portfolio = tk.Frame(root, width=left_right_width, height=left_right_small_height, 
                                      highlightthickness=BORDER_THICKNESS, highlightbackground=BORDER_COLOR)
        headline_portfolio.place(x=margin, y=margin + left_right_large_height + inner_margin)

        ### Keyword monitor window
        keyword_window = KeywordWindow(root, width=left_right_width+inner_margin, height=left_right_large_height,
                                       border_width=BORDER_THICKNESS, border_color=BORDER_COLOR)
        keyword_window.place(x=self.width - left_right_width - margin - inner_margin, y=margin)
        keyword_grid = KeywordWindow(root, width=left_right_width-inner_margin-10, height=left_right_large_height-(inner_margin*2)-10)
        keyword_grid.place(x=self.width - left_right_width - margin, y=margin + 10)

        keyword_grid.fill_with_keywords(keyword_grid)

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
        ticker_grid_frame = TickerGrid(root,width=center_width-10, height=small_rect_height-10)
        ticker_grid_frame.place(x=left_right_width + margin*2+35 + inner_margin, y=margin + large_rect_height + 2 * inner_margin+10)
        personal_ticker_window.place(x=left_right_width + margin*2 + inner_margin, y=margin + large_rect_height + 2 * inner_margin)
        personal_ticker_window.create_grid(ticker_grid_frame)

        ### Bottom toolbar
        toolbar = tk.Frame(root,background=BG_COLOR)
        toolbar.pack(side=tk.BOTTOM)

        buttons = ['1D','1W','1M','3M','6M','1Y','5Y']

        for button_label in buttons:
            button = HighlightButton(toolbar, text=button_label,fg_color='transparent',width=12)
            button.pack(side=tk.LEFT,padx=10,pady=15)


class ScrollWindow(ctk.CTkScrollableFrame):
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


class KeywordWindow(ctk.CTkFrame):

    def __init__(self,master=None,**kwargs):
        super().__init__(master,**kwargs)

        self.master = master

    def fill_with_keywords(self,frame):
        ### Will replace with db pull of headline data
        keywords = {
            'nvidia':[1,2,4,6,3,2,1],
            'mason':[5,2,3,5,6,8],
            'russia':[9,7,4,1,2,3],
            'yemen':[4,6,1,3,7,8],
            'flu':[7,5,2,4,5,1],
        }


        for i, (word,data) in enumerate(keywords.items()):
            keyword_label = tk.Label(frame,text=word,justify='left',bg=BG_WINDOW_COLOR)
            #.pack(pady=4,anchor='w')
            keyword_label.grid(row=i,column=0,stick='w',padx=5,pady=5)

            graph_image = f'attachments/graph_{i}.png'

            self.create_chart(data,graph_image)
            img = Image.open(graph_image)
            img = ImageTk.PhotoImage(img)

            graph_label = tk.Label(frame,image=img,bg=BG_WINDOW_COLOR)
            graph_label.image = img
            graph_label.grid(row=i,column=2,stick='w',padx=30,pady=5)

    def create_chart(self,data,filename):
            color = 'green' if data[0] <= data[-1] else 'red'
            fig,ax = plt.subplots(figsize=(1,0.4))
            ax.bar(range(len(data)),data,color=color)
            ax.set_axis_off()
            plt.savefig(filename,bbox_inches='tight',pad_inches=0,facecolor='#292929')
            plt.close(fig)


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

        self.max_stock_num = 20
    def create_grid(self,frame):
        ### Will replace with ticker pulling function
        tickers = {
            'AAPL': 1.23,
            'BA': -0.40,
            'GOOGL': 4.56,
            'TSLA': -3.87,
            'BLAH': -10.00,
            'TEST': -5.00,
            'C': 1.23,
            'D': -0.40,
            'E': 4.56,
            'F': -3.87,
            'G': -10.00,
            'H': -5.00,
            'I': 1.23,
            'J': -0.40,
            'K': 4.56,
            'L': -3.87,
            'M': -10.00,
            'N': -5.00,
        }
        
        for i, (ticker,percentage) in enumerate(tickers.items()):
            # Only allow certain number of stocks
            if i == self.max_stock_num:
                break

            row = i % 4
            col = (i//4) * 2
            ticker_label = tk.Label(frame, text=ticker,fg='white',padx=10,pady=5,bg=BG_WINDOW_COLOR)
            ticker_label.grid(row=row,column=col,sticky='w',padx=5,pady=5)

            percentage_label=tk.Label(frame,text=f'{percentage:.2f}%', fg=self.get_color(percentage),bg=BG_WINDOW_COLOR)
            percentage_label.grid(row=row, column=col+1,stick='w',padx=5,pady=5)

    def get_color(self, percentage) -> str:
        if percentage >= 0:
            return 'green'
        return 'red'
