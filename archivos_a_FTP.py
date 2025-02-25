import os
from ftplib import FTP

def subir_archivo_ftp(ftp, archivo_local, directorio_remoto):
    with open(archivo_local, 'rb') as f:
        ftp.storbinary('STOR ' + os.path.join(directorio_remoto, os.path.basename(archivo_local)), f)

def buscar_y_subir_archivos_ftp(directorio_local, extension, servidor_ftp, usuario_ftp, contraseña_ftp, directorio_remoto):
    # Conexión al servidor FTP
    ftp = FTP(servidor_ftp)
    ftp.login(usuario_ftp, contraseña_ftp)

    # Recorre el directorio y subdirectorios
    for directorio_actual, _, archivos in os.walk(directorio_local):
        for archivo in archivos:
            if archivo.endswith(extension):
                archivo_local = os.path.join(directorio_actual, archivo)
                subir_archivo_ftp(ftp, archivo_local, directorio_remoto)

    # Cierra la conexión FTP
    ftp.quit()

if __name__ == "__main__":
    # Parámetros de conexión FTP
    servidor_ftp = 'ftp.ejemplo.com'
    usuario_ftp = 'tu_usuario_ftp'
    contraseña_ftp = 'tu_contraseña_ftp'

    # Parámetros del directorio local y extensión de archivo
    directorio_local = '/ruta/del/directorio/local'
    extension_archivo = '.txt'  # Cambia a la extensión que estás buscando

    # Directorio remoto en el servidor FTP
    directorio_remoto = '/ruta/del/directorio/remoto'

    # Llama a la función para buscar y subir archivos al servidor FTP
    buscar_y_subir_archivos_ftp(directorio_local, extension_archivo, servidor_ftp, usuario_ftp, contraseña_ftp, directorio_remoto)
