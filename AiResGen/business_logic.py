import tkinter as tk
import threading
from data_handling import scrape_job_description, extract_pdf_text, extract_key_terms, generate_resume_with_openai, improve_resume

class ResumeGeneratorController:
    def __init__(self, gui):
        self.gui = gui

    def async_generate_resume(self):
        threading.Thread(target=self.generate_resume, daemon=True).start()

    def generate_resume(self):
        self.gui.update_status("Generating resume...")
        job_description = self.get_job_description()

        if not job_description:
            self.gui.show_error("Error", "No job description provided.")
            self.gui.update_status("")
            return

        key_terms = extract_key_terms(job_description)
        pdf_text = extract_pdf_text(self.gui.pdf_file_path) if self.gui.pdf_file_path else ""
        existing_resume = self.gui.resume_display.get("1.0", tk.END).strip()

        generated_resume = generate_resume_with_openai(job_description, key_terms, pdf_text, existing_resume)
        improved_resume = improve_resume(generated_resume, job_description, key_terms)

        self.gui.master.after(0, lambda: self.gui.display_generated_resume(improved_resume))
        self.gui.update_status("Resume displayed")
        self.gui.update_progress(100)

    def get_job_description(self):
        job_url = self.gui.job_url_entry.get()
        if job_url:
            return scrape_job_description(job_url)
        else:
            return self.gui.job_desc_entry.get("1.0", tk.END).strip()
