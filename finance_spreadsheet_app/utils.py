import matplotlib.pyplot as plt
import base64
from io import BytesIO

def get_graph():
    buffer = BytesIO() # create a bytes buffer for the eventual image to be saved to 
    plt.savefig(buffer, format = 'png')
    buffer.seek(0)
    image_png = buffer.getvalue() # retrieve the contents of the image 
    graph = base64.b64encode(image_png) # encode the image into base64
    graph = graph.decode('utf-8') # decode the string from base 64 into utf8
    buffer.close() # close the buffer to free the memory 
    return graph

def get_expense_plot(x, y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title('Total Expenses per Month')
    plt.plot(x, y)
    plt.xticks(rotation=45)
    plt.xlabel('Month')
    plt.ylabel('Total Expenses ($)')
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_deposit_plot(x, y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title('Total Deposits per Month')
    plt.plot(x, y)
    plt.xticks(rotation=45)
    plt.xlabel('Month')
    plt.ylabel('Total Deposits ($)')
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_investment_plot(x, y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title('Total Investments per Month')
    plt.plot(x, y)
    plt.xticks(rotation=45)
    plt.xlabel('Month')
    plt.ylabel('Total Investments ($)')
    plt.tight_layout()
    graph = get_graph()
    return graph