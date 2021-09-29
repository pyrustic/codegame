import tkinter as tk
from tkinter.scrolledtext import ScrolledText

import codeval
from cyberpunk_theme.widget.button import get_button_style_4, get_button_style_9
from viewable import Viewable
from codegame.game.testing import eval_user_code
from megawidget.toast import Toast


class Editor(Viewable):
    def __init__(self, master, tests, on_success):
        super().__init__()
        self._master = master
        self._tests = tests
        self._on_success = on_success
        self._scrolled_text = None

    def _build(self):
        self._body = tk.Toplevel(self._master)
        self._body.geometry("600x400")
        self._body.title("Solve Me - Editor")
        self._install_text_editor()
        self._install_footer()

    def _on_map(self):
        super()._on_map()

    def _on_destroy(self):
        pass

    def _install_text_editor(self):
        self._scrolled_text = ScrolledText(self._body, width=0, height=0,
                                           selectbackground="#93C6F9",
                                           selectforeground="#4073A6")
        self._scrolled_text.focus_set()
        self._scrolled_text.pack(expand=1, fill=tk.BOTH)
        self._scrolled_text.bind("<Tab>",
            lambda e, textwidget=self._scrolled_text: prettytab(textwidget))

    def _install_footer(self):
        frame = tk.Frame(self._body)
        frame.pack(fill=tk.X, padx=2, pady=(2, 2))
        # button clear
        button_clear = tk.Button(frame, text="Clear",
                                 command=self._on_click_clear)
        button_clear.pack(side=tk.LEFT)
        get_button_style_9().target(button_clear)
        # button submit
        button_submit = tk.Button(frame, text="Submit",
                                  command=self._on_click_submit)
        button_submit.pack(side=tk.RIGHT, padx=(0, 2))
        get_button_style_4().target(button_submit)
        # button paste
        button_paste = tk.Button(frame, text="Paste",
                                 command=self._on_click_paste)
        button_paste.pack(side=tk.RIGHT, padx=(0, 2))
        # button copy
        button_copy = tk.Button(frame, text="Copy",
                                command=self._on_click_copy)
        button_copy.pack(side=tk.RIGHT, padx=(0, 2))
        # button cancel
        button_cancel = tk.Button(frame, text="Close",
                                  command=self.destroy)
        button_cancel.pack(side=tk.RIGHT, padx=(0, 2))

    def _on_click_clear(self):
        self._scrolled_text.delete("1.0", tk.END)

    def _on_click_copy(self):
        cache = self._scrolled_text.get("1.0", "end-1c")
        self._body.clipboard_clear()
        self._body.clipboard_append(cache)

    def _on_click_submit(self):
        code = self._scrolled_text.get("1.0", "end-1c")
        for test in self._tests:
            test_name = test[0].get("name", "Test")
            try:
                eval_user_code(code, test)
            except codeval.IdentifierError:
                msg = "{} failed !\n{}".format(test_name, "Invalid Function Name Error")
                Toast(self._body, message=msg)
                return
            except codeval.CodevalFunctionError:
                msg = "{} failed !\n{}".format(test_name, "Function Error")
                Toast(self._body, message=msg)
                return
            except codeval.CodevalMaxTimeError:
                msg = "{} failed !\n{}".format(test_name, "Max Time Error")
                Toast(self._body, message=msg)
                return
            except codeval.CodevalOutputError:
                msg = "{} failed !\n{}".format(test_name, "Output Error")
                Toast(self._body, message=msg)
                return
            except codeval.CodevalCodeError:
                msg = "{} failed !\n{}".format(test_name, "Code Error")
                Toast(self._body, message=msg)
                return
        toast = Toast(self._body, message="Success !")
        toast.wait_window()
        self.destroy()
        self._on_success()

    def _on_click_paste(self):
        cache = self._body.clipboard_get()
        if cache:
            self._scrolled_text.insert(tk.END, cache)

            
def prettytab(textwidget):
    textwidget.insert(tk.INSERT, " " * 4)
    return "break"
