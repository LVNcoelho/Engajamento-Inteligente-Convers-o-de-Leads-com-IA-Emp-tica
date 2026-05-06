import sqlite3
from datetime import datetime

def criar_tabela():
    """Cria a tabela de leads se ela não existir."""
    conn = sqlite3.connect('leads_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_atendimento TEXT,
            nicho TEXT,
            dor_principal TEXT,
            comentario_original TEXT,
            insight_gerado TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_lead(nicho, dor, comentario, insight):
    """Salva os dados do atendimento no banco."""
    conn = sqlite3.connect('leads_database.db')
    cursor = conn.cursor()
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cursor.execute('''
        INSERT INTO leads (data_atendimento, nicho, dor_principal, comentario_original, insight_gerado)
        VALUES (?, ?, ?, ?, ?)
    ''', (data_atual, nicho, dor, comentario, insight))
    conn.commit()
    conn.close()

def buscar_leads():
    """Retorna todos os leads salvos."""
    conn = sqlite3.connect('leads_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM leads ORDER BY id DESC')
    dados = cursor.fetchall()
    conn.close()
    return dados

# Inicializa o banco ao rodar o script
if __name__ == "__main__":
    criar_tabela()
    print("✅ Banco de dados e tabela de leads prontos!")
