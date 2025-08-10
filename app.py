from flask import Flask, render_template, request
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

def parse_mock_html():
    with open('templates/mock_case.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    h3 = soup.find('h3')
    def find_p(label):
        p = soup.find('p', string=lambda t: t and label in t)
        return p.text.replace(label, '').strip() if p else "N/A"

    order = soup.find('a', href=True)
    return {
        "status": h3.text.replace("Case Status:", "").strip() if h3 else "N/A",
        "parties": find_p("Parties:"),
        "filing_date": find_p("Filing Date:"),
        "next_hearing": find_p("Next Hearing:"),
        "order_link": order['href'] if order else "#"
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    case_details = None

    if request.method == 'POST':
        case_type = request.form.get('case_type', '').strip()
        case_number = request.form.get('case_number', '').strip()
        filing_year = request.form.get('filing_year', '').strip()

        # generate Python timestamp (string)
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save to DB (explicitly include timestamp)
        conn = sqlite3.connect('search_history.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO searches (case_type, case_number, filing_year, timestamp) VALUES (?, ?, ?, ?)",
            (case_type, case_number, filing_year, ts)
        )
        conn.commit()
        conn.close()

        # parse mock HTML to show details
        case_details = parse_mock_html()

    return render_template('index.html', case_details=case_details)

@app.route('/history')
def history():
    conn = sqlite3.connect('search_history.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT case_type, case_number, filing_year, timestamp FROM searches ORDER BY rowid DESC")
    rows = cursor.fetchall()
    conn.close()
    return render_template('history.html', history=rows)

if __name__ == '__main__':
    app.run(debug=True)



    
