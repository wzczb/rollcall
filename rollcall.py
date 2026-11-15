import tkinter as tk
from tkinter import filedialog, messagebox
import random

class RollCall:
    def __init__(self, root):
        self.root = root
        self.root.title("随机点名器")
        self.root.geometry("680x420")
        self.root.config(bg="#f7f8fa")

        self.student_list = []
        self.is_running = False
        self.timer_id = None

        self.label_title = tk.Label(root, text="随机点名器", font=("微软雅黑", 24), bg="#f7f8fa", fg="#333333")
        self.label_title.pack(pady=20)

        self.label_name = tk.Label(root, text="等待点名", font=("微软雅黑", 60, "bold"), bg="#f7f8fa", fg="#222222")
        self.label_name.pack(pady=10)

        frame_btn = tk.Frame(root, bg="#f7f8fa")
        frame_btn.pack(pady=30)

        self.btn_load = tk.Button(frame_btn, text="导入名单", command=self.load_file, width=12, height=2, font=("微软雅黑",12))
        self.btn_load.grid(row=0, column=0, padx=8)

        self.btn_start = tk.Button(frame_btn, text="开始点名", command=self.toggle_run, width=12, height=2, font=("微软雅黑",12))
        self.btn_start.grid(row=0, column=1, padx=8)

        self.btn_reset = tk.Button(frame_btn, text="重置", command=self.reset, width=12, height=2, font=("微软雅黑",12))
        self.btn_reset.grid(row=0, column=2, padx=8)

        self.auto_load()

    def auto_load(self):
        try:
            with open("students.txt", "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                self.student_list = lines
        except:
            pass

    def load_file(self):
        path = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
            if not lines:
                messagebox.showwarning("提示", "名单文件为空！")
                return
            self.student_list = lines
            messagebox.showinfo("成功", f"导入{len(self.student_list)}名学生")
        except Exception as e:
            messagebox.showerror("错误", f"读取失败：{e}")

    def toggle_run(self):
        if not self.student_list:
            messagebox.showwarning("提示", "请先导入名单！")
            return
        if self.is_running:
            self.is_running = False
            self.btn_start.config(text="开始点名")
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
        else:
            self.is_running = True
            self.btn_start.config(text="停止")
            self.roll()

    def roll(self):
        if not self.is_running:
            return
        name = random.choice(self.student_list)
        self.label_name.config(text=name)
        self.timer_id = self.root.after(60, self.roll)

    def reset(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.is_running = False
        self.btn_start.config(text="开始点名")
        self.label_name.config(text="等待点名")

if __name__ == "__main__":
    window = tk.Tk()
    app = RollCall(window)
    window.mainloop()
