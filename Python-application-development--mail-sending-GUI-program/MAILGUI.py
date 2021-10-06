from tkinter import * #tkinter编写的GUI程序
from PIL import Image,ImageTk #由于我们设置窗口图片背景，所以要引入pil库，对应的通用库名为Pillow 库
from MAIL import MAIL #需要导入MAIL类
import datetime #用来获取时间
import calendar #用来生成日历形式的库
import tkinter.filedialog #tk库里的文件选择框模块
class MAILGUI(MAIL):#继承自MAIL类
    def __init__(self):
        super().__init__()
        # 主窗口设置
        self.root = Tk()  # 程序主窗体
        self.root.title('基于SMTP协议自动发送的邮箱程序')  # 设置窗口标题
        self.root.geometry('800x600+300+100')  # 设置窗口大小和在系统显示下的位置
        self.root.iconbitmap('mail.ico')  # 设置窗体图标
        self.lists=[''] #由于后面以第一个列表元素作为显示，所以初始元素先设置为空字符串
        self.filename = '' #初始化附件地址变量

        photo1=Image.open('background1.png')#同代码文件目录下的图片文件，用于日历背景
        self.background_image1 = ImageTk.PhotoImage(photo1.resize((500, 400)))

        # GUI组件
        # 收件人提示标签
        to_label = Label(self.root, text='收件人：', font=('黑体', 13)).place(x=10, y=20)
        # 收件人输入框
        self.to_text = Text(self.root, width=26, height=1.55, font=('黑体', 13))
        self.to_text.place(x=90, y=20)

        # 邮件主题标签
        title_label = Label(self.root, text='主题：', font=('黑体', 13)).place(x=10, y=80)
        # 邮件主题输入框
        self.title_text = Text(self.root, width=26, height=1.55, font=('黑体', 13))
        self.title_text.place(x=90, y=80)

        # 邮件内容提示标签
        contents_label = Label(self.root, text='内容：', font=('黑体', 13)).place(x=10, y=140)
        # 邮件内容输入框
        self.content_text = Text(self.root, width=75, height=12, font=('黑体', 13))
        self.content_text.place(x=90, y=140)

        #邮件附件按钮
        attachments_button = Button(self.root, text='附件地址', font=('黑体', 13), fg='white', bg='green', command=self.Attachments,width=10, height=2, relief=RAISED)
        attachments_button.place(x=30, y=370)
        #邮件附件提示标签
        self.attachments_label=Label(self.root, text='暂无选择文件', font=('黑体', 9),width=80, height=3, fg='white', bg='green')
        self.attachments_label.place(x=180, y=370)


        #邮件发送确认按钮
        check_button = Button(self.root, text='确认发送', font=('黑体', 13), fg='white', bg='green', command=self.Sendto, width=10,height=2, relief=RAISED).place(x=30, y=450)

        #程序状态标签
        tip_label = Label(self.root, text='程序状态：', font=('黑体', 13)).place(x=10, y=530)

        # 其文本内容对应着实际操作程序的操作提示的标签
        self.tipout_label = Label(self.root, text='暂无操作！', font=('黑体', 13), bg='green', fg='white')
        self.tipout_label.place(x=120, y=530)

        # 用于时间显示标签
        self.time_label = Label(self.root, text='', font=('黑体', 16), fg='green')
        self.time_label.place(x=340, y=85)

        self.menubar = Menu(self.root)  # 主菜单
        self.menuout = Menu(self.root, tearoff=0)  # 弹出菜单，清楚功能实现的汇集
        self.root['menu'] = self.menubar  # 设置主菜单
        # 菜单项加入：
        self.menubar.add_command(label="初始化配置文件  ", command=self.creatconfig)#初始化配置文件的菜单选项功能
        self.menubar.add_command(label="  打开配置文件  ", command=self.openconfig)#打开配置文件的菜单选项功能
        self.menubar.add_command(label="  草稿   ", command=self.textbook)
        self.menubar.add_command(label="  日历  ", command=self.show_datetime)
        self.root.bind("<Button-3>", self.pops)  # <Button-3>为右键点击事件，用于触发弹出菜单
        self.menuout.add_command(label='清空收件人窗口', command=self.Clear_to)
        self.menuout.add_command(label='清空主题窗口', command=self.Clear_title)
        self.menuout.add_command(label='清空内容窗口', command=self.Clear_content)
        self.menuout.add_command(label='清空附件地址', command=self.Clear_attachments)
        self.menuout.add_command(label='清空所有输入窗口', command=self.message)
        self.root.mainloop()

    # 附件控件控制函数
    def Attachments(self):
        self.filename = tkinter.filedialog.askopenfilename()  # 在弹出框内选择文件，并获得字符串型的文件地址
        if self.filename != '':  # 用filename是否为空字符串来判断，如果没选择的，就用初始量
            self.tipout_label['text'] = '您选择了附件文件！'
            self.attachments_label['text'] = '您选择的文件是' + self.filename
        else:
            self.tipout_label['text'] = '您没有选择任何文件!'
            self.attachments_label['text'] = '您还没选择任何文件!'

    # 主函数：处理邮件发送
    def Sendto(self):
        to = self.to_text.get('1.0', 'end')  # 获取相关内容
        title = self.title_text.get('1.0', 'end')
        content = self.content_text.get('1.0', 'end')
        if self.filename == '':  # 根据filename值来选择发送时是否包含附件
            try:  # 检查邮件发送是否成功很重要；
                self.mail.send(to, title, content)
                self.tipout_label['text'] = "发送成功！"
            except:
                self.message()
        elif self.filename != '':
            try:
                self.mail.send(to, title, content, self.filename)
                self.tipout_label['text'] = "发送成功！"
            except:
                self.message()

    def show_datetime(self):  # 利用calendar库显示日历的窗口
        winnew = Toplevel(self.root)  # 顶层窗体
        winnew.title('日历窗口')
        winnew.geometry('500x400+700+50')
        winnew.iconbitmap('mail.ico')  # 设置窗口图标，统一使用同一张
        self.tipout_label['text'] = '你点开了日历窗口！'  # 操作变化提示，基本每个模块被使用时都会含有
        date_time = datetime.datetime.today()
        year = date_time.year  # 获取当前年份
        month = date_time.month  # 获取当前月份
        calendar.setfirstweekday(firstweekday=6)  # 设置日历的初始天（第一天）
        dates = calendar.month(year, month)  # 获得日历的字符串类型
        alldate = Label(winnew, text='', bg='green', fg='white', width=1000, height=600, font=('黑体', 20),
                        image=self.background_image1, compound=CENTER)
        alldate.configure(text=dates)
        alldate.pack()

    def textbook(self):# 草稿操作的窗口
        text_win = Toplevel(self.root)
        text_win.title('草稿窗口')
        text_win.geometry('740x520+500+50')
        text_win.iconbitmap('mail.ico')
        self.tipout_label['text'] = '你点开了草稿窗口！'
        self.draft_paper = Text(text_win, width=100, height=30)  # 该实例为草稿箱输入和文本显示框功能
        self.draft_paper.insert('1.0', self.lists[0])  # 插入所保存的内容，相当记忆重现，实现了保存功能逻辑
        save_button = Button(text_win, text='保存', command=self.saves, relief=RAISED, fg='white', bg='green', font=('黑体', 14),
                             width=10, height=2).place(x=19, y=430)
        clear_button = Button(text_win, text='清空所有内容', command=self.clears, relief=RAISED, fg='white', bg='green',
                              font=('黑体', 14), width=16, height=2).place(x=150, y=430)
        self.draft_paper.place(x=19, y=18)

    def saves(self):#保存了草稿箱里的内容的方法
        self.lists[0] = self.draft_paper.get(1.0, 'end')  # 点击保存按钮，触发获取文本框的内容，可在编写过程任一时刻保存，避免丢失
        self.tipout_label['text'] = "你保存了草稿箱里的内容！"

    def clears(self):#清空草稿箱里的内容的方法
        self.draft_paper.delete('1.0', 'end')
        self.tipout_label['text'] = "你清空了草稿箱里的内容！"

    # 用于其他模块下错误信息提示的使用，使用时调用即可
    def message(self):
        self.tipout_label['text'] = "输入有误或已全清空！请重新输入所有内容！"
        self.to_text.delete('1.0', 'end')  # 文本框控件中第一个字符的位置是 1.0，可以用数字 1.0 或字符串"1.0"来表示
        self.title_text.delete('1.0', 'end')
        self.content_text.delete('1.0', 'end')
        self.filename=''
        self.tipout_label['text']='你清空了所有输入内容！包括收件人，主题，内容，附件地址的所有输入！'
        self.attachments_label['text']='您还没选择任何文件!'

    def pops(self,event):  # 右键响应函数，弹出菜单
        self.menuout.post(event.x_root, event.y_root)  # 这两个变量可让在在窗口任一触发部位弹出

    def Clear_to(self):  # 清空收件人输入框函数
        self.to_text.delete('1.0', 'end')
        self.tipout_label['text'] = '你清空了收件人窗口！'

    def Clear_title(self):  # 清空邮件主题输入框的方法
        self.title_text.delete('1.0', 'end')
        self.tipout_label['text'] = '你清空了主题窗口！'

    def Clear_content(self):  # 清空邮件内容输入框的方法
        self.content_text.delete('1.0', 'end')
        self.tipout_label['text'] = '你清空了内容窗口！'

    def Clear_attachments(self):
        self.filename=''
        self.tipout_label['text'] = '你清除了附件地址！'
        self.attachments_label['text'] = '您还没选择任何文件!'


if __name__ == '__main__':
    MAILGUI()



