import os

def combine_scripts_to_file(script_names, output_file):
    with open(output_file, 'w') as outfile:
        for filename in script_names:
            try:
                with open(filename, 'r') as infile:
                    content = infile.read()
                    # Schreibe den Dateinamen als Kommentar
                    outfile.write(f"# {filename}:\n")
                    # Prüfe, ob die Datei leer ist
                    if content.strip():  # Inhalt ist nicht leer
                        outfile.write(content)
                    else:  # Datei ist leer
                        outfile.write("--- File ist leer ---")
                    # Füge eine neue Zeile nach jedem Skript hinzu
                    outfile.write("\n\n")
            except FileNotFoundError:
                print(f"Die Datei {filename} wurde nicht gefunden.")

# Beispielhafte Verwendung
current_script = os.path.basename(__file__)
script_directory = os.path.dirname(os.path.abspath(__file__))
py_files = [f for f in os.listdir(script_directory) if f.endswith('.py') and f != current_script]

# Speicherpfad für die Ausgabe
output_file_path = os.path.join(script_directory, 'combined_scripte.txt')

combine_scripts_to_file(py_files, output_file_path)
