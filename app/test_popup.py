import ctypes  # An included library with Python install.
ctypes.windll.user32.MessageBoxW(0, "Click Ok to Finish", "Macrovan", 1)

# import ctypes  # An included library with Python install.
def Mbox(title, text, style):
     return ctypes.windll.user32.MessageBoxW(0, text, title, style)

Mbox('Your title', 'Your text', 1)
