import customtkinter as ctk
from tkinter import filedialog, messagebox
import random

ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("blue")

class RollCall:
    def __init__(self, root):
        self.root = root
        self.root.title("随机点名器")
        self.root.geometry("750x480")
        self.root.resizable(False, False)

        self.student_list = []
        self.is_running = False
        self.timer_id = None

        self.label_title = ctk.CTkLabel(
            root,
            text="随机点名器",
            font=("微软雅黑", 30, "bold")
        )
        self.label_title.pack(pady=30)

        self.label_name = ctk.CTkLabel(
            root,
            text="等待点名",
            font=("微软雅黑", 80, "bold"),
            width=600,
            height=140,
            fg_color="#ffffff",
            corner_radius=16
        )
        self.label_name.pack(pady=10)

        frame_btn = ctk.CTkFrame(root, fg_color="transparent")
        frame_btn.pack(pady=40)

        self.btn_load = ctk.CTkButton(
            frame_btn,
            text="导入名单",
            command=self.load_file,
            width=160,
            height=48,
            font=("微软雅黑",15)
        )
        self.btn_load.grid(row=0, column=0, padx=12)

        self.btn_start = ctk.CTkButton(
            frame_btn,
            text="开始点名",
            command=self.toggle_run,
            width=160,
            height=48,
            font=("微软雅黑",15),
            fg_color="#27ae60",
            hover_color="#219653"
        )
        self.btn_start.grid(row=0, column=1, padx=12)

        self.btn_reset = ctk.CTkButton(
            frame_btn,
            text="重置",
            command=self.reset,
            width=160,
            height=48,
            font=("微软雅黑",15),
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        self.btn_reset.grid(row=0, column=2, padx=12)

        self.auto_load()

    def auto_load(self):
        try:
            with open("students.txt", "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                self.student_list = lines
        except Exception:
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
            self.btn_start.configure(text="开始点名", fg_color="#27ae60", hover_color="#219653")
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
        else:
            self.is_running = True
            self.btn_start.configure(text="停止", fg_color="#f39c12", hover_color="#e67e22")
            self.roll()

    def roll(self):
        if not self.is_running:
            return
        name = random.choice(self.student_list)
        self.label_name.configure(text=name)
        self.timer_id = self.root.after(60, self.roll)

    def reset(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.is_running = False
        self.btn_start.configure(text="开始点名", fg_color="#27ae60", hover_color="#219653")
        self.label_name.configure(text="等待点名")

if __name__ == "__main__":
    app = ctk.CTk()
    window = RollCall(app)
    app.mainloop()