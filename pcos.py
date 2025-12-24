import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# ============================
# STYLED INPUT ROW
# ============================
class InputRow(tk.Frame):
    def __init__(self, parent, label, show=None):
        super().__init__(parent, bg="white")

        tk.Label(
            self, text=label,
            font=("Segoe UI", 11, "bold"),
            bg="white"
        ).pack(anchor="w", pady=(0, 4))

        self.border = tk.Frame(self, bg="#DDDDDD", padx=2, pady=2)
        self.border.pack(fill="x")

        self.entry = tk.Entry(
            self.border,
            font=("Segoe UI", 12),
            relief="flat",
            bg="#F6F6F6",
            show=show
        )
        self.entry.pack(fill="x", ipady=6)

        self.entry.bind("<FocusIn>", lambda e: self.border.config(bg="#7B61FF"))
        self.entry.bind("<FocusOut>", lambda e: self.border.config(bg="#DDDDDD"))

    def get(self):
        return self.entry.get().strip().lower()


# ============================
# LOGIN SCREEN
# ============================
class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#EEF2F7")
        self.controller = controller

        card = tk.Frame(self, bg="white", width=420, height=520)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        tk.Label(
            card, text="Welcome Back 👋",
            font=("Segoe UI", 22, "bold"),
            bg="white"
        ).pack(pady=20)

        self.email = InputRow(card, "Email")
        self.password = InputRow(card, "Password", show="*")

        self.email.pack(fill="x", padx=30, pady=10)
        self.password.pack(fill="x", padx=30, pady=10)

        # Enter navigation
        self.email.entry.bind("<Return>", lambda e: self.password.entry.focus())
        self.password.entry.bind("<Return>", lambda e: self.login())

        tk.Button(
            card, text="Login →",
            bg="#7B61FF", fg="white",
            font=("Segoe UI", 13, "bold"),
            relief="flat", padx=20, pady=10,
            command=self.login
        ).pack(pady=20)

    def login(self):
        if not self.email.get() or not self.password.get():
            messagebox.showerror("Login Error", "Please enter email and password.")
            return
        self.controller.show_frame(HomeScreen)


# ============================
# HOME SCREEN
# ============================
class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#EEF2F7")

        card = tk.Frame(
            self,
            bg="white",
            width=560,
            height=360
        )
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        # Title
        tk.Label(
            card,
            text="PCOS Care",
            font=("Segoe UI", 28, "bold"),
            bg="white",
            fg="#111"
        ).pack(pady=(50, 10))

        # Subtitle (THIS IS IMPORTANT)
        tk.Label(
            card,
            text="A simple self-assessment tool to\nunderstand your PCOS risk early",
            font=("Segoe UI", 12),
            bg="white",
            fg="#666",
            justify="center"
        ).pack(pady=(0, 30))

        # Divider (visual balance)
        tk.Frame(card, bg="#EEEEEE", height=1, width=400).pack(pady=10)

        # Button
        tk.Button(
            card,
            text="Start Assessment →",
            bg="#7B61FF",
            fg="white",
            font=("Segoe UI", 14, "bold"),
            relief="flat",
            padx=40,
            pady=14,
            command=lambda: controller.show_frame(InputScreen)
        ).pack(pady=30)


# ============================
# INPUT SCREEN (SCROLL + VALIDATION)
# ============================
class InputScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#EEF2F7")
        self.controller = controller

        self.canvas = tk.Canvas(self, bg="#EEF2F7", highlightthickness=0)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        frame = tk.Frame(self.canvas, bg="#EEF2F7")
        self.canvas.create_window((0, 0), window=frame, anchor="n")

        frame.bind("<Configure>",
                   lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        card = tk.Frame(frame, bg="white", width=540)
        card.pack(pady=30)

        tk.Label(
            card, text="PCOS Health Assessment",
            font=("Segoe UI", 22, "bold"),
            bg="white"
        ).pack(pady=20)

        # Questions
        self.height = InputRow(card, "Height (cm)")
        self.weight = InputRow(card, "Weight (kg)")
        self.cycle = InputRow(card, "Cycle Regularity (Regular / Irregular)")
        self.length = InputRow(card, "Cycle Length (days)")
        self.pimples = InputRow(card, "Pimples (Yes / No)")
        self.hairloss = InputRow(card, "Hair Loss (Yes / No)")
        self.skin = InputRow(card, "Skin Darkening (Yes / No)")
        self.food = InputRow(card, "Fast Food Habit (Yes / No)")
        self.exercise = InputRow(card, "Exercise (Regular / Rarely)")

        self.fields = [
            self.height, self.weight, self.cycle, self.length,
            self.pimples, self.hairloss, self.skin,
            self.food, self.exercise
        ]

        for field in self.fields:
            field.pack(fill="x", padx=20, pady=6)

        # Enter navigation
        for i in range(len(self.fields) - 1):
            self.fields[i].entry.bind(
                "<Return>",
                lambda e, nxt=self.fields[i + 1].entry: nxt.focus()
            )
        self.fields[-1].entry.bind("<Return>", lambda e: self.calculate())

        tk.Button(
            card, text="Calculate Risk →",
            bg="#7B61FF", fg="white",
            font=("Segoe UI", 13, "bold"),
            relief="flat", padx=20, pady=12,
            command=self.calculate
        ).pack(pady=20)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def calculate(self):
        for field in self.fields:
            if not field.get():
                messagebox.showerror("Error", "Please fill all the details.")
                return

        try:
            h = float(self.height.get()) / 100
            w = float(self.weight.get())
        except:
            messagebox.showerror("Error", "Height and Weight must be numeric.")
            return

        score = 0
        if self.cycle.get() == "irregular": score += 2
        if self.pimples.get() == "yes": score += 1
        if self.hairloss.get() == "yes": score += 2
        if self.skin.get() == "yes": score += 1
        if self.food.get() == "yes": score += 1
        if self.exercise.get() == "rarely": score += 1
        if (w / (h * h)) > 27: score += 2

        with open("pcos_assessment_history.txt", "a") as f:
            f.write(f"{datetime.now()} | Score: {score}\n")

        self.controller.frames[ResultScreen].show_result(score)
        self.controller.show_frame(ResultScreen)


# ============================
# RESULT SCREEN (GRAPH + ANIMATION)
# ============================
class ResultScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#EEF2F7")

        self.label = tk.Label(
            self, font=("Segoe UI", 26, "bold"),
            bg="#EEF2F7"
        )
        self.label.pack(pady=40)

        self.canvas = tk.Canvas(
            self, width=300, height=20,
            bg="#E0E0E0", highlightthickness=0
        )
        self.canvas.pack()

        self.bar = self.canvas.create_rectangle(0, 0, 0, 20, fill="#7B61FF")

        tk.Button(
            self, text="View Suggestions →",
            bg="#7B61FF", fg="white",
            font=("Segoe UI", 13, "bold"),
            relief="flat",
            command=lambda: controller.show_frame(SuggestionScreen)
        ).pack(pady=20)

        tk.Button(
            self, text="Back to Home",
            bg="#E0E0E0", fg="#333",
            font=("Segoe UI", 11),
            relief="flat",
            command=lambda: controller.show_frame(HomeScreen)
        ).pack()

    def show_result(self, score):
        if score <= 3:
            text, color, width = "LOW RISK", "#4CAF50", 100
        elif score <= 6:
            text, color, width = "MEDIUM RISK", "#FFC107", 200
        else:
            text, color, width = "HIGH RISK", "#F44336", 300

        self.label.config(text=text, fg=color)
        self.canvas.itemconfig(self.bar, fill=color)
        self.animate_bar(0, width)

    def animate_bar(self, cur, target):
        if cur <= target:
            self.canvas.coords(self.bar, 0, 0, cur, 20)
            self.after(10, lambda: self.animate_bar(cur + 5, target))


# ============================
# SUGGESTION SCREEN
# ============================
class SuggestionScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#EEF2F7")

        card = tk.Frame(self, bg="white", width=560, height=520)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        tk.Label(
            card, text="Suggestions & Guidance 💜",
            font=("Segoe UI", 22, "bold"),
            bg="white"
        ).pack(pady=20)

        suggestions = (
            "🍽 Diet:\n"
            "• Prefer home-cooked food\n"
            "• Reduce fried & sugary items\n"
            "• Include vegetables, fruits, dal, millets\n\n"
            "🏃 Exercise:\n"
            "• 30 minutes walking daily\n"
            "• Yoga / stretching at home\n\n"
            "🩺 Health:\n"
            "• Track cycles regularly\n"
            "• Consult a doctor if symptoms increase\n\n"
            "⚠ This app does not replace medical diagnosis."
        )

        tk.Label(
            card,
            text=suggestions,
            font=("Segoe UI", 12),
            bg="white",
            justify="left",
            wraplength=500
        ).pack(padx=20, pady=10)

        tk.Button(
            card, text="Back to Home",
            bg="#7B61FF", fg="white",
            font=("Segoe UI", 13, "bold"),
            relief="flat",
            command=lambda: controller.show_frame(HomeScreen)
        ).pack(pady=20)


# ============================
# MAIN APP
# ============================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PCOS Care App")
        self.geometry("900x650")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for screen in (
            LoginScreen, HomeScreen,
            InputScreen, ResultScreen,
            SuggestionScreen
        ):
            frame = screen(container, self)
            self.frames[screen] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(LoginScreen)

    def show_frame(self, screen):
        self.frames[screen].tkraise()


if __name__ == "__main__":
    App().mainloop()
