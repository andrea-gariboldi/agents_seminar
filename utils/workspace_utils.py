from pathlib import Path

def cleanup_workspace(workspace_dir: str = "agents_workspace"):
	for item in Path(workspace_dir).iterdir():
		if item.is_dir() and item.name == "data":
			continue
		else:
			if item.is_dir():
				rmdir(item)
			else:
				item.unlink()

def rmdir(directory):
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()