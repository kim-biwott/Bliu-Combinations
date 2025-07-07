import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme

custom_theme = Theme({
    "title": "bold #00AAFF",
    "subtitle": "bold #FFAA00",
    "border": "#00FFAA",
    "highlight": "bold #FF00AA"
})
console = Console(theme=custom_theme)

def display_title():
    try: 
        width = console.width      
        font = "block" if width >= 80 else "slant" if width >= 60 else "small"
        ascii_art = pyfiglet.figlet_format("SUBJECT COMBINATIONS", font=font, width=width)   
        main_panel = Panel.fit(
            Text(ascii_art, style="title"),
            title=Text("Bliu Combinations", style="subtitle"),
            subtitle=Text("", style="#AAAAAA"),
            border_style="border",
            padding=(1, 2)
        )
        console.print(main_panel, justify="center")
        console.rule(style="highlight")      
    except Exception:
        console.print("\n[bold blue]SUBJECT COMBINATIONS[/bold blue]", justify="center")
        console.print("[bold yellow]Pathway filtering system[/yellow]\n", justify="center")