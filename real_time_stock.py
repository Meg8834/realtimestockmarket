import tkinter as tk
from tkinter import messagebox
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

# Function to fetch stock data
def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

# Function to display stock trend (price chart)
def display_stock_trend(stock_data, ticker):
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Plot the stock closing price
    ax.plot(stock_data.index, stock_data['Close'], label=f'{ticker} Close Price', color='blue')
    
    # Calculate and plot the 50-day moving average (SMA)
    stock_data['SMA50'] = stock_data['Close'].rolling(window=50).mean()
    ax.plot(stock_data.index, stock_data['SMA50'], label='50-Day SMA', color='orange')
    
    ax.set_title(f'{ticker} Stock Price and 50-Day Moving Average')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.legend()

    # Display the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=frame)  
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

# Function to get stock data and show the chart
def fetch_data():
    ticker = ticker_entry.get().strip()
    if not ticker:
        messagebox.showerror("Input Error", "Please enter a stock ticker symbol.")
        return
    
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid dates in YYYY-MM-DD format.")
        return

    # Fetch stock data and display chart
    stock_data = get_stock_data(ticker, start_date, end_date)
    
    if stock_data.empty:
        messagebox.showerror("Data Error", "Could not fetch data for the given stock symbol.")
        return
    
    display_stock_trend(stock_data, ticker)

# GUI setup
root = tk.Tk()
root.title("Stock Price Tracker with Analysis")
root.geometry("800x600")

# Create widgets
tk.Label(root, text="Enter Stock Ticker:", font=("Arial", 14)).pack(pady=10)

ticker_entry = tk.Entry(root, font=("Arial", 14))
ticker_entry.pack(pady=10)

tk.Label(root, text="Start Date (YYYY-MM-DD):", font=("Arial", 14)).pack(pady=5)
start_date_entry = tk.Entry(root, font=("Arial", 14))
start_date_entry.insert(0, "2023-01-01")  # Default start date
start_date_entry.pack(pady=5)

tk.Label(root, text="End Date (YYYY-MM-DD):", font=("Arial", 14)).pack(pady=5)
end_date_entry = tk.Entry(root, font=("Arial", 14))
end_date_entry.insert(0, "2023-12-31")  # Default end date
end_date_entry.pack(pady=5)

tk.Button(root, text="Fetch Stock Data", command=fetch_data, font=("Arial", 14)).pack(pady=20)

# Frame for stock chart
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()
