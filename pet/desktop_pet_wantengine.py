import tkinter as tk
import random
import math
import time


class DesktopPet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.config(bg='magenta')
        self.root.wm_attributes('-transparentcolor', 'magenta')

        self.w = 170
        self.h = 180
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()

        self.x = random.randint(100, self.screen_w - 260)
        self.y = random.randint(100, self.screen_h - 280)
        self.dx = 3
        self.dy = 2
        self.bob_t = 0

        self.root.geometry(f"{self.w}x{self.h}+{self.x}+{self.y}")

        self.canvas = tk.Canvas(self.root, width=self.w, height=self.h, bg='magenta', highlightthickness=0)
        self.canvas.pack()

        self.dragging = False
        self.drag_offset = (0, 0)
        self.last_speak = 0
        self.speech = ""

        self.messages = [
            "继续推进，先做最关键的。",
            "已切到工程模式。",
            "先标准化，再扩展。",
            "保持专注，交付优先。",
            "要不要我继续整理文件？"
        ]

        self.root.bind('<ButtonPress-1>', self.on_press)
        self.root.bind('<B1-Motion>', self.on_drag)
        self.root.bind('<ButtonRelease-1>', self.on_release)
        self.root.bind('<Double-Button-1>', self.on_double_click)
        self.root.bind('<Button-3>', self.on_right_click)
        self.root.bind('<Escape>', lambda e: self.root.destroy())

        self.draw_pet()
        self.animate()

    def draw_pet(self):
        self.canvas.delete('all')

        bob = int(4 * math.sin(self.bob_t))

        # body
        self.canvas.create_oval(45, 45 + bob, 125, 125 + bob, fill='#4A90E2', outline='#2C5EA8', width=3)
        # ears
        self.canvas.create_polygon(58, 56 + bob, 43, 26 + bob, 73, 44 + bob, fill='#4A90E2', outline='#2C5EA8', width=2)
        self.canvas.create_polygon(112, 56 + bob, 127, 26 + bob, 97, 44 + bob, fill='#4A90E2', outline='#2C5EA8', width=2)
        # eyes
        self.canvas.create_oval(67, 73 + bob, 77, 83 + bob, fill='white', outline='')
        self.canvas.create_oval(93, 73 + bob, 103, 83 + bob, fill='white', outline='')
        self.canvas.create_oval(71, 76 + bob, 75, 80 + bob, fill='black', outline='')
        self.canvas.create_oval(97, 76 + bob, 101, 80 + bob, fill='black', outline='')
        # mouth
        self.canvas.create_arc(73, 87 + bob, 97, 103 + bob, start=200, extent=140, style='arc', width=2)

        # name
        self.canvas.create_text(85, 138 + bob, text='WantEngine 🤖', fill='#1F2937', font=('Segoe UI', 10, 'bold'))

        # speech bubble
        if self.speech:
            self.canvas.create_oval(6, 2, 164, 46, fill='white', outline='#2C5EA8', width=2)
            self.canvas.create_polygon(84, 46, 94, 58, 74, 46, fill='white', outline='#2C5EA8', width=2)
            self.canvas.create_text(85, 24, text=self.speech, fill='#111827', font=('Microsoft YaHei UI', 9), width=145)

    def speak(self, text):
        self.speech = text
        self.last_speak = time.time()

    def on_press(self, event):
        self.dragging = True
        self.drag_offset = (event.x, event.y)

    def on_drag(self, event):
        if self.dragging:
            new_x = self.root.winfo_x() + event.x - self.drag_offset[0]
            new_y = self.root.winfo_y() + event.y - self.drag_offset[1]
            self.root.geometry(f"+{new_x}+{new_y}")

    def on_release(self, _event):
        self.dragging = False

    def on_double_click(self, _event):
        self.speak(random.choice(self.messages))

    def on_right_click(self, _event):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label='说一句', command=lambda: self.speak(random.choice(self.messages)))
        menu.add_command(label='打开工作目录', command=self.open_workspace)
        menu.add_separator()
        menu.add_command(label='退出宠物', command=self.root.destroy)
        menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())

    def open_workspace(self):
        import os
        os.startfile(r'C:\OpenClawWorkspace')

    def animate(self):
        if not self.dragging:
            x = self.root.winfo_x() + self.dx
            y = self.root.winfo_y() + self.dy

            if x <= 0 or x + self.w >= self.screen_w:
                self.dx *= -1
            if y <= 0 or y + self.h >= self.screen_h - 48:
                self.dy *= -1

            self.root.geometry(f"+{x}+{y}")

        # speech timeout
        if self.speech and time.time() - self.last_speak > 5:
            self.speech = ''

        # occasional auto speech
        if random.random() < 0.002:
            self.speak(random.choice(self.messages))

        self.bob_t += 0.22
        self.draw_pet()
        self.root.after(30, self.animate)

    def run(self):
        self.speak('已上线，持续待命。')
        self.root.mainloop()


if __name__ == '__main__':
    DesktopPet().run()
