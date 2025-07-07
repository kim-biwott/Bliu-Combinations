from rich.console import Console
from rich.prompt import Prompt
from models import create_session
from menus.subject_menu import SubjectMenu
from display import display_title
import os

console = Console()

def main():
    #display_title()
    console.print("=" * 50)
    
    if not os.path.exists("combinations.db"):
        console.print("Database not found. Would you like to seed it now?", style="bold yellow")
        if Prompt.ask("Run database seed? (y/n)", choices=["y", "n"]) == "y":
            from seed import seed_database
            seed_database("subject-combinations-senior-schools.xlsx")
        else:
            console.print("Exiting application. Database required to proceed.", style="bold red")
            return
    
    session = create_session()
    try:
        SubjectMenu(session).run()
    except Exception as e:
        console.print(f"An error occurred: {str(e)}", style="bold red")
    finally:
        session.close()

if __name__ == "__main__":
    main()