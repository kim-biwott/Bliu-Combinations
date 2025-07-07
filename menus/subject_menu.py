from .base_menu import BaseMenu
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.console import Console
from rich.table import Table
from models import SubjectCombination
from display import display_title
import re

console = Console()

class SubjectMenu(BaseMenu):
    def __init__(self, session):
        super().__init__(session)
        self.model = SubjectCombination
        self.entity_name = "Subject Combination"
        self.display_attrs = ["id", "pathway", "track", "subjects"]
    
    def _display_combinations(self, combinations):
        if not combinations:
            console.print("No combinations found", style="bold yellow")
            return
        
        table = Table(title=f"Found {len(combinations)} Combinations", show_header=True, header_style="bold green")
        table.add_column("ID", style="cyan")
        table.add_column("Pathway")
        table.add_column("Track")
        table.add_column("Subjects")
        
        for combo in combinations:
            table.add_row(
                str(combo.id),
                combo.pathway,
                combo.track,
                combo.subjects
            )
        console.print(table)
    
    def search_by_pathway(self):
        pathway = Prompt.ask("Enter pathway to search (e.g., STEM, ARTS)")
        results = SubjectCombination.find_by_pathway(self.session, pathway)
        self._display_combinations(results)
    
    def search_by_track(self):
        track = Prompt.ask("Enter track to search (e.g., PURE SCIENCES, LANGUAGES)")
        results = SubjectCombination.find_by_track(self.session, track)
        self._display_combinations(results)
    
    def search_by_subject(self):
        subject_input = Prompt.ask("Enter subjects to search (comma separated)")
        subjects = [s.strip() for s in subject_input.split(",") if s.strip()]
        if not subjects:
            console.print("No subjects provided", style="bold yellow")
            return
        
        results = SubjectCombination.find_combinations(
            self.session, 
            subjects=subjects
        )
        self._display_combinations(results)
    
    def search_by_pathway_and_track(self):
        pathway = Prompt.ask("Enter pathway")
        track = Prompt.ask("Enter track")
        results = SubjectCombination.find_combinations(
            self.session, 
            pathway=pathway,
            track=track
        )
        self._display_combinations(results)
    
    def search_by_pathway_and_subject(self):
        pathway = Prompt.ask("Enter pathway")
        subject_input = Prompt.ask("Enter subjects (comma separated)")
        subjects = [s.strip() for s in subject_input.split(",") if s.strip()]
        
        if not subjects:
            console.print("No subjects provided", style="bold yellow")
            return
        
        results = SubjectCombination.find_combinations(
            self.session, 
            pathway=pathway,
            subjects=subjects
        )
        self._display_combinations(results)
    
    def search_by_track_and_subject(self):
        track = Prompt.ask("Enter track")
        subject_input = Prompt.ask("Enter subjects (comma separated)")
        subjects = [s.strip() for s in subject_input.split(",") if s.strip()]
        
        if not subjects:
            console.print("No subjects provided", style="bold yellow")
            return
        
        results = SubjectCombination.find_combinations(
            self.session, 
            track=track,
            subjects=subjects
        )
        self._display_combinations(results)
    
    def search_by_all(self):
        pathway = Prompt.ask("Enter pathway (press Enter to skip)")
        track = Prompt.ask("Enter track (press Enter to skip)")
        subject_input = Prompt.ask("Enter subjects (comma separated, press Enter to skip)")
        
        subjects = [s.strip() for s in subject_input.split(",")] if subject_input.strip() else None
        
        results = SubjectCombination.find_combinations(
            self.session, 
            pathway=pathway if pathway.strip() else None,
            track=track if track.strip() else None,
            subjects=subjects
        )
        self._display_combinations(results)
    
    def view_details(self):
        combo = self._get_by_id()
        if combo:
            table = Table(title=f"Combination Details (ID: {combo.id})", show_header=False)
            table.add_column("Field", style="bold cyan")
            table.add_column("Value")
            
            table.add_row("ID", str(combo.id))
            table.add_row("Pathway", combo.pathway)
            table.add_row("Track", combo.track)
            table.add_row("Subjects", combo.subjects)
            
            console.print(table)
        else:
            console.print("Combination not found", style="bold red")
    
    def run(self):
        while True:
            display_title()
            console.print("\n[bold cyan]Subject Combination Explorer[/bold cyan]")
            console.print("1. List All Combinations")
            console.print("2. Search by Pathway")
            console.print("3. Search by Track")
            console.print("4. Search by Subject(s)")
            console.print("5. Search by Pathway and Track")
            console.print("6. Search by Pathway and Subject(s)")
            console.print("7. Search by Track and Subject(s)")
            console.print("8. Advanced Search (All Criteria)")
            console.print("9. View Combination Details by ID")
            console.print("10. Exit")
            
            choice = Prompt.ask("Choose an option", choices=[str(i) for i in range(1, 11)])
            
            if choice == "1":
                self.list_all()
            elif choice == "2":
                self.search_by_pathway()
            elif choice == "3":
                self.search_by_track()
            elif choice == "4":
                self.search_by_subject()
            elif choice == "5":
                self.search_by_pathway_and_track()
            elif choice == "6":
                self.search_by_pathway_and_subject()
            elif choice == "7":
                self.search_by_track_and_subject()
            elif choice == "8":
                self.search_by_all()
            elif choice == "9":
                self.view_details()
            elif choice == "10":
                console.print("Exiting Bliu Combinations, Goodbye  bliu :)", style="bold green")
                break