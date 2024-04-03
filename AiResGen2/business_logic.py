import threading
import asyncio
import tkinter

class ResumeGeneratorApp:
    def __init__(self):
        self.pdf_file_path = None

class ResumeGeneratorController:
    def __init__(self, gui):
        self.gui = gui

    def async_generate_resume(self):
        threading.Thread(target=self._generate_resume, daemon=True).start()

  
    def _generate_resume(self):
        self.gui.update_status("Generating resume...")
        job_url = self.gui.job_url_entry.get()

        if job_url:
            job_description = asyncio.run(self._fetch_job_description(job_url))
        else:
            job_description = self.gui.job_desc_entry.get("1.0", tkinter.END).strip()

        if not job_description:
            self.gui.show_error("Error", "No job description provided.")
            self.gui.update_status("Idle")
            return

        if not self.gui.pdf_file_path:
            self.gui.show_error("Error", "No PDF file selected.")
            self.gui.update_status("Idle")
            return

      
   