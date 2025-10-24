import googletrans
import tkinter as tk
from tkinter import messagebox, ttk
import requests
import threading
import datetime

default_font = ("Segoe UI", 12)
FILENAME = ".translatorHistory.txt"
 
class LinTL:
    def __init__(self, root):
        self.root = root
        self.root.title("LinTL")
        self.root.geometry('450x550')
        self.root.resizable(False, False)
        self.isDark = True

        self.isShowHistoryPopupAvail = False

        self.menubar = tk.Menu(self.root, font=default_font)
        
        self.optionmenu = tk.Menu(self.menubar, tearoff=0)
        self.optionmenu.add_command(label="Toggle Theme", command=self.toggle_theme, font=default_font)
        self.optionmenu.add_command(label="History", command=self.showHistory, font=default_font)
        self.optionmenu.add_command(label="Clear History", command=self.clearHistory, font=default_font)
        self.menubar.add_cascade(label="Options", menu=self.optionmenu)
        self.root.configure(menu=self.menubar)

        self.resultListbox = tk.Listbox(self.root, width=50, height=6, font=default_font)
        self.resultListbox.pack(padx=5, pady=5)

        self.label0 = tk.Label(self.root, text="Input:", font=default_font)
        self.label0.pack(padx=5, pady=5)

        self.userInput = tk.Entry(self.root, width=50, font=default_font)
        self.userInput.pack(padx=5, pady=5)
        self.userInput.focus()

        self.label1 = tk.Label(self.root, text="Translate from:", font=default_font)
        self.label1.pack(padx=5, pady=5)

        self.languages = googletrans.LANGUAGES

        self.sourceLang = ttk.Combobox(self.root, values=list(self.languages.values()))
        self.sourceLang.set("English")
        self.sourceLang.pack(padx=5, pady=5)
        
        self.label2 = tk.Label(self.root, text="Translate to:", font=default_font)
        self.label2.pack(padx=5, pady=5)

        self.targetLang = ttk.Combobox(self.root, values=list(self.languages.values()))
        self.targetLang.set("")
        self.targetLang.pack(padx=5, pady=5)

        self.translate_btn = tk.Button(self.root, text="Translate", command=self.translate, width=10, height=2, font=default_font)
        self.translate_btn.pack(padx=5, pady=5)

        self.clear_btn = tk.Button(self.root, text="Clear", command=self.clear, width=10, height=2, font=default_font)
        self.clear_btn.pack(padx=5, pady=5)

        self.exit_btn = tk.Button(self.root, text="Exit", command=self.root.quit, width=10, height=2, font=default_font)
        self.exit_btn.pack(padx=5, pady=5)

        self.toggle_theme()

        self.root.bind('<Return>', lambda _: self.translate())
        self.root.bind('<Control-q>', lambda _: self.root.quit())
        self.root.bind('<Control-h>', lambda _: self.showHistory())
        self.root.bind('<Control-t>', lambda _: self.toggle_theme())

    def toggle_theme(self):
        light_theme = {
            "bg": "#F8F9FA",
            "fg": "#202124",
            "entry_bg": "#FFFFFF",
            "listbox_bg": "#FFFFFF",
            "button_bg": "#E4E6EB",
            "button_fg": "#202124",
            "highlight": "#0D6EFD",
        }

        dark_theme = {
            "bg": "#181818",
            "fg": "#EAEAEA",
            "entry_bg": "#202020",
            "listbox_bg": "#202020",
            "button_bg": "#2A2A2A",
            "button_fg": "#EAEAEA",
            "highlight": "#1E90FF",
        }  

        self.theme = dark_theme if self.isDark else light_theme

        self.root.configure(bg=self.theme['bg'])
        self.menubar.configure(bg=self.theme['bg'], fg=self.theme['fg'])
        self.optionmenu.configure(bg=self.theme['bg'], fg=self.theme['fg'])
        self.userInput.configure(bg=self.theme['entry_bg'], fg=self.theme['fg'])
        self.sourceLang.configure(background=self.theme['bg'], foreground=self.theme['highlight'])
        self.targetLang.configure(background=self.theme['bg'], foreground=self.theme['highlight'])
        self.resultListbox.configure(bg=self.theme['listbox_bg'], fg=self.theme['fg'])

        for label in [self.label0, self.label1, self.label2]:
            label.configure(bg=self.theme['bg'], fg=self.theme['fg'])

        for button in [self.translate_btn, self.clear_btn, self.exit_btn]:
            button.configure(bg=self.theme['button_bg'], fg=self.theme['button_fg'])

        if self.isShowHistoryPopupAvail:
            self.historyPopup.configure(bg=self.theme['bg'])
            self.historyListbox.configure(bg=self.theme['listbox_bg'], fg=self.theme['fg'])
            self.exitHistoryPopup_btn.configure(bg=self.theme['button_bg'], fg=self.theme['button_fg'])    

        self.isDark = not self.isDark

    def send_request(self, url, params):
        try:
            response = requests.get(url, params)
            if response.status_code == 200:
                return response.json()
            else:
                messagebox.showerror("Error", f"[Error: {url}] => {response.status_code} - {response.text}", parent=self.root)
                return None

        except requests.RequestException as e:
            messagebox.showerror("Error" ,f'Request exception at {url}: {e}', parent=self.root)
            return None

    def translate(self):
        if not self.userInput.get():
            messagebox.showerror("Error", "Enter phrase to translate.", parent=self.root)
            return

        if not self.sourceLang.get():
            messagebox.showerror("Error", "Select a source language to translate.", parent=self.root)
            return
        
        if not self.targetLang.get():
            messagebox.showerror("Error", "Select a target language to translate.", parent=self.root)
            return
        
        def run():
            urls_list = ["https://collonoid.tasport1.workers.dev/translate", "https://655.mtis.workers.dev/translate", "https://t72.mouth-ploy-evoke.workers.dev/translate", "https://emergency-tas-backup1.uncoverclimatix.workers.dev/translate"]    

            params = {
                'text': self.userInput.get(),
                'source_lang': next((k for k, v in self.languages.items() if v == self.sourceLang.get().lower()), None),
                'target_lang': next((k for k, v in self.languages.items() if v == self.targetLang.get().lower()), None),
            }

            result = None

            for url in urls_list:
                result = self.send_request(url, params)
                if result is not None:
                    break
            
            if result is not None:
                userinput = result['inputs']['text']
                output = result['response']['translated_text']
                self.resultListbox.insert(tk.END, f"Input: {userinput}")
                self.resultListbox.insert(tk.END, f"Output: {output}\n")
                self.resultListbox.see(tk.END)
                self.saveHistory(userinput, output)

        
        thread = threading.Thread(target=run)
        thread.start()

    def clear(self):
        self.resultListbox.delete(0, tk.END)
        self.userInput.delete(0, tk.END)

    def saveHistory(self, userinput, output):
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(FILENAME, 'a') as f:
            f.write(f"[!] {current_time}\nInput: {userinput}\nOutput: {output}\n\n")

    def clearHistory(self):
        with open(FILENAME, 'w') as f:
            f.write('')
            messagebox.showinfo("History", "History cleared successfully.", parent=self.root)

    def showHistory(self): 
        if self.isShowHistoryPopupAvail:
            self.historyPopup.lift()
            return
        self.isShowHistoryPopupAvail = True

        self.historyPopup = tk.Toplevel(self.root)
        self.historyPopup.title("History")
        self.historyPopup.geometry('450x450')
        self.historyPopup.resizable(False, False)


        self.historyListbox = tk.Listbox(self.historyPopup, width=50, height=15, font=default_font)
        self.historyListbox.pack(padx=5, pady=5)

        try:
            with open(FILENAME, 'r') as f:
                content = f.readlines()
                if not content:
                    self.historyListbox.insert(tk.END, "No History Found.")
                    
                for line in content:
                    self.historyListbox.insert(tk.END, line.strip())
        except FileNotFoundError:
            messagebox.showinfo("History", "No History Found.")
            self.historyPopup.destroy()
            return

        def exitHistoryPopup():
            self.isShowHistoryPopupAvail = False
            self.historyPopup.destroy()

        self.exitHistoryPopup_btn = tk.Button(self.historyPopup, text="Exit", command=exitHistoryPopup, width=10, height=2, font=default_font)
        self.exitHistoryPopup_btn.pack(padx=5, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = LinTL(root)
    root.mainloop()