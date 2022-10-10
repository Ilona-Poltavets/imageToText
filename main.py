from tkinter import Tk, Menu, Text, BOTH, filedialog, END, simpledialog, Button, ACTIVE, LEFT, Label
from tkinter.ttk import Frame
from tkinter import messagebox as mb
import os
import Converter
from PIL import ImageGrab, Image

lang="eng"

def get_path_img_file():
    im = ImageGrab.grabclipboard()
    if isinstance(im, Image.Image):
        im.save("temp.png")
        return os.path.abspath("temp.png")

class MainWin(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.master.title("Image to Text")
        self.pack()

        menubar = Menu(self.master)
        self.master.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Image to Text", command=self.imageToText)
        fileMenu.add_command(label="Find the word in the picture", command=self.findText)
        menubar.add_cascade(label="File", menu=fileMenu)

        self.txt = Text(self)
        self.txt.pack(fill=BOTH, expand=1)

    def imageToText(self):
        fl = self.openFile()
        SelectLanguageDialog(self)
        global lang
        if fl != '':
            path = os.path.abspath(fl)
            try:
                text = Converter.convetImageToTxt(path,lang)
                self.txt.delete("1.0", "end")
                self.txt.insert(END, text)
            except:
                mb.showerror("ERROR", "File type not supported")

    def findText(self):
        fl = self.openFile()
        SelectLanguageDialog(self)
        txt = simpledialog.askstring("Enter text", "Enter text")
        if fl != '':
            global lang
            path = os.path.abspath(fl)
            try:
                Converter.findWordOnImage(path, txt, lang)
            except:
                mb.showerror("ERROR", "File type not supported")

    def openFile(self):
        answer = mb.askyesno(title="Notification", message="Take picture from clipboard?")
        if answer:
            return get_path_img_file()
        ftypes = [("JPG", "*.jpg"), ("PNG", "*.png"), ("All Files", "*")]
        dlg = filedialog.Open(self, filetypes=ftypes)
        fl = dlg.show()
        return fl


class SelectLanguageDialog(simpledialog.Dialog):
    def ukr(self):
        global lang
        lang="ukr"
        self.destroy()

    def rus(self):
        global lang
        lang="rus"
        self.destroy()

    def eng(self):
        global lang
        lang="eng"
        self.destroy()

    def buttonbox(self):
        box = Frame(self)
        Label(text="Select text language")
        tmp = Button(box, text="Ukr", width=10, command=self.ukr)
        tmp.pack(side=LEFT, padx=5, pady=5)
        tmp = Button(box, text="Rus", width=10, command=self.rus)
        tmp.pack(side=LEFT, padx=5, pady=5)
        tmp = Button(box, text="Eng", width=10, command=self.eng, default=ACTIVE)
        tmp.pack(side=LEFT, padx=5, pady=5)
        box.pack()


def main():
    root = Tk()
    fr = MainWin()
    root.mainloop()


if __name__ == '__main__':
    main()
