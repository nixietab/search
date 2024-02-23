import tkinter as tk
from tkinter import scrolledtext

def read_database(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def parse_database(data):
    pages = []
    entries = data.split('\n\n')

    for entry in entries:
        page = dict(line.split(': ', 1) for line in entry.split('\n') if ': ' in line)
        pages.append(page)

    return pages

def search_by_term(pages, search_term):
    search_terms = search_term.lower().split()
    return [page for page in pages if all(any(term in value.lower() for value in page.values()) for term in search_terms)]

def sort_results(results, sort_option):
    if sort_option == 'Name':
        return sorted(results, key=lambda x: x.get('Name', ''))
    elif sort_option == 'IP':
        return sorted(results, key=lambda x: x.get('IP', ''))
    else:
        return results

class SearchApp:
    def __init__(self, master):
        self.master = master
        master.title("Search Engine")

        self.dark_mode = True
        self.sort_options = ['None', 'Name', 'IP']
        self.sort_option_var = tk.StringVar(master)
        self.sort_option_var.set(self.sort_options[0])  # Default: None

        self.create_widgets()
        self.configure_layout()
        self.set_theme()
        self.bind_events()

    def create_widgets(self):
        tk.Label(self.master, text="Enter search term:").grid(row=0, column=0, pady=10, padx=10, sticky='e')

        self.search_entry = tk.Entry(self.master)
        self.search_entry.grid(row=0, column=1, pady=10, padx=10, sticky='ew')
        self.search_entry.bind("<Return>", lambda event: self.perform_search())

        tk.Button(self.master, text="Search", command=self.perform_search).grid(row=0, column=2, pady=10, padx=10, sticky='w')

        tk.Label(self.master, text="Sort by:").grid(row=0, column=3, pady=10, padx=10, sticky='e')

        tk.OptionMenu(self.master, self.sort_option_var, *self.sort_options).grid(row=0, column=4, pady=10, padx=10, sticky='w')

        self.result_text = scrolledtext.ScrolledText(self.master, width=60, height=15, wrap=tk.WORD)
        self.result_text.grid(row=1, column=0, columnspan=5, pady=10, padx=10, sticky='nsew')

    def configure_layout(self):
        for i in range(5):
            self.master.columnconfigure(i, weight=1 if i == 1 else 0)
        self.master.rowconfigure(0, weight=0)
        self.master.rowconfigure(1, weight=1)

    def set_theme(self):
        theme_colors = {
            'dark': {"bg": "#1e1e1e", "fg": "white", "entry_bg": "#333333", "button_bg": "#444444"},
            'light': {"bg": "white", "fg": "black", "entry_bg": "#eeeeee", "button_bg": "#dddddd"}
        }

        theme = theme_colors['dark'] if self.dark_mode else theme_colors['light']
        self.master.configure(bg=theme["bg"])
        for widget in [self.search_entry, self.result_text]:
            widget.configure(bg=theme["entry_bg"], fg=theme["fg"], insertbackground=theme["fg"])
        self.search_entry.configure(selectbackground="#4e5d94", selectforeground="white")
        tk.Button(self.master, text="Search", command=self.perform_search, bg=theme["button_bg"], fg=theme["fg"]).grid(row=0, column=2, pady=10, padx=10, sticky='w')

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.set_theme()

    def bind_events(self):
        self.sort_option_var.trace_add('write', lambda *args: self.perform_search())

    def perform_search(self):
        search_term = self.search_entry.get().strip()
        if not search_term:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Enter search term.\n")
            return

        results = search_by_term(pages, search_term)
        sorted_results = sort_results(results, self.sort_option_var.get())
        self.display_results(sorted_results)

    def display_results(self, results):
        self.result_text.delete(1.0, tk.END)
        if results:
            for page in results:
                for key, value in page.items():
                    self.result_text.insert(tk.END, f"{key}: {value}\n")

                url = page.get('URL', '')
                self.result_text.tag_configure("url", foreground="#61dafb", underline=True)
                self.result_text.tag_bind("url", "<Button-1>", lambda event, url=url: self.on_url_click(url))
                self.result_text.insert(tk.END, f"URL: {url}\n", "url")

                self.result_text.insert(tk.END, "\n")
        else:
            self.result_text.insert(tk.END, "No results were found.\n")

    def on_url_click(self, url):
        import webbrowser
        webbrowser.open_new(url)

if __name__ == "__main__":
    file_path = "webpages.txt"
    data = read_database(file_path)
    pages = parse_database(data)

    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()
