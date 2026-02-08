from fpdf import FPDF
import pandas as pd

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'DataNudge - Analysis Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

class ReportGenerator:
    def __init__(self, df):
        self.df = df
        
    def generate_report(self, output_path="report.pdf"):
        pdf = PDFReport()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # 1. Dataset Info
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "1. Dataset Overview", 0, 1)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Total Rows: {self.df.shape[0]}", 0, 1)
        pdf.cell(0, 10, f"Total Columns: {self.df.shape[1]}", 0, 1)
        pdf.ln(5)
        
        # 2. Columns
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "2. Column List", 0, 1)
        pdf.set_font("Arial", size=10)
        cols = ", ".join(self.df.columns.tolist())
        pdf.multi_cell(0, 10, cols)
        pdf.ln(5)
        
        # 3. Missing Values
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "3. Missing Values Summary", 0, 1)
        pdf.set_font("Arial", size=10)
        missing = self.df.isnull().sum()
        missing = missing[missing > 0]
        if not missing.empty:
            for col, val in missing.items():
                pdf.cell(0, 10, f"{col}: {val} missing", 0, 1)
        else:
             pdf.cell(0, 10, "No missing values found.", 0, 1)
        pdf.ln(10)

        # 4. Basic Stats (Numerical)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "4. Basic Statistics (Numerical)", 0, 1)
        pdf.set_font("Arial", size=8)
        
        desc = self.df.describe()
        # Convert df to string for simple printing
        # A real table would be better but requires more complex FPDF logic
        stats_str = desc.to_string() 
        pdf.multi_cell(0, 5, stats_str)
        
        pdf.output(output_path)
        return output_path
