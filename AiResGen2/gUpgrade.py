import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from business_logic import ResumeGeneratorController

class ResumeGeneratorApp:
    def __init__(self, master):
        self.controller = ResumeGeneratorController(self)
        self.master = master
        self._setup_ui()

    def _setup_ui(self):
        self._create_job_url_entry()
        self._create_job_description_entry()
        self._create_pdf_selection_button()
        self._create_generate_resume_button()
        self._create_status_label()
        self._create_resume_display()
        self._create_progress_bar()

    def _create_job_url_entry(self):
        tk.Label(self.master, text="Enter Job Description URL:").pack()
        self.job_url_entry = tk.Entry(self.master)
        self.job_url_entry.pack()

    def _create_job_description_entry(self):
        tk.Label(self.master, text="Or paste the job description here:").pack()
        self.job_desc_entry = scrolledtext.ScrolledText(self.master, height=10, width=100)
        self.job_desc_entry.pack()

    def _create_pdf_selection_button(self):
        self.select_pdf_button = tk.Button(self.master, text="Select PDF File", command=self._select_pdf)
        self.select_pdf_button.pack()

    def _create_generate_resume_button(self):
        self.generate_button = tk.Button(self.master, text="Generate Resume", command=self.controller.async_generate_resume)
        self.generate_button.pack()

    def _create_status_label(self):
        self.status_var = tk.StringVar(self.master)
        tk.Label(self.master, textvariable=self.status_var).pack()

    def _create_resume_display(self):
        self.resume_display = scrolledtext.ScrolledText(self.master, height=15, width=100)
        self.resume_display.pack()

    def _create_progress_bar(self):
        self.canvas = tk.Canvas(self.master, width=400, height=20)
        self.canvas.pack()
        self.progress_bar = self.canvas.create_rectangle(0, 0, 0, 20, fill="blue")

    def _select_pdf(self):
        self.pdf_file_path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
        if self.pdf_file_path:
            self.update_status(f"Selected PDF file: {self.pdf_file_path}")

    def update_status(self, message):
        self.status_var.set(message)
        self.master.update_idletasks()

    def update_progress(self, value):
        self.canvas.coords(self.progress_bar, 0, 0, 400 * value / 100, 20)
        self.master.update_idletasks()

    def display_generated_resume(self, resume):
        self.resume_display.delete('1.0', tk.END)
        self.resume_display.insert(tk.END, resume)

    def show_error(self, title, message):
        messagebox.showerror(title, message)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Resume Generator")
    app = ResumeGeneratorApp(root)
    root.mainloop()
