import os

def cleanup_workspace():
	for file in os.listdir("agents_workspace"):
		file_path = os.path.join("agents_workspace", file)
		try:
			if os.path.isfile and file_path == "agents_workspace/data/ecoli.csv":
				continue
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(f"Error deleting file {file_path}: {e}")

