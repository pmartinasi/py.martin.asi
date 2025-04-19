import os
import argparse
from pyhanko.sign import signers, fields
from pyhanko.sign.validation import validate_pdf_signature_field
from cryptography.x509 import load_pem_x509_certificate
from pyhanko.sign.certvalidation import validate_signature
from pyhanko.sign.signers import SimpleSigner
from pyhanko.sign.fields import SigFieldSpec
from pyhanko.sign.validation import ValidationError

def verify_pdf_signature(pdf_path):
    """
    Verifica la firma digital en un archivo PDF, incluyendo la validez del certificado y la cadena de confianza.
    :param pdf_path: Ruta al archivo PDF.
    """
    # Intentamos validar la firma del PDF usando PyHanko
    try:
        # Realizar la validación de la firma en el archivo PDF
        validation_result = validate_pdf_signature_field(pdf_path)

        # Si la validación pasa, mostramos detalles de la firma
        if validation_result.is_valid:
            print("Firma digital válida.")
            print(f"Detalles de la firma:\n{validation_result.signature_details}")
        else:
            print("Firma no válida.")
        
        # Verificar la cadena de confianza del certificado asociado a la firma
        for signature in validation_result.signatures:
            cert = signature.cert  # El certificado asociado con la firma
            # Validamos el certificado (esto verificará la cadena de confianza)
            try:
                # Este método valida la cadena de confianza y la fecha de validez del certificado
                validate_signature(cert)
                print("Cadena de confianza del certificado válida.")
            except Exception as e:
                print(f"Error en la cadena de confianza del certificado: {e}")
                return False

    except ValidationError as e:
        print(f"Error al validar la firma del PDF: {e}")
        return False

    return True


def extract_signed_content(pdf_path):
    """
    Extrae el contenido firmado de un archivo PDF.
    :param pdf_path: Ruta al archivo PDF.
    :return: Contenido firmado como bytes (puede ser el contenido que fue firmado).
    """
    # Aquí utilizaríamos PyHanko para extraer el contenido firmado.
    # Este contenido es esencial para realizar una verificación adecuada de la firma.
    try:
        with open(pdf_path, "rb") as f:
            # Extraemos las firmas del archivo PDF
            signed_content = signers.extract_signed_data(f)
            return signed_content
    except Exception as e:
        print(f"Error al extraer el contenido firmado: {e}")
        return None


def main(pdf_path):
    # Verificar la firma digital del archivo PDF
    is_valid = verify_pdf_signature(pdf_path)

    # Si la firma es válida, extraemos y mostramos el contenido firmado
    if is_valid:
        signed_content = extract_signed_content(pdf_path)
        if signed_content:
            print("Contenido firmado extraído correctamente.")
        else:
            print("No se pudo extraer el contenido firmado.")
    else:
        print("La firma digital no es válida.")


if __name__ == "__main__":
    # Configuración de argparse para aceptar parámetros desde la línea de comandos
    parser = argparse.ArgumentParser(description="Verificar la firma digital de un archivo PDF.")
    parser.add_argument("pdf_path", help="Ruta al archivo PDF que contiene la firma digital.")
    args = parser.parse_args()
    
    # Llamada a la función principal con el parámetro pasado por consola
    main(args.pdf_path)
