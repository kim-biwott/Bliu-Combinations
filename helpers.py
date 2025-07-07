import re

def validate_input(input_str, min_length=2):
    """Basic input validation"""
    return len(input_str.strip()) >= min_length

def parse_subjects(subject_str):
    """Parse comma-separated subjects into a list"""
    return [s.strip() for s in subject_str.split(",") if s.strip()]

def format_subjects(subjects):
    """Format subjects list into a readable string"""
    if not subjects:
        return ""
    if len(subjects) == 1:
        return subjects[0]
    return ", ".join(subjects[:-1]) + " and " + subjects[-1]