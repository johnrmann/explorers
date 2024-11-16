import os
import sys

def count_lines_in_file(file_path):
	try:
		with open(file_path, 'r', encoding='utf-8') as file:
			return sum(1 for _ in file)
	except Exception as e:
		print(f"Error reading {file_path}: {e}")
		return 0

def should_count(file):
	return file.endswith('.py') or file.endswith('.c') or file.endswith('.h')

def count_lines_in_directory(directory):
	total_lines = 0
	for root, _, files in os.walk(directory):
		for file in files:
			if should_count(file):
				file_path = os.path.join(root, file)
				total_lines += count_lines_in_file(file_path)
	return total_lines

def collect_line_counts(directory, prefix=""):
	line_counts = []
	total_lines = 0

	# Iterate through the items in the directory
	for item in sorted(os.listdir(directory)):
		item_path = os.path.join(directory, item)
		if os.path.isdir(item_path):
			if item_path.endswith('__pycache__'):
				continue
			if '.git' in item_path:
				continue
			if 'assets' in item_path or '.vscode' in item_path:
				continue
			# Recurse into subdirectory
			sub_lines = count_lines_in_directory(item_path)
			line_counts.append((f"{prefix}{item}", sub_lines))
			total_lines += sub_lines
			# Recursively collect counts for subdirectories
			sub_line_counts = collect_line_counts(item_path, prefix=f"{prefix}{item}/")
			line_counts.extend(sub_line_counts)
		elif item.endswith('.py'):
			total_lines += count_lines_in_file(item_path)

	if prefix == "":
		line_counts.insert(0, ("(root)", total_lines))

	return line_counts

def print_line_counts(line_counts):
	line_len = 50
	for path, count in line_counts:
		space = '.' * (line_len - (len(path) + len(str(count))))
		print(f"{path}{space}{count}")

if __name__ == "__main__":
	# Get directory from command line arguments or default to current directory
	root_directory = sys.argv[1] if len(sys.argv) > 1 else "."
	if not os.path.isdir(root_directory):
		print(f"Error: '{root_directory}' is not a valid directory.")
		sys.exit(1)

	line_counts = collect_line_counts(root_directory)
	print_line_counts(line_counts)
