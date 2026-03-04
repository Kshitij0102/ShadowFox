from tkinter import *
from tkinter import ttk, scrolledtext
from spellchecker import SpellChecker

class AutocorrectKeyboard:
    def __init__(self, root):
        self.root = root
        self.root.title("ShadowFox Autocorrect Keyboard - Fixed")
        self.root.geometry("700x600")
        
        self.spell = SpellChecker(language='en')
        self.word_start = None  # Track word start position
        
        # Main text area
        self.text_area = scrolledtext.ScrolledText(root, wrap=WORD, font=("Arial", 12))
        self.text_area.pack(padx=10, pady=10, fill=BOTH, expand=True)
        self.text_area.bind('<KeyRelease>', self.check_spelling)
        self.text_area.bind('<space>', self.on_space)
        self.text_area.bind('<Return>', self.on_enter)
        
        # Status label
        self.status = Label(root, text="Ready - Type to test", relief=SUNKEN, anchor=W)
        self.status.pack(side=BOTTOM, fill=X)
        
        # Suggestions frame
        self.sug_frame = Frame(root)
        self.sug_frame.pack(padx=10, pady=5, fill=X)
        
        Label(self.sug_frame, text="Suggestions (click or space):").pack(anchor=W)
        self.sug_list = Listbox(self.sug_frame, height=4)
        self.sug_list.pack(fill=X, pady=2)
        self.sug_list.bind('<<ListboxSelect>>', self.replace_suggestion)
        
        Button(self.sug_frame, text="Accept Top", command=self.replace_top).pack(side=LEFT)
        Button(self.sug_frame, text="Ignore", command=self.ignore_word).pack(side=RIGHT)
    
    def get_current_word_info(self):
        contents = self.text_area.get("1.0", END).rstrip()
        if not contents:
            return "", None
        
        # Find last word boundaries
        pos = self.text_area.index(END)
        pos = pos[:pos.rfind(' ')] if ' ' in pos else pos
        
        line, col = map(int, pos.split('.'))
        line_text = self.text_area.get(f"1.0", f"{line}.0 lineend")
        words = line_text.split()
        if not words:
            return "", None
        
        last_word = words[-1].strip('.,!?;:"\'')
        if last_word.lower() in self.spell:
            return last_word, None
        
        # Position for replacement: end of last word
        word_end = self.text_area.index(f"end - {len(contents)-len(last_word)} chars")
        return last_word, word_end
    
    def check_spelling(self, event=None):
        self.sug_list.delete(0, END)
        word, pos = self.get_current_word_info()
        if word and len(word) > 1 and not self.spell[word.lower()]:
            self.status.config(text=f"Misspelled: '{word}'")
            suggestions = self.spell.candidates(word)
            for sug in list(suggestions)[:5]:
                self.sug_list.insert(END, sug)
        else:
            self.status.config(text="Good spelling")
    
    def on_space(self, event):
        word, pos = self.get_current_word_info()
        if self.sug_list.size() > 0:
            self.replace_top()
        self.status.config(text="Space added")
        return 'break'  # Prevent double space
    
    def on_enter(self, event):
        return 'break'  # Allow normal enter
    
    def replace_top(self):
        if self.sug_list.size() > 0:
            self.replace_suggestion_helper(self.sug_list.get(0))
    
    def replace_suggestion(self, event=None):
        selection = self.sug_list.curselection()
        if selection:
            self.replace_suggestion_helper(self.sug_list.get(selection[0]))
    
    def replace_suggestion_helper(self, new_word):
        word, start_pos = self.get_current_word_info()
        if start_pos and word:
            end_pos = self.text_area.index(f"{start_pos} + {len(word)} chars")
            self.text_area.delete(start_pos, end_pos)
            self.text_area.insert(start_pos, new_word)
        self.sug_list.delete(0, END)
        self.status.config(text=f"Replaced with '{new_word}'")
    
    def ignore_word(self):
        self.sug_list.delete(0, END)
        self.status.config(text="Ignored")

if __name__ == "__main__":
    root = Tk()
    app = AutocorrectKeyboard(root)
    root.mainloop()
