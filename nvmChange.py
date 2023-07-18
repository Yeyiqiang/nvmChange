
import os
import subprocess
from tkinter import *
import tkinter as tk
import time

# 创建窗口对象
window = tk.Tk()
window.title('基于nvm快速切换node版本')
window.geometry('500x500')

# 命令
nvm_list = 'nvm list'
nvm_arch = 'nvm arch'

class app:
    v = tk.StringVar()
    s = tk.IntVar()
    
    def __init__(self,win):
        self.win = win
        self.frame = tk.Frame(win)
        self.frame.pack(fill ='both')
        self.msg_label = tk.Label(win,font=('宋体', '12'),fg='green', padx=15, pady=15)
        self.msg_label.pack(side ='bottom')
    
    def refresh(self):
        self.frame.destroy()
        self.frame = tk.Frame(self.win)
        self.frame.pack(fill ='both')
        time.sleep(1)
        self.create()

    # 执行cmd获取列表
    def adb_shell_readlines(self,cmd):
        result = os.popen(cmd).readlines()
        return result
    
    # 提交事件处理
    def callback(self):
        version = self.v.get()
        system = self.s.get()
        if version.find('*')>-1:
            self.msg_label.config(text = '已在当前版本，无需切换！')
        else:
            result = '正在切换%s %s ...' %(version,system)
            self.msg_label.config(text = result)
            code = 'nvm use %s %s' %(version,system)
            self.await_shell(code)

    def await_shell(self,code):
        res = subprocess.Popen(code, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        result = res.stdout.read().decode('utf-8')
        res.wait()
        res.stdout.close()
        self.msg_label.config(text = result)
        self.refresh()
    
    def create(self):
        # 执行nvm列表命令
        tk.Label(self.frame, text='---NVM 版本---',font=('宋体','10', 'bold'), padx=15, pady=15).pack(anchor ='w')

        li = self.adb_shell_readlines(nvm_list)

        for val in li:
            val = val.replace('\n','').replace('\r','')
            if val != '':
                if val.find('*')>-1:
                    self.v.set(val)
                radio_button = Radiobutton(self.frame, text=val, variable=self.v, value=val).pack(anchor ='w')

        tk.Label(self.frame, text='---系统 版本---',font=('宋体','10', 'bold'), padx=15, pady=15).pack(anchor ='w')

        # 展示系统类型
        arch = self.adb_shell_readlines(nvm_arch)

        for val in arch:
            if val.find('32-bit')>-1:
                self.s.set(32)
            else:
                self.s.set(64)

        tk.Radiobutton(self.frame, text='64位系统', variable=self.s, value=64).pack(anchor ='w')
        tk.Radiobutton(self.frame, text='32位系统', variable=self.s, value=32).pack(anchor ='w')

        # 展示确定
        tk.Button(self.frame, text="快速切换", command=self.callback).pack()

if __name__ == '__main__':
    app_win = app(window)
    app_win.create()

window.mainloop()
