# server/utils.py

import coincurve
from coincurve import PublicKey

def load_public_key(public_key_hex):
    """
    Carga una clave pública desde una cadena hexadecimal.
    """
    return PublicKey(bytes.fromhex(public_key_hex))

def verify_response(public_key, challenge, signature_hex):
    """
    Verifica la firma Schnorr de la respuesta del cliente.
    """
    message = str(challenge).encode()
    signature = bytes.fromhex(signature_hex)
    try:
        return public_key.schnorr_verify(message, signature)
    except Exception as e:
        print(f"Error al verificar la firma: {e}")
        return False
