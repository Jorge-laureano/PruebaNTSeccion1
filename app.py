# app.py
from flask import Flask, render_template_string, request
import pandas as pd
from sqlalchemy import create_engine, text
import etl  # Tu script ETL actualizado

app = Flask(__name__)

# ---------- CONFIGURACIÓN DE CONEXIÓN ----------
user = 'user'
password = 'user123'
host = '127.0.0.1'
port = '3306'
database = 'pruebaNT'

engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

@app.route('/')
def index():
    # Parámetros de paginación y orden
    page = int(request.args.get('page', 1))
    per_page = 20
    sort_by = request.args.get('sort_by', 'day')
    sort_order = request.args.get('sort_order', 'asc')

    # Leer datos de la vista daily_totals
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM daily_totals", conn)

    # Ordenar
    if sort_by in df.columns:
        df = df.sort_values(by=sort_by, ascending=(sort_order=='asc'))

    # Paginación
    total_pages = (len(df) - 1) // per_page + 1
    start = (page - 1) * per_page
    end = start + per_page
    df_page = df.iloc[start:end]

    # HTML
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Daily Totals</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { 
                background-color: #3399ff; /* azul claro clicable */
                color: #ffffff; 
                cursor: pointer; 
                user-select: none;
                position: relative;
            }
            th span.arrow { margin-left: 5px; font-size: 0.8em; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            .pagination { margin-top: 20px; }
            .pagination a { margin: 0 5px; text-decoration: none; padding: 5px 10px; border: 1px solid #3399ff; color: #3399ff; }
            .pagination a.active { background-color: #3399ff; color: white; }
        </style>
    </head>
    <body>
        <h2>Daily Totals</h2>
        <table>
            <tr>
            {% for col in df_page.columns %}
                <th onclick="window.location='/?sort_by={{ col }}&sort_order={{ 'desc' if sort_by==col and sort_order=='asc' else 'asc' }}'">
                    {{ col }}
                    {% if sort_by == col %}
                        <span class="arrow">{{ '▲' if sort_order=='asc' else '▼' }}</span>
                    {% else %}
                        <span class="arrow">↕</span>
                    {% endif %}
                </th>
            {% endfor %}
            </tr>
            {% for row in df_page.itertuples() %}
            <tr>
                {% for value in row[1:] %}
                    <td>{{ value }}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </table>
        <div class="pagination">
        {% for p in range(1, total_pages + 1) %}
            <a href="/?page={{ p }}&sort_by={{ sort_by }}&sort_order={{ sort_order }}" class="{{ 'active' if p==page else '' }}">{{ p }}</a>
        {% endfor %}
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, df_page=df_page, page=page, total_pages=total_pages,
                                  sort_by=sort_by, sort_order=sort_order)

if __name__ == '__main__':
    print("Ejecutando ETL antes de iniciar la app...")
    etl.run_etl()  # Asegúrate que tu etl.py tenga esta función
    print("ETL completado, iniciando la app Flask...")
    app.run(debug=True)
