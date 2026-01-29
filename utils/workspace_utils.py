from pathlib import Path

def cleanup_workspace(workspace_dir: str = "agents_workspace"):
	print("Workspace dir", workspace_dir)
	for item in Path(workspace_dir).iterdir():
		if item.is_dir() and item.name == "data":
			continue
		else:
			item.unlink()