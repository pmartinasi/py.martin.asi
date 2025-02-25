import requests
from bs4 import BeautifulSoup
import mysql.connector

# Configuración de la base de datos MySQL
db_params = {
    'host': 'tu_host',
    'database': 'tu_base_de_datos',
    'user': 'tu_usuario',
    'password': 'tu_contraseña'
}

# Crear la tabla 'enlaces' si no existe
create_table_query = '''
    CREATE TABLE IF NOT EXISTS enlaces (
        id INT AUTO_INCREMENT PRIMARY KEY,
        url VARCHAR(255)
    );
'''

def create_table(conn):
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
    conn.commit()

def insert_link(conn, url):
    insert_query = 'INSERT INTO enlaces (url) VALUES (%s);'
    with conn.cursor() as cursor:
        cursor.execute(insert_query, (url,))
    conn.commit()

def web_crawler(url, conn):
    linkshref = []
    try:
        # Hacer la solicitud HTTP
        response = requests.get(url)
        
        # Verificar si la solicitud fue exitosa (código 200)
        if response.status_code == 200:
            # Analizar el contenido HTML de la página
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Aquí puedes realizar operaciones con el contenido HTML
            # Por ejemplo, imprimir todos los enlaces de la página
            for link in soup.find_all('a'):
                l = str(link.get('href'))
                print(link.get('href'))
                if(l.lower().startswith("http://") or l.lower().startswith("https://")):
                    linkshref.append(l)
                    insert_link(conn, l)
        else:
            print(f"Error al hacer la solicitud. Código de estado: {response.status_code}")

    except Exception as e:
        print(f"Error: {e}")
    return linkshref


def web_crawler_r(url, conn):
    linkshref = web_crawler(url, conn)
    for sublink in linkshref:
        print(sublink)
        web_crawler_r(sublink, conn)

# Ejemplo de uso
url_a_crawlear = "https://pmartinasi.es"

# Conectar a la base de datos
conn = mysql.connector.connect(**db_params)

# Crear la tabla si no existe
create_table(conn)

# Realizar el crawling y guardar en la base de datos
sublinks = web_crawler_r(url_a_crawlear, conn)

# Cerrar la conexión a la base de datos
conn.close()
