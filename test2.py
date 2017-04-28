try:
    import Tkinter as tk
    import ttk
except ImportError: # Python 3
    import tkinter as tk
    import tkinter.ttk as ttk

SUNKABLE_BUTTON = 'SunkableButton.TButton'

root = tk.Tk()
root.geometry("400x300")
style = ttk.Style()

def start():
    button.state(['pressed', 'disabled'])
    style.configure(SUNKABLE_BUTTON, relief=tk.SUNKEN, foreground='green')

def stop():
    button.state(['!pressed', '!disabled'])
    style.configure(SUNKABLE_BUTTON, relief=tk.RAISED, foreground='red')

button = ttk.Button(root, text ="Start", command=start, style=SUNKABLE_BUTTON)
button.pack(fill=tk.BOTH, expand=True)
ttk.Button(root, text="Stop", command=stop).pack(fill=tk.BOTH, expand=True)
root.mainloop()
