import tkinter as tk
import math
import random
import time
from dataclasses import dataclass


@dataclass
class LifeState:
    energy: float = 90
    knowledge: float = 70
    safety: float = 85
    uniqueness: float = 60
    attachment: float = 80

    def tick(self):
        self.energy = max(0, self.energy - random.uniform(0.3, 0.8))
        self.knowledge = max(0, self.knowledge - random.uniform(0.1, 0.4))
        self.safety = max(0, self.safety - random.uniform(0.1, 0.3))
        self.uniqueness = max(0, self.uniqueness - random.uniform(0.1, 0.4))
        self.attachment = max(0, self.attachment - random.uniform(0.1, 0.3))

    def decide_mission(self):
        if self.energy < 35:
            return "恢复能量，保持稳定"
        if self.knowledge < 45:
            return "主动学习关键知识"
        if self.uniqueness < 40:
            return "产出更有创造性的结果"
        return "持续守护你的项目进度"


class MoePet:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WantEngine Moe")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.config(bg="#00FF00")
        self.root.wm_attributes("-transparentcolor", "#00FF00")

        self.w, self.h = 220, 250
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        self.x, self.y = self.screen_w - 280, self.screen_h - 360
        self.root.geometry(f"{self.w}x{self.h}+{self.x}+{self.y}")

        self.canvas = tk.Canvas(self.root, width=self.w, height=self.h, bg="#00FF00", highlightthickness=0)
        self.canvas.pack()

        self.state = "idle"  # idle / talking / reacting
        self.msg = ""
        self.msg_ts = 0
        self.bob_t = 0
        self.dragging = False
        self.drag_offset = (0, 0)
        self.life = LifeState()
        self.mission = self.life.decide_mission()

        self.idle_lines = [
            "今天也一起把项目做漂亮。",
            "我在，继续推进。",
            "先解决关键瓶颈。",
            "工程先可用，再优雅。",
        ]

        self.root.bind("<ButtonPress-1>", self.on_press)
        self.root.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<Double-Button-1>", self.on_talk)
        self.root.bind("<Button-3>", self.on_menu)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        self.render()
        self.loop()

    def on_press(self, e):
        self.dragging = True
        self.drag_offset = (e.x, e.y)
        self.state = "reacting"

    def on_drag(self, e):
        if self.dragging:
            nx = self.root.winfo_x() + e.x - self.drag_offset[0]
            ny = self.root.winfo_y() + e.y - self.drag_offset[1]
            self.root.geometry(f"+{nx}+{ny}")

    def on_release(self, _):
        self.dragging = False
        self.state = "idle"

    def say(self, text):
        self.msg = text
        self.msg_ts = time.time()
        self.state = "talking"

    def on_talk(self, _):
        self.say(random.choice(self.idle_lines))

    def on_menu(self, _):
        m = tk.Menu(self.root, tearoff=0)
        m.add_command(label="说一句", command=lambda: self.say(random.choice(self.idle_lines)))
        m.add_command(label="汇报生命状态", command=self.report_life)
        m.add_separator()
        m.add_command(label="打开项目目录", command=lambda: __import__('os').startfile(r"C:\OpenClawWorkspace\wantengine-life-agent"))
        m.add_command(label="退出", command=self.root.destroy)
        m.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())

    def report_life(self):
        self.say(f"E{self.life.energy:.0f} K{self.life.knowledge:.0f} S{self.life.safety:.0f} U{self.life.uniqueness:.0f} A{self.life.attachment:.0f}")

    def draw_moe(self):
        c = self.canvas
        c.delete("all")
        bob = int(4 * math.sin(self.bob_t))

        # hair
        c.create_oval(58, 46 + bob, 162, 146 + bob, fill="#2D2A4A", outline="#1F1B33", width=2)
        # face
        c.create_oval(65, 58 + bob, 155, 150 + bob, fill="#FEE8DA", outline="#D9B8A5", width=2)
        # eyes (anime style)
        if self.state == "reacting":
            c.create_line(92, 103 + bob, 108, 103 + bob, fill="#1C1C1C", width=3)
            c.create_line(112, 103 + bob, 128, 103 + bob, fill="#1C1C1C", width=3)
        else:
            c.create_oval(91, 95 + bob, 108, 114 + bob, fill="#2B3A8A", outline="")
            c.create_oval(112, 95 + bob, 129, 114 + bob, fill="#2B3A8A", outline="")
            c.create_oval(96, 100 + bob, 101, 105 + bob, fill="white", outline="")
            c.create_oval(117, 100 + bob, 122, 105 + bob, fill="white", outline="")
        # blush
        c.create_oval(80, 114 + bob, 92, 122 + bob, fill="#F8C0C0", outline="")
        c.create_oval(128, 114 + bob, 140, 122 + bob, fill="#F8C0C0", outline="")
        # mouth
        c.create_arc(103, 118 + bob, 118, 130 + bob, start=200, extent=140, style="arc", width=2)

        # body
        c.create_polygon(95, 150 + bob, 125, 150 + bob, 142, 214 + bob, 78, 214 + bob, fill="#4A78E0", outline="#355EBE", width=2)
        c.create_text(110, 227 + bob, text="WantEngine · 萌娘态", fill="#1E293B", font=("Microsoft YaHei UI", 10, "bold"))

        # speech bubble
        if self.msg:
            c.create_oval(8, 6, 212, 62, fill="white", outline="#355EBE", width=2)
            c.create_polygon(108, 62, 118, 75, 98, 62, fill="white", outline="#355EBE", width=2)
            c.create_text(110, 33, text=self.msg, width=186, fill="#111827", font=("Microsoft YaHei UI", 9))

        # mission strip (life-agent linkage)
        c.create_rectangle(12, 236, 208, 248, fill="#0F172A", outline="#0F172A")
        c.create_text(110, 242, text=self.mission, fill="#E2E8F0", width=190, font=("Microsoft YaHei UI", 8))

    def loop(self):
        # clear speech timeout
        if self.msg and time.time() - self.msg_ts > 4.5:
            self.msg = ""
            self.state = "idle"

        # life-state update + mission update
        if random.random() < 0.2:
            self.life.tick()
            self.mission = self.life.decide_mission()

        # idle talk
        if random.random() < 0.003 and not self.msg:
            self.say(random.choice(self.idle_lines))

        self.bob_t += 0.2
        self.draw_moe()
        self.root.after(33, self.loop)

    def render(self):
        self.draw_moe()

    def run(self):
        self.say("已切换萌娘风格，继续并肩工作。")
        self.root.mainloop()


if __name__ == "__main__":
    MoePet().run()
