import tkinter as tk

from tkinter import  scrolledtext, messagebox
from tkinter.filedialog import askdirectory
import os,datetime

class TkinterUi(object):
    def __init__(self):
        self.win = tk.Tk()
        self.win.title('清理数据库脚本文档')
        self.win.geometry('800x450+300+20')

        self.l1 = tk.Label(self.win, text='请选择目录：', font=('Arial', 11))
        self.l1.place(x=10, y=20)

        self.EntryPath = tk.StringVar()
        self.entry = tk.Entry(self.win, font=('Arial', 11),textvariable = self.EntryPath)
        self.entry.place(x=110,y=20)

        self.entry.bind(sequence="<Button-1>", func=self.SelectPath)

        self.button = tk.Button(self.win,text='开始清理',font=('Arial',11),command=self.ClearDBTxt,bg='lightblue')
        self.button.place(x=300,y=16)

        self.m1 = tk.LabelFrame(self.win, text="Result:")  # 创建一个容器，其父容器为win
        self.m1.grid(column=0, row=0, padx=10, pady=10)
        self.scr1 = tk.scrolledtext.ScrolledText(self.m1, width=109, height=28, wrap=tk.WORD,foreground='brown',
                                              state='disabled')
        self.scr1.grid(column=0, columnspan=3)
        self.m1.place(x=10, y=45)

        self.FileDirs = []
        self.LocalTime = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')


        self.win.mainloop()
    def SelectPath(self,key):
        path_ = askdirectory()
        self.EntryPath.set(path_)

    def ClearDBTxt(self):
        FileDir = self.entry.get()

        if self.scr1.get('1.0', 'end-1c'):
            self.scr1.configure(state='normal')
            self.scr1.delete(1.0, tk.END)
            self.scr1.configure(state='disabled')
        if FileDir:
            FileDir = FileDir.replace('/','\\')
            LogFile = self.FindFile(FileDir.strip())

            self.scr1.configure(state='normal')
            self.scr1.insert(tk.END, LogFile)
            self.scr1.see(tk.END)
            self.scr1.configure(state='disabled')

        else:
            messagebox.showinfo('消息框', '请选择目录')

    # 查找文件
    def FindFile(self,filelocal):
        for root, dirs, flnames in os.walk(filelocal):
            self.flag = True
            if flnames != []:
                if len(flnames) == 1 and flnames[0][-4:] == '.txt':
                    self.FileDirs.append((flnames[0], root + "\\" + flnames[0]))
                elif len(flnames) > 1:
                    for flname in flnames:
                        if flname[-4:] == '.txt':
                            self.FileDirs.append((flname, root + "\\" + flname))
        return self.ClearFile(self.FileDirs)

    # 清理文件
    def ClearFile(self, FileDirs):
        LogStr = []
        for file in FileDirs:
            try:
                file_dir = file[1]
                if os.popen("type %s" % file[1]).read():
                    with open(file[1], 'w', encoding='gb18030', errors='ignore') as  f:
                        f.write('')
                    LogStr.append(file[1])
            except Exception as e:
                with open(file_dir, 'w', encoding='gb18030', errors='ignore') as  f:
                    f.write('')
                    LogStr.append(file[1])
        return self.CollectionLog(LogStr)
    # 记录日志
    def CollectionLog(self, log):

        LogStr = self.LocalTime.center(30, '-') + '文档清理日志\n\n'
        if log:
            for i in log:
                LogStr += i + '  已清空\n'
        else:
            flag = False
            LogStr += '本次清理未发现有数据的文档文件'.center(30, '+')
        WriteFlag = 'a' if os.path.isfile('ClearDBLog.txt') else 'w'
        with open('ClearDBLog.txt', WriteFlag, encoding='gb18030', errors='ignore') as f:
            f.write(LogStr + "\n")
        print(LogStr)
        return LogStr



if __name__ == '__main__':
    StartClearDBFfile = TkinterUi()

