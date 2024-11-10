import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import json
import os
import random

DATA_FILE = "data.json"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("错题整理")
        self.geometry("600x600")
        self.configure(bg="#d3d3d3")

        # Load saved data or initialize an empty list
        self.data = self.load_data()

        # Initialize pages
        self.main_page = MainPage(self)
        self.add_page = AddPage(self)
        self.review_page = ReviewPage(self)
        self.detail_page = DetailPage(self)
        self.quiz_page = QuizPage(self)

        # Show the main page initially
        self.main_page.pack(expand=True, fill='both')

    def show_main_page(self):
        self.clear_all_pages()
        self.main_page.pack(expand=True, fill='both')

    def show_add_page(self):
        self.clear_all_pages()
        self.add_page.pack(expand=True, fill='both')

    def show_review_page(self):
        self.clear_all_pages()
        self.review_page.update_list()
        self.review_page.pack(expand=True, fill='both')

    def show_detail_page(self, entry_index):
        self.clear_all_pages()
        self.detail_page.display_entry(entry_index)
        self.detail_page.pack(expand=True, fill='both')

    def show_quiz_page(self):
        self.clear_all_pages()
        self.quiz_page.start_quiz()
        self.quiz_page.pack(expand=True, fill='both')

    def clear_all_pages(self):
        self.main_page.pack_forget()
        self.add_page.pack_forget()
        self.review_page.pack_forget()
        self.detail_page.pack_forget()
        self.quiz_page.pack_forget()

    def save_data_to_file(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        return []

class MainPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#d3d3d3")
        current_date = datetime.now().strftime("%Y-%m-%d")
        date_label = tk.Label(self, text=current_date, bg="#d3d3d3", fg="black", font=("Helvetica", 12))
        date_label.place(x=10, y=10)

        self.grid_columnconfigure((0, 2), weight=1)
        self.grid_rowconfigure(1, weight=1)

        button_options = {
            "bg": "#66c2c7",
            "fg": "black",
            "font": ("Helvetica", 20),
            "width": 4,
            "height": 2
        }

        button1 = tk.Button(self, text="添加", **button_options, command=master.show_add_page)
        button1.grid(row=1, column=0, padx=10, pady=10)

        button2 = tk.Button(self, text="复习", **button_options, command=master.show_review_page)
        button2.grid(row=1, column=1, padx=10, pady=10)

        button3 = tk.Button(self, text="自测", **button_options, command=master.show_quiz_page)
        button3.grid(row=1, column=2, padx=10, pady=10)

class AddPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#d3d3d3")
        current_date = datetime.now().strftime("%Y-%m-%d")
        date_label = tk.Label(self, text="日期: " + current_date, bg="#d3d3d3", font=("Helvetica", 20))
        date_label.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        question_label = tk.Label(self, text="添加题目", bg="#d3d3d3", font=("Helvetica", 20))
        question_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.image_label = tk.Label(self, bg="#d3d3d3")
        self.image_label.grid(row=1, column=1, padx=20, pady=10, sticky="n")

        upload_button = tk.Button(self, text="上传图片", command=self.upload_image)
        upload_button.grid(row=2, column=1, padx=20, pady=10, sticky="e")

        answer_label = tk.Label(self, text="答案", bg="#d3d3d3", font=("Helvetica", 20))
        answer_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        answer_frame = tk.Frame(self, bg="#d3d3d3")
        answer_frame.grid(row=3, column=1, padx=20, pady=10, sticky="nsew")

        self.answer_text = tk.Text(answer_frame, width=40, height=8, wrap="word")
        answer_scrollbar = tk.Scrollbar(answer_frame, orient="vertical", command=self.answer_text.yview)
        self.answer_text.configure(yscrollcommand=answer_scrollbar.set)

        self.answer_text.pack(side="left", fill="both", expand=True)
        answer_scrollbar.pack(side="right", fill="y")

        save_button = tk.Button(self, text="保存", command=self.save_data)
        save_button.grid(row=4, column=1, pady=20)
        back_button = tk.Button(self, text="返回主页", command=master.show_main_page)
        back_button.grid(row=5, column=1, pady=20)

        self.image = None
        self.image_path = None

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            self.image_path = file_path
            image = Image.open(file_path)
            thumbnail_image = image.resize((200, 200), Image.LANCZOS)
            self.image = ImageTk.PhotoImage(thumbnail_image)
            self.image_label.config(image=self.image)

    def save_data(self):
        answer_text = self.answer_text.get("1.0", tk.END).strip()
        
        if self.image_path is None or not answer_text:
            messagebox.showwarning("Warning", "请上传图片并填写答案。")
            return

        entry_name = simpledialog.askstring("Save Entry", "请输入保存名称:")

        if entry_name:
            entry = {
                "name": entry_name,
                "image_path": self.image_path,
                "answer": answer_text
            }
            self.master.data.append(entry)
            self.master.save_data_to_file()
            messagebox.showinfo("Success", f"保存成功: {entry_name}")
            
            self.image_label.config(image='')
            self.image = None
            self.image_path = None
            self.answer_text.delete("1.0", tk.END)
            
            self.master.show_main_page()

class ReviewPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#d3d3d3")
        
        self.listbox = tk.Listbox(self, font=("Helvetica", 16))
        self.listbox.pack(expand=True, fill="both", padx=20, pady=20)

        back_button = tk.Button(self, text="返回", command=master.show_main_page)
        back_button.pack(pady=10)

        self.listbox.bind("<Double-1>", self.open_entry)

    def update_list(self):
        self.listbox.delete(0, tk.END)
        for entry in self.master.data:
            self.listbox.insert(tk.END, entry["name"])

    def open_entry(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            entry_index = selected_index[0]
            self.master.show_detail_page(entry_index)

class DetailPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#d3d3d3")
        self.current_index = None

        self.image_label = tk.Label(self, bg="#d3d3d3")
        self.image_label.pack(pady=10)

        self.image_label.bind("<Button-1>", self.show_full_image)

        self.answer_text = tk.Text(self, width=40, height=8, wrap="word")
        self.answer_text.pack(pady=10)
        self.answer_text.config(state="disabled")

        nav_frame = tk.Frame(self, bg="#d3d3d3")
        nav_frame.pack(pady=10)
        
        prev_button = tk.Button(nav_frame, text="上一题", command=self.show_previous)
        prev_button.grid(row=0, column=0, padx=10)
        
        next_button = tk.Button(nav_frame, text="下一题", command=self.show_next)
        next_button.grid(row=0, column=1, padx=10)

        delete_button = tk.Button(nav_frame, text="删除", command=self.delete_entry)
        delete_button.grid(row=0, column=2, padx=10)

        back_button = tk.Button(nav_frame, text="返回主页", command=master.show_main_page)
        back_button.grid(row=0, column=3, padx=10)

    def show_full_image(self, event):
        if self.current_index is not None:
            original_image = Image.open(self.master.data[self.current_index]["image_path"])

            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            max_width = int(screen_width * 0.8)
            max_height = int(screen_height * 0.8)

            scale_factor = min(max_width / original_image.width, max_height / original_image.height, 1)
            resized_image = original_image.resize((int(original_image.width * scale_factor), int(original_image.height * scale_factor)), Image.LANCZOS)

            popup = tk.Toplevel(self)
            popup.title("原始图片")
            popup.geometry(f"{resized_image.width}x{resized_image.height}")

            original_img = ImageTk.PhotoImage(resized_image)
            img_label = tk.Label(popup, image=original_img)
            img_label.image = original_img
            img_label.pack()

    def show_previous(self):
        if self.current_index > 0:
            self.display_entry(self.current_index - 1)

    def show_next(self):
        if self.current_index < len(self.master.data) - 1:
            self.display_entry(self.current_index + 1)

    def delete_entry(self):
        if self.current_index is not None:
            del self.master.data[self.current_index]
            self.master.save_data_to_file()
            messagebox.showinfo("删除", "条目已删除")
            self.master.show_review_page()

    def display_entry(self, entry_index):
        self.current_index = entry_index
        entry = self.master.data[entry_index]
        image = Image.open(entry["image_path"]).resize((200, 200), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.image)
        
        self.answer_text.config(state="normal")
        self.answer_text.delete("1.0", tk.END)
        self.answer_text.insert("1.0", entry["answer"])
        self.answer_text.config(state="disabled")

class QuizPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f7f7f7")
        self.master = master
        self.data = master.data
        self.quiz_data = []
        self.image_cache = {}  # Cache images for faster loading
        self.current_index = 0
        self.is_answer_shown = False

        self.progress_label = tk.Label(self, text="自测：1/10", font=("Helvetica", 16), bg="#f7f7f7")
        self.progress_label.pack(anchor="nw", padx=20, pady=10)

        self.card_frame = tk.Frame(self, width=400, height=300, bg="#d3d3d3")
        self.card_frame.pack(padx=20, pady=20)

        self.action_button = tk.Button(self, text="完成", command=self.flip_card, font=("Helvetica", 14))
        self.action_button.pack(anchor="e", padx=20, pady=20)

    def load_image(self, path, size=None):
        """Load and cache images"""
        if path not in self.image_cache:
            image = Image.open(path)
            if size:
                image.thumbnail(size)
            self.image_cache[path] = ImageTk.PhotoImage(image)
        return self.image_cache[path]

    def show_full_image(self, event):
        """Show full image in a popup window with dynamic resizing"""
        if self.current_index is not None:
            entry = self.quiz_data[self.current_index]
            original_image = Image.open(entry["image_path"])

            screen_width, screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
            max_width, max_height = int(screen_width * 0.8), int(screen_height * 0.8)

            scale_factor = min(max_width / original_image.width, max_height / original_image.height, 1)
            resized_image = original_image.resize(
                (int(original_image.width * scale_factor), int(original_image.height * scale_factor)), Image.LANCZOS
            )

            popup = tk.Toplevel(self)
            popup.title("原始图片")
            popup.geometry(f"{resized_image.width}x{resized_image.height}")

            original_img = ImageTk.PhotoImage(resized_image)
            img_label = tk.Label(popup, image=original_img)
            img_label.image = original_img
            img_label.pack()

    def start_quiz(self):
        # Check if there are questions in the database
        if not self.data:
            messagebox.showinfo("提示", "错题未添加")
            self.master.show_main_page()  # Return to main page if no data
            return

        # Initialize quiz if there are questions available
        total_questions = min(10, len(self.data))
        self.quiz_data = random.sample(self.data, total_questions)
        self.current_index = 0
        self.update_progress()
        self.show_question()



    def update_progress(self):
        self.progress_label.config(text=f"自测：{self.current_index + 1}/{len(self.quiz_data)}")

    def show_question(self):
        entry = self.quiz_data[self.current_index]
        self.card_image = self.load_image(entry["image_path"], size=(400, 300))

        for widget in self.card_frame.winfo_children():
            widget.destroy()

        image_label = tk.Label(self.card_frame, image=self.card_image, bg="#d3d3d3")
        image_label.pack(expand=True)
        image_label.bind("<Button-1>", self.show_full_image)

        self.is_answer_shown = False
        self.action_button.config(text="完成")

    def show_answer(self):
        entry = self.quiz_data[self.current_index]

        for widget in self.card_frame.winfo_children():
            widget.destroy()

        answer_label = tk.Label(self.card_frame, text=entry["answer"], font=("Helvetica", 14), wraplength=380, bg="#f7f7f7")
        answer_label.pack(expand=True)
        self.is_answer_shown = True
        self.action_button.config(text="下一题")

    def flip_card(self):
        if self.is_answer_shown:
            self.next_question()
        else:
            self.show_answer()

    def next_question(self):
        if self.current_index < len(self.quiz_data) - 1:
            self.current_index += 1
            self.update_progress()
            self.show_question()
        else:
            self.end_quiz()

    def end_quiz(self):
        for widget in self.card_frame.winfo_children():
            widget.destroy()
        self.progress_label.config(text="自测完成！")
        self.action_button.config(text="返回主页", command=self.master.show_main_page)

app = App()
app.mainloop()
