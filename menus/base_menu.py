from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.table import Table
from sqlalchemy.exc import IntegrityError

console = Console()

class BaseMenu:
    def __init__(self, session):
        self.session = session
        self.model = None
        self.entity_name = ""
        self.display_attrs = []
    
    def display_table(self, items, title=None, columns=None):
        if not items:
            console.print(f"No {self.entity_name}s found", style="bold yellow")
            return
        
        table = Table(title=title or f"{self.entity_name}s", show_header=True, header_style="bold blue")
        for attr in (columns or self.display_attrs):
            table.add_column(attr.replace('_', ' ').title(), overflow="fold")
        
        for item in items:
            row = []
            for attr in (columns or self.display_attrs):
                val = getattr(item, attr, None)
                row.append(str(val) if val is not None else "N/A")
            table.add_row(*row)
        console.print(table)
    
    def _get_by_id(self):
        entity_id = IntPrompt.ask(f"Enter {self.entity_name} ID")
        return self.session.get(self.model, entity_id)
    
    def list_all(self):
        items = self.session.query(self.model).all()
        self.display_table(items)
    
    def run(self):
        raise NotImplementedError("Subclasses must implement run method")