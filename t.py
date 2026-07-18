import string
import random
import urllib.request
import json

def generate_nitro_code() -> str:
    """Génère un code Nitro valide (16 caractères, base32, format XXXX-XXXX-XXXX)."""
    chars = string.ascii_uppercase + string.digits
    code = ''.join(random.choices(chars, k=16))
    return f"{code[:4]}-{code[4:8]}-{code[8:]}"

def verify_nitro_code(code: str) -> tuple[bool, str]:
    """Vérifie la validité du code via l'API publique Discord."""
    while True:
        url = f"https://discord.com/api/v9/entitlements/gift-codes/{code}?with_application=true"
        try:
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                if response.status == 200 and data.get("type") in (1, 2):
                    return True, "Valide (Nitro)"
                elif response.status == 404:
                    return False, "Introuvable ou expiré"
                else:
                    return True, f"Validé - Type: {data.get('application', {}).get('name', 'Inconnu')}"
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return False, "Introuvable ou expiré"
            return False, f"Erreur API HTTP: {e.code}"
        except Exception as e:
            return False, f"Erreur de vérification: {e}"

if __name__ == "__main__":
    code = generate_nitro_code()
    print(f"Nouveau code généré : {code}")
    is_valid, message = verify_nitro_code(code)
    print(f"Statut : {'✅ ' if is_valid else '❌ '}{message}")