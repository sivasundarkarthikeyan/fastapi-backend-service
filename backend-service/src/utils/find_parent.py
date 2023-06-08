from pathlib import Path

def get_project_root() -> Path:
    """method used to find fourth level parent for a file

    Returns:
        Path: the fourth level parent's path of the file from 
                which this script is invoked
    """
    return str(Path(__file__).parent.parent.parent.parent)
