import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

def read_csv(path):
    """Read CSV into pandas DataFrame"""
    return pd.read_csv(path)

def analyze(df):
    """Basic summary statistics for numeric columns"""
    numeric = df.select_dtypes(include='number')
    summary = {}
    for col in numeric.columns:
        summary[col] = {
            'count': int(df[col].count()),
            'mean': float(df[col].mean()),
            'sum': float(df[col].sum())
        }
    return summary

def make_plot(df, col, out_path):
    """Generate a bar chart and save as image"""
    plt.figure(figsize=(6, 3))
    df.plot(x='name', y=col, kind='bar', legend=False)
    plt.title(f'{col} by name')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def generate_pdf(title, df, summary, image_path, out_pdf):
    """Generate PDF report"""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- Cover Page ---
    pdf.add_page()
    pdf.set_font("helvetica", 'B', 18)
    pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(6)

    pdf.set_font("helvetica", size=12)
    pdf.cell(0, 8, f"Total rows: {len(df)}", new_x="LMARGIN", new_y="NEXT")

    # --- Summary Section ---
    pdf.ln(4)
    pdf.set_font("helvetica", 'B', 14)
    pdf.cell(0, 8, "Summary", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("helvetica", size=11)
    for col, stats in summary.items():
        text = f"{col}: count={stats['count']}  mean={stats['mean']:.2f}  sum={stats['sum']:.2f}"
        pdf.cell(0, 7, text, new_x="LMARGIN", new_y="NEXT")  # ✅ aligned neatly

    # --- Chart Page ---
    if os.path.exists(image_path):
        pdf.add_page()
        pdf.set_font("helvetica", 'B', 12)
        pdf.cell(0, 8, "Charts", new_x="LMARGIN", new_y="NEXT")
        pdf.image(image_path, x=15, y=30, w=180)

    # --- Save PDF ---
    pdf.output(out_pdf)
    print(f"✅ Saved PDF: {out_pdf}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate automated PDF report")
    parser.add_argument("input_csv", help="Path to input CSV file")
    parser.add_argument("output_pdf", help="Path to output PDF file")
    args = parser.parse_args()

    df = read_csv(args.input_csv)
    summary = analyze(df)

    # generate chart for first numeric column
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    chart_file = "temp_chart.png"
    if numeric_cols:
        make_plot(df, numeric_cols[0], chart_file)

    generate_pdf("Automated Report", df, summary, chart_file, args.output_pdf)
