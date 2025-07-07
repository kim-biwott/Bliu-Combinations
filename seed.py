import pandas as pd
from sqlalchemy.exc import IntegrityError
from models import SubjectCombination, create_session, Base, engine
from rich.progress import track
from rich.console import Console

console = Console()

def reset_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    console.print("Database tables recreated", style="bold green")

def seed_database(file_path):
    reset_database()
    session = create_session()

    try:
        df = pd.read_excel('./subject-combinations-senior-schools.xlsx')
        console.print(f"Loaded {len(df)} records from spreadsheet", style="bold green")
        
    
        df = df.rename(columns={
            "S/No.": "id",
            "PATHWAY": "pathway",
            "TRACK": "track",
            "SUBJECTS": "subjects"
        })
        
        records = df.to_dict(orient='records')
        
        for record in track(records, description="Seeding database..."):
            if str(record.get('pathway')).upper() == 'PATHWAY':
                continue
                
            session.add(SubjectCombination(
                pathway=record['pathway'],
                track=record['track'],
                subjects=record['subjects']
            ))
        
        session.commit()
        console.print(f"Inserted {len(records)} combinations into database", style="bold green")
        
        count = session.query(SubjectCombination).count()
        console.print(f"Database now contains {count} combinations", style="bold green")
        
    except Exception as e:
        session.rollback()
        console.print(f"Seeding failed: {str(e)}", style="bold red")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    seed_database("subject-combinations-senior-schools.xlsx")