import base64


class PasswordManager:
    def __init__(self, key="EnVoitureSimone2025"):
        self.key = key

    def encrypt(self, text):
        """chiffre le texte pour le stocker de manière sécurisée"""
        xored = "".join(
            chr(ord(c) ^ ord(self.key[i % len(self.key)])) for i, c in enumerate(text)
        )
        return base64.b64encode(xored.encode()).decode()

    def decrypt(self, encrypted_text):
        """Déchiffre le texte"""
        try:
            xored = base64.b64decode(encrypted_text.encode()).decode()
            return "".join(
                chr(ord(c) ^ ord(self.key[i % len(self.key)]))
                for i, c in enumerate(xored)
            )
        except:
            return encrypted_text
