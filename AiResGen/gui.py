import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from business_logic import ResumeGeneratorController

class ResumeGeneratorApp:
    def __init__(self, master):
        self.controller = ResumeGeneratorController(self)
        self.master = master
        master.title("Resume Generator")
        self.setup_ui()

    def setup_ui(self):
        self.label1 = tk.Label(self.master, text="Enter Job Description URL:")
        self.label1.pack()

        self.job_url_entry = tk.Entry(self.master)
        self.job_url_entry.pack()

        tk.Label(self.master, text="Or paste the job description here:").pack()
        self.job_desc_entry = scrolledtext.ScrolledText(self.master, height=10, width=100)
        self.job_desc_entry.pack()

        self.select_pdf_button = tk.Button(self.master, text="Select PDF File", command=self.select_pdf)
        self.select_pdf_button.pack()

        self.generate_button = tk.Button(self.master, text="Generate Resume", command=self.controller.async_generate_resume)
        self.generate_button.pack()

        self.status_var = tk.StringVar(self.master)
        tk.Label(self.master, textvariable=self.status_var).pack()

        self.resume_display = scrolledtext.ScrolledText(self.master, height=15, width=100)
        self.resume_display.pack()

        self.canvas = tk.Canvas(self.master, width=400, height=20)
        self.canvas.pack()
        self.progress_bar = self.canvas.create_rectangle(0, 0, 0, 20, fill="blue")

        self.pdf_file_path = None

    def select_pdf(self):
        self.pdf_file_path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if self.pdf_file_path:
            self.update_status(f"Selected PDF file: {self.pdf_file_path}")

    def update_status(self, message):
        self.status_var.set(message)
        self.master.update_idletasks()

    def update_progress(self, value):
        self.canvas.coords(self.progress_bar, 0, 0, 4 * value, 20)
        self.master.update_idletasks()

    def display_generated_resume(self, resume):
        self.resume_display.delete('1.0', tk.END)
        self.resume_display.insert(tk.END, resume)

    def show_error(self, title, message):
        messagebox.showerror(title, message)

if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeGeneratorApp(root)
    root.mainloop()
