#coding = utf-8
import tkinter as tk
from PIL import Image, ImageTk
import platform
import time
from main import total_supply, get_comunity, get_article_title, get_article_owner, create_comunity, key_to_address, \
    create_article, get_article, get_reply_message, create_reply_message, get_article_cost, get_article_license, pay_article, \
    create_article_cost


# window.update()
# win_size = min( window.winfo_width(), window.winfo_height())
# print(win_size)

class APP:

    def __init__(self):
        self.window = tk.Tk()
        self.private_key = tk.StringVar()
        self.comunity_temp = ""
        self.article_title_temp = ""
        self.article_title_num_temp = -1
        self.comunity_listbox_empty = 0
        self.article_title_listbox_empty = 0
        self.window.title('ptt_blockchain')
        self.now_page = "login"


        self.align_mode = 'nsew'
        self.pad = 10

        self.div_size = 20
        self.div1 = tk.Frame(self.window, width=self.div_size, height=self.div_size)
        self.div2 = tk.Frame(self.window, width=self.div_size, height=self.div_size)
        self.div3 = tk.Frame(self.window, width=self.div_size, height=self.div_size)
        self.div4 = tk.Frame(self.window, width=self.div_size, height=self.div_size)
        self.div5 = tk.Frame(self.window, width=self.div_size, height=self.div_size)
        self.div6 = tk.Frame(self.window, width=self.div_size, height=self.div_size)

        self.div1.grid(column=0, row=0, padx=self.pad, pady=self.pad, sticky=self.align_mode)
        self.div2.grid(column=0, row=1, padx=self.pad, pady=self.pad, sticky=self.align_mode)
        self.div3.grid(column=0, row=2, padx=self.pad, pady=self.pad, sticky=self.align_mode)
        self.div4.grid(column=0, row=3, padx=self.pad, pady=self.pad, sticky=self.align_mode)
        self.div5.grid(column=0, row=4, padx=self.pad, pady=self.pad, sticky=self.align_mode)
        self.div6.grid(column=0, row=5, padx=self.pad, pady=self.pad, sticky=self.align_mode)

        self.login_label = tk.Label(self.div2, width=50, text="請輸入private key").grid(column=0, row=0)
        self.login_text = tk.Entry(self.div2, width=50, textvariable=self.private_key).grid(column=0, row=1)
        self.login_buttom = tk.Button(self.div2, text='登入', command=self.main).grid(column=0, row=2)

        self.isFullScreen = False
        self.window.bind('<F12>', self.toggle_fullScreen)
        self.window.bind('<Escape>', self.del_window)

        self.window.bind('<ButtonRelease>', lambda event: self.get_size)

        self.define_layout(self.window, cols=1, rows=2)

        # 切換全螢幕
        # self.isFullScreen = False
        # self.window.bind('<F12>', self.toggle_fullScreen)
        # self.window.bind('<Escape>', self.del_window)
        #
        # self.window.bind('<ButtonRelease>', lambda event: self.get_size)
        #
        # self.update()
        self.window.mainloop()

    def add_comunity(self):
        create_comunity(self.private_key.get(), self.comunity_name.get())
        self.clear3()
        self.show_comunity()

    def add_article(self):
        create_article(self.private_key.get(), self.comunity_temp, self.article_title_input.get(), self.article_content_input.get())
        self.clear2()
        self.clear3()
        self.clear4()
        self.comunity_listbox_empty = 0
        self.show_article_title()

    def add_reply_message(self):
        create_reply_message(self.private_key.get(), self.comunity_temp, self.article_title_temp, self.reply_message_input.get())
        self.clear2()
        self.clear3()
        self.clear4()
        self.article_title_listbox_empty = 0
        self.show_article()

    def to_pay_article(self):
        self.article_title_num_temp = self.article_title_listbox.curselection()[0]
        self.article_title_temp = self.article_title[self.article_title_num_temp]
        pay_article(self.private_key.get(), self.comunity_temp, self.article_title_temp)
        self.clear2()
        self.clear3()
        self.clear4()
        self.comunity_listbox_empty = 0
        self.show_article_title()

    def add_article_cost(self):
        self.article_title_num_temp = self.article_title_listbox.curselection()[0]
        self.article_title_temp = self.article_title[self.article_title_num_temp]
        create_article_cost(self.private_key.get(), self.comunity_temp, self.article_title_temp, self.article_cost_input.get())
        self.clear2()
        self.clear3()
        self.clear4()
        self.comunity_listbox_empty = 0
        self.show_article_title()

    def show_comunity(self):
        self.now_page = "comunity"
        comunity = get_comunity()[1:]
        self.clear2()
        self.clear3()
        self.comunity_scrollbar = tk.Scrollbar(self.div2)
        self.comunity_scrollbar.grid(row=1, column=1)
        self.comunity_listbox = tk.Listbox(self.div2, width=50, yscrollcommand=self.comunity_scrollbar.set, selectmode=tk.SINGLE)
        for i in range(len(comunity)):
            self.comunity_listbox.insert("end", comunity[i])
        self.comunity_listbox.grid(row=1, column=0)
        self.comunity_scrollbar.config(command=self.comunity_listbox.yview)
        self.comunity_listbox_empty = 1
        self.comunity_buttom = tk.Button(self.div2, text='Enter', command=self.show_article_title)
        self.comunity_buttom.grid(row=2, column=0, sticky=self.align_mode)

        self.comunity_name = tk.StringVar()
        self.comunity_label = tk.Label(self.div3, width=50, text="請輸入comunity name").grid(column=0, row=0)
        self.comunity_text = tk.Entry(self.div3, width=40, textvariable=self.comunity_name).grid(column=0, row=1)
        self.comunity_buttom = tk.Button(self.div3, text='create comunity', command=self.add_comunity).grid(column=0, row=2)

    def show_article_title(self):
        self.now_page = "article_title"
        if self.comunity_listbox_empty == 1:
            self.comunity_temp = self.comunity_listbox.get(self.comunity_listbox.curselection())
        self.article_title = get_article_title(self.comunity_temp)
        article_title_sum = []
        for i in range(len(self.article_title)):
            article_owner = get_article_owner(self.comunity_temp, self.article_title[i])
            article_cost = get_article_cost(self.comunity_temp, self.article_title[i])
            article_license = get_article_license(self.comunity_temp, self.article_title[i], key_to_address(self.private_key.get()))
            if article_license==True:
                article_title_sum.append(self.article_title[i] + "    作者" + article_owner[:5] + "..." + article_owner[37:] + "    價格" + str(article_cost) + "已購買")
            else:article_title_sum.append(self.article_title[i] + "    作者" +article_owner[:5] + "..." + article_owner[37:] + "    價格" + str(article_cost))
        self.clear2()
        self.clear3()

        self.article_title_scrollbar = tk.Scrollbar(self.div2)
        self.article_title_scrollbar.grid(row=1, column=1)
        self.article_title_scrollbar2 = tk.Scrollbar(self.div2,orient='horizontal')
        self.article_title_scrollbar2.grid(row=2, column=0)
        self.article_title_listbox = tk.Listbox(self.div2, width=50, yscrollcommand=self.article_title_scrollbar.set, selectmode=tk.SINGLE)
        for i in range(len(article_title_sum)):
            self.article_title_listbox.insert("end", article_title_sum[i])
        self.article_title_listbox.grid(row=1, column=0)
        self.article_title_scrollbar.config(command=self.article_title_listbox.yview)
        self.article_title_scrollbar2.config(command=self.article_title_listbox.xview)
        self.article_title_listbox_empty = 1
        self.article_title_buttom = tk.Button(self.div2, text='Enter', command=self.show_article)
        self.article_title_buttom.grid(row=3, column=0, sticky=self.align_mode)
        self.article_title_buttom = tk.Button(self.div2, text='付款', command=self.to_pay_article)
        self.article_title_buttom.grid(row=4, column=0, sticky=self.align_mode)

        self.article_title_input = tk.StringVar()
        self.article_title_label = tk.Label(self.div3, width=50, text="請輸入article title").grid(column=0, row=0)
        self.article_title_text = tk.Entry(self.div3, width=40, textvariable=self.article_title_input).grid(column=0, row=1)

        self.article_content_input  = tk.StringVar()
        self.article_label = tk.Label(self.div3, width=50, text="請輸入article content ").grid(column=0, row=2)
        self.article_text = tk.Entry(self.div3, width=40, textvariable=self.article_content_input).grid(column=0, row=3)
        self.article_buttom = tk.Button(self.div3, text='create article', command=self.add_article).grid(column=0, row=4)

        self.article_cost_input = tk.IntVar()
        self.article_label = tk.Label(self.div4, width=50, text="請輸入價格").grid(column=0, row=5)
        self.article_text = tk.Entry(self.div4, width=40, textvariable=self.article_cost_input).grid(column=0, row=6)
        self.article_buttom = tk.Button(self.div4, text='create cost', command=self.add_article_cost).grid(column=0, row=7)

    def show_article(self):
        self.clear3()
        self.clear4()
        self.now_page = "article"
        if self.article_title_listbox_empty == 1:
            self.article_title_num_temp = self.article_title_listbox.curselection()[0]
        self.article_title_temp = self.article_title[self.article_title_num_temp]
        article = get_article(self.comunity_temp, self.article_title_temp, key_to_address(self.private_key.get()))
        self.clear2()
        self.clear3()
        self.article_title_label = tk.Label(self.div2, width=50, text=self.article_title_temp).grid(column=0, row=0)
        self.article_title_owner_label = tk.Label(self.div2, width=50, text=get_article_owner(self.comunity_temp, self.article_title_temp)).grid(column=0, row=1)

        # self.article_title_content_label = tk.Label(self.div2, width=50, text=article).grid(column=0, row=2)
        self.article_title_scrollbar = tk.Scrollbar(self.div2)
        self.article_title_scrollbar.grid(row=2, column=1)
        self.article_title_content = tk.Listbox(self.div2, width=50, yscrollcommand=self.article_title_scrollbar.set,selectmode=tk.SINGLE)
        self.article_title_content.insert("end", article)
        self.article_title_content.grid(row=2, column=0)
        self.article_title_scrollbar.config(command=self.article_title_listbox.yview)


        reply_message = get_reply_message(self.comunity_temp, self.article_title_temp)
        self.article_title_scrollbar2 = tk.Scrollbar(self.div2)
        self.article_title_scrollbar2.grid(row=3, column=1)
        self.article_title_listbox = tk.Listbox(self.div2, width=50, yscrollcommand=self.article_title_scrollbar2.set,selectmode=tk.SINGLE)
        for i in range(len(reply_message)):
            self.article_title_listbox.insert("end", reply_message[i])
        self.article_title_listbox.grid(row=3, column=0)
        self.article_title_scrollbar2.config(command=self.article_title_listbox.yview)
        self.reply_message_input = tk.StringVar()
        self.article_title_label = tk.Label(self.div3, width=50, text="請輸入reply message").grid(column=0, row=0)
        self.article_reply_input = tk.Entry(self.div3, width=40, textvariable=self.reply_message_input).grid(column=0, row=1)

        self.article_buttom = tk.Button(self.div3, text='create reply', command=self.add_reply_message).grid(column=0,row=4)

    def clear1(self):
        for widget in self.div1.winfo_children():
            widget.destroy()

    def clear2(self):
        for widget in self.div2.winfo_children():
            widget.destroy()

    def clear3(self):
        for widget in self.div3.winfo_children():
            widget.destroy()

    def clear4(self):
        for widget in self.div4.winfo_children():
            widget.destroy()

    def main(self):
        self.now_page = "main"
        self.clear2()
        self.comunity_label = tk.Label(self.div1, width=50, text=key_to_address(self.private_key.get())).grid(column=0, row=0, columnspan=4)
        self.bt1 = tk.Button(self.div1, text='所有版面', command=self.show_comunity)
        self.bt1.grid(column=0, row=1, sticky=self.align_mode)
        self.bt2 = tk.Button(self.div1, text='上一頁', command=self.bt2)
        self.bt2.grid(column=1, row=1, sticky=self.align_mode)
        self.bt3 = tk.Button(self.div1, text='登出', command=self.bt3)
        self.bt3.grid(column=2, row=1, sticky=self.align_mode)
        self.bt4 = tk.Button(self.div1, text='Quit', command=self.del_window)
        self.bt4.grid(column=3, row=1, sticky=self.align_mode)

    def get_size(self, event):
        self.w, self.h = self.div2.winfo_width(), self.div2.winfo_height()


    def bt2(self):
        self.clear2()
        self.clear3()
        self.clear4()
        if self.now_page=="main":
            self.window.destroy()
            APP()
        elif self.now_page=="comunity":
            self.now_page = "main"
        elif self.now_page=="article_title":
            self.show_comunity()
        elif self.now_page=="article":
            self.comunity_listbox_empty = 0
            self.show_article_title()

    def bt3(self):
        # self.clear1()
        # self.clear2()
        # self.clear3()
        # self.clear4()
        self.window.destroy()
        APP()

    def del_window(self):
        self.window.destroy()

    def toggle_fullScreen(self, event):
        is_windows = lambda: 1 if platform.system() == 'Windows' else 0
        self.isFullScreen = not self.isFullScreen
        self.window.attributes("-fullscreen" if is_windows() else "-zoomed", self.isFullScreen)

    def define_layout(self, obj, cols=1, rows=1):
        def method(trg, col, row):
            [trg.columnconfigure(c, minsize=self.div_size, weight=1) for c in range(cols)]
            [trg.rowconfigure(r, minsize=self.div_size, weight=1) for r in range(rows)]
        if type(obj) == list:
            [method(trg, cols, rows) for trg in obj]
        else:
            method(obj, cols, rows)



APP()