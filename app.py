
import os
import pandas as pd
from flask import Flask, render_template, send_file, request
from datetime import datetime

app = Flask(__name__)

DATA_DIR = 'data'

@app.route('/')
def home():
    return "Bot is running. Visit /dashboard to view stats."

@app.route('/dashboard')
def dashboard():
    all_data = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(DATA_DIR, file))
            all_data.append(df)

    if not all_data:
        return "📂 No data available."

    df_all = pd.concat(all_data)
    df_all['timestamp'] = pd.to_datetime(df_all['timestamp'])

    start_date = request.args.get('start')
    end_date = request.args.get('end')
    if start_date and end_date:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        df_all = df_all[(df_all['timestamp'] >= start) & (df_all['timestamp'] <= end)]

    chart_data = df_all['message_type'].value_counts().to_dict()
    return render_template("dashboard.html", stats=chart_data)

@app.route('/export')
def export():
    all_data = []
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(DATA_DIR, file))
            all_data.append(df)
    if not all_data:
        return "No data to export"

    df = pd.concat(all_data)
    output_path = os.path.join(DATA_DIR, "export.xlsx")
    df.to_excel(output_path, index=False)
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
