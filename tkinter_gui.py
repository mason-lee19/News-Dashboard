import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk

import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config
from utils.get_stock_data import GetStockData
from utils.tools import Utils

BORDER_COLOR = 'White'
BORDER_THICKNESS = 2
BG_COLOR = 'gray15'
BG_WINDOW_COLOR = 'gray17'

DEFAULT_TIME_FRAME = '1D'


class GUI:
    def __init__(self,root):
        self.root = root

        self.stock_api = GetStockData()

        self.setup_gui()
    def setup_gui(self):

        self.root.title('News Dash')
        self.root.configure()

        # Get the dimensions of the root window
        self.root.update_idletasks()
        self.width = self.root.winfo_width()
        self.height = self.root.winfo_height()
        
        # Define some margins
        margin = 20
        inner_margin = 10

        # Define the widths and heights of the sections
        left_right_width = self.width // 6
        center_width = self.width - 2 * left_right_width - 5 * margin
        input_rect_width = left_right_width // 4
        large_rect_height = (self.height - 6 * margin) * 3 // 4 - inner_margin
        small_rect_height = (self.height - 2 * margin) // 4 - inner_margin
        input_rect_height = margin
        

        # Define the heights for left and right rectangles
        left_right_large_height = (self.height - 2 * margin - inner_margin) * 2 // 3
        left_right_small_height = (self.height - 2 * margin - inner_margin) // 3

        ### Headline scroll window
        headline_window = ScrollWindow(self.root, label_text='Headlines', width=left_right_width-inner_margin, height=left_right_large_height-(inner_margin*6), 
                                               border_width=BORDER_THICKNESS, border_color=BORDER_COLOR)
        headline_window.place(x=margin, y=margin)
        headline_window.fill_with_headlines(headline_window)

        ### Portfolio based on headline ticker activity
        headline_portfolio = tk.Frame(self.root, width=left_right_width, height=left_right_small_height, 
                                      highlightthickness=BORDER_THICKNESS, highlightbackground=BORDER_COLOR)
        headline_portfolio.place(x=margin, y=margin + left_right_large_height + inner_margin)

        ### Keyword monitor window
        keyword_window = KeywordWindow(self.root, width=left_right_width+inner_margin, height=left_right_large_height,
                                       border_width=BORDER_THICKNESS, border_color=BORDER_COLOR)
        keyword_window.place(x=self.width - left_right_width - margin - inner_margin, y=margin)
        keyword_grid = KeywordWindow(self.root, width=left_right_width-inner_margin-10, height=left_right_large_height-(inner_margin*2)-10)
        keyword_grid.place(x=self.width - left_right_width - margin, y=margin + 10)

        keyword_grid.fill_with_keywords(keyword_grid)

        ### Call Volume or top keyword window
        top_keywords = tk.Frame(self.root, width=left_right_width, height=left_right_small_height,
                                highlightthickness=BORDER_THICKNESS, highlightbackground=BORDER_COLOR)
        top_keywords.place(x=self.width - left_right_width - margin, y=margin + left_right_large_height + inner_margin)

        ### Ticker input
        ticker_entry = ctk.CTkEntry(self.root,width=input_rect_width,height=input_rect_height)
        ticker_entry.place(x=left_right_width+margin*2+inner_margin,y=margin + inner_margin - .5 * margin)

        ### Ticker plot button
        def plot_ticker(period:str='1D'):
            print(f'plot for ticker {ticker_entry.get()}')
            self.plot_stock(self.stock_api.apiConfig,ticker_entry.get(),period,stock_history)

        plot_button = ctk.CTkButton(self.root,text='Plot',command=plot_ticker,width=input_rect_width,height=input_rect_height,fg_color=BG_WINDOW_COLOR)
        plot_button.place(x=left_right_width+margin*2+2*inner_margin+input_rect_width,y=margin+inner_margin-.5*margin)

        ### Ticker history viewer
        stock_history = tk.Frame(self.root, width=center_width, height=large_rect_height - 1 * margin,
                                 highlightthickness=BORDER_THICKNESS, highlightbackground=BORDER_COLOR)
        stock_history.place(x=left_right_width + margin*2 + inner_margin, y=margin + inner_margin + 1 * margin)

        ### Personal portfolio window
        # Initialize the canvas to place the interactive stock history
        self.init_canvas()

        personal_ticker_window = TickerGrid(self.root,width=center_width, height=small_rect_height,
                                            border_width=BORDER_THICKNESS, border_color=BORDER_COLOR)
        ticker_grid_frame = TickerGrid(self.root,width=center_width-10, height=small_rect_height-10)
        ticker_grid_frame.place(x=left_right_width + margin*2+35 + inner_margin, y=margin + large_rect_height + 2 * inner_margin+10)
        personal_ticker_window.place(x=left_right_width + margin*2 + inner_margin, y=margin + large_rect_height + 2 * inner_margin)
        personal_ticker_window.create_grid(ticker_grid_frame)

        ### Bottom toolbar
        def on_toolbar_button_press(period):
            personal_ticker_window.update_tickers(self.stock_api,period)
            personal_ticker_window.create_grid(ticker_grid_frame)
            plot_ticker(period)

        toolbar = Toolbar(self.root,callback=on_toolbar_button_press)

    def init_canvas(self):
        self.canvas = None

    def plot_stock(self,stock_api,ticker:str,period:int,frame):
        data = {
            'Date': pd.date_range(start='1/1/2020', periods=100),
            'Open': pd.Series(range(100)) + 100,
            'High': pd.Series(range(100)) + 105,
            'Low': pd.Series(range(100)) + 95,
            'Close': pd.Series(range(100)) + 100,
            'Volume': pd.Series(range(100)) * 1000
        }
        # Pull data -> get_stock_data.py will check if we have it in db
        # daily will have to constantly be updated every time 1D gets pressed

        # If there is already a plot we want to destroy and draw another
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        df = pd.DataFrame(data)
        df.set_index('Date',inplace=True)

        fig,ax = plt.subplots(figsize=(6.9,4.7),facecolor='#393939')
        plt.title(f'{period} - {ticker}')
        ax = self.color_axis(ax)

        mpf.plot(df,type='candle',ax=ax,mav=(3,6,9))

        self.canvas = FigureCanvasTkAgg(fig,master=frame)
        self.canvas.get_tk_widget().pack_forget()
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=ctk.BOTH,expand=True)

    def color_axis(self,ax):
        ax.set_facecolor('#393939')
        ax.spines['bottom'].set_color('#dddddd')
        ax.spines['top'].set_color('#dddddd')
        ax.spines['right'].set_color('#dddddd')
        ax.spines['left'].set_color('#dddddd')

        ax.tick_params(axis='x', colors='#dddddd')
        ax.tick_params(axis='y', colors='#dddddd')

        ax.yaxis.label.set_color('#dddddd')
        ax.xaxis.label.set_color('#dddddd')

        ax.title.set_color('#dddddd')

        return ax



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

        self.image_refs = []

    def fill_with_keywords(self,frame):
        ### Will replace with db pull of headline data
        # Create seperate graph check, and do proper os cleanup of that image and create another
        # Segmentation fault due to self.create_chart writing over already created same name pngs
        keywords = {
            'nvidia':[1,2,4,6,3,2,1],
            'mason':[5,2,3,5,6,8],
            'russia':[9,7,4,1,2,3],
            'yemen':[4,6,1,3,7,8],
            'flu':[7,5,2,4,5,1],
        }


        for i, (word,data) in enumerate(keywords.items()):
            keyword_label = tk.Label(frame,text=word,justify='left',bg=BG_WINDOW_COLOR)
            keyword_label.grid(row=i,column=0,stick='w',padx=5,pady=5)
            
            graph_image = f'attachments/graph_{i}.png'

            #self.create_chart(data,graph_image)
            img = Image.open(graph_image)
            img = ImageTk.PhotoImage(img)

            self.image_refs.append(img)
            
            graph_label = tk.Label(frame,image=img,bg=BG_WINDOW_COLOR)
            graph_label.image = img
            graph_label.grid(row=i,column=1,stick='w',padx=10,pady=5)
            
            value_label = tk.Label(frame,text=str(keywords[word][-1]),justify='left',bg=BG_WINDOW_COLOR)
            value_label.grid(row=i,column=3,stick='w',padx=5,pady=5)

            

    def create_chart(self,data,filename):
            color = 'green' if data[0] <= data[-1] else 'red'
            fig,ax = plt.subplots(figsize=(1,0.4))
            ax.bar(range(len(data)),data,color=color)
            ax.set_axis_off()
            plt.savefig(filename,bbox_inches='tight',pad_inches=0,facecolor='#292929')
            plt.close(fig)


class HighlightButton(ctk.CTkButton):
    def __init__(self,master=None,command=None,**kwargs):
        super().__init__(master,**kwargs)
        self.master = master
        self.callback = command
        self.default_bg = BG_COLOR
        self.highlight_bg = 'gray25'

        self.configure(fg_color=self.default_bg)

        self.bind("<Button-1>", self.on_press)

    def on_press(self,event):
        ### Update to change time frame on press depending on button
        for button in self.master.winfo_children():
                button.configure(fg_color=self.default_bg)
        self.configure(fg_color=self.highlight_bg)
        if self.callback:
            self.callback(self)

class Toolbar(ctk.CTkFrame):
    def __init__(self,master=None,callback=None,**kwargs):
        super().__init__(master,**kwargs)
        self.master = master
        self.pack(side=tk.BOTTOM)

        self.callback = callback

        self.buttons = []
        self.selected_button = None

        self.add_button("1D")
        self.add_button("1W")
        self.add_button("1M")
        self.add_button("3M")
        self.add_button("6M")
        self.add_button("1Y")
        self.add_button("5Y")

    def add_button(self,text):
        button = HighlightButton(self,text=text,fg_color='transparent',width=12,command=self.on_button_press)
        button.pack(side=tk.LEFT,padx=10,pady=15)
        self.buttons.append(button)

    def on_button_press(self,button):
        # Force a refresh of portfolio ticker grid, keyword graphs, main ticker graph
        print(f'Refreshing for timeframe {button.cget('text')}')
        if self.callback:
            self.callback(button.cget('text'))
    
    def get_selected_button_text(self):
        return self.selected_button.cget('text') if self.selected_button else None

class TickerGrid(ctk.CTkFrame):
    def __init__(self,master=None,**kwargs):
        super().__init__(master,**kwargs)

        self.max_stock_num = 20

        self.tickers = config.TICKERS
        #self.update_tickers()
        self.ticker_dict = {key:0 for key in self.tickers}

    def update_tickers(self,api,period:str='1D'):
        # check if we have the ticker data
        # maybe add database saving later

        # If not we can pull and add to DB
        for ticker in self.ticker_dict.keys():
            data = api.get_data(ticker,period)
            self.ticker_dict[ticker] = float(api.calc_returns(data))
            
        print(self.ticker_dict)


    def create_grid(self,frame):
        
        for i, (ticker,percentage) in enumerate(self.ticker_dict.items()):
            # Only allow certain number of stocks
            if i == self.max_stock_num:
                break

            row = i % 4
            col = (i//4) * 2
            ticker_label = tk.Label(frame, text=ticker,fg='white',padx=10,pady=5,bg=BG_WINDOW_COLOR)
            ticker_label.grid(row=row,column=col,sticky='w',padx=5,pady=5)

            percentage_label=tk.Label(frame,text=f'{percentage:.2f}%', fg=Utils.get_color(percentage),bg=BG_WINDOW_COLOR)
            percentage_label.grid(row=row, column=col+1,stick='w',padx=5,pady=5)
