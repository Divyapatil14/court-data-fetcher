from flask import Flask, render_template, request
import sqlite3
from bs4 import BeautifulSoup

app = Flask(__name__)

# ✅ Function to safely parse mock HTML
def parse_mock_html():
    with open('templates/mock_case.html', 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Safely find all elements
    h3_tag = soup.find("h3")
    parties_tag = soup.find("p", text=lambda t: t and "Parties:" in t)
    filing_date_tag = soup.find("p", text=lambda t: t and "Filing Date:" in t)
    next_hearing_tag = soup.find("p", text=lambda t: t and "Next Hearing:" in t)
    order_link_tag = soup.find("a", href=True)

    # Return details with checks for None
    return {
        "status": h3_tag.text.replace("Case Status:", "").strip() if h3_tag else "N/A",
        "parties": parties_tag.text.replace("Parties:", "").strip() if parties_tag else "N/A",
        "filing_date": filing_date_tag.text.replace("Filing Date:", "").strip() if filing_date_tag else "N/A",
        "next_hearing": next_hearing_tag.text.replace("Next Hearing:", "").strip() if next_hearing_tag else "N/A",
        "order_link": order_link_tag['href'] if order_link_tag else "#"
    }

# ✅ Main route for form and display
@app.route('/', methods=['GET', 'POST'])
@app.route('/history')
def view_history():
    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()
    c.execute("SELECT * FROM searches ORDER BY rowid DESC")
    rows = c.fetchall()
    conn.close()
    return render_template('history.html', searches=rows)

def index():
    case_details = None

    if request.method == 'POST':
        case_type = request.form['case_type']
        case_number = request.form['case_number']
        filing_year = request.form['filing_year']

        # ✅ Save to SQLite
        conn = sqlite3.connect('search_history.db')
        c = conn.cursor()
        c.execute("INSERT INTO searches (case_type, case_number, filing_year) VALUES (?, ?, ?)",
                  (case_type, case_number, filing_year))
        conn.commit()
        conn.close()

        # ✅ Parse mock case data
        case_details = parse_mock_html()

    return render_template('index.html', case_details=case_details)

@app.route('/history')
def history():
    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()
    c.execute("SELECT case_type, case_number, filing_year, timestamp FROM searches ORDER BY rowid DESC")
    history_data = c.fetchall()
    conn.close()

    return render_template('history.html', history=history_data)

# ✅ Run app
if __name__ == '__main__':
    app.run(debug=True)

    
