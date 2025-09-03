import pandas as pd
from sqlalchemy import create_engine, text

def run_etl():
    # ---------- CONFIGURACIÓN DE CONEXIÓN ----------
    user = 'user'
    password = 'user123'
    host = '127.0.0.1'
    port = '3306'
    database = 'pruebaNT'

    engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')

    # ---------- CARGA DEL CSV ----------
    df = pd.read_csv("data_prueba_tecnica.csv")

    # Limpiar columnas vacías y espacios en blanco
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.dropna(how='all', axis=1)

    # ---------- FILTRAR SOLO COMPAÑÍAS VÁLIDAS ----------
    valid_companies = ["Muebles chidos", "MiPasajefy"]
    df = df[df['name'].isin(valid_companies)]

    # ---------- TRANSFORMACIÓN ----------
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    df['paid_at'] = pd.to_datetime(df['paid_at'], errors='coerce')
    df['id'] = df['id'].astype(str)
    df['company_id'] = df['company_id'].astype(str)
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
    df['status'] = df['status'].astype(str)
    df['name'] = df['name'].astype(str)

    # ---------- CREACIÓN DE TABLAS ----------
    companies = df[['company_id', 'name']].drop_duplicates().rename(columns={'name': 'company_name'})
    companies.to_sql('companies', con=engine, if_exists='replace', index=False)
    # print("Tabla 'companies' cargada correctamente.") DEBUG

    charges = df[['id', 'company_id', 'amount', 'status', 'created_at', 'paid_at']]
    charges.to_sql('charges', con=engine, if_exists='replace', index=False)
    # print("Tabla 'charges' cargada correctamente.") DEBUG 

    # ---------- CREACIÓN DE VISTA ----------
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE OR REPLACE VIEW daily_totals AS
        SELECT 
            c.company_name,
            DATE(ch.created_at) AS day,
            SUM(ch.amount) AS total_amount
        FROM charges ch
        JOIN companies c ON ch.company_id = c.company_id
        GROUP BY c.company_name, DATE(ch.created_at);
        """))
        conn.commit()
    print("Vista 'daily_totals' creada correctamente.")
