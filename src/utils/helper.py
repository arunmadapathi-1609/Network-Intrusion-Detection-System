from pathlib import Path
import joblib


# ==========================================
# Create Directory
# ==========================================

def create_directory(path: str):
    """
    Create a directory if it does not exist.
    """

    Path(path).mkdir(parents=True, exist_ok=True)


# ==========================================
# Save Object
# ==========================================

def save_object(obj, filepath: str):
    """
    Save a Python object using joblib.
    """

    create_directory(Path(filepath).parent)

    joblib.dump(obj, filepath)


# ==========================================
# Load Object
# ==========================================

def load_object(filepath: str):
    """
    Load a saved Python object.
    """

    return joblib.load(filepath)


# ==========================================
# Print Section
# ==========================================

def print_section(title: str):
    """
    Print a formatted section title.
    """

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)