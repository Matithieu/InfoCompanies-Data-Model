import subprocess

# Liste des chemins vers vos scripts Python et le chemin vers le programme C
scripts = [
    "Chiffres-Cles/sortNumbers.py",
    "Entreprises-crées/addNewCompanies.py",
    "Entreprises-crées/sortCompanies.py",
    "Entreprises-Radiées/newRadiatedCompanies.py",
    "Entreprises-Radiées/sortRadiated.py",
    "Fichiers_FIN/finalSort.py",
    "Fichiers_FIN/rename.py",
    "Fichiers_FIN/renameColumnsFinal.py",
    #"Fichiers_FIN/merging.py",
    #"Fichiers_FIN/main",
]

# Boucle pour exécuter chaque script
for script_path in scripts:
    try:
        if script_path.endswith(".py"):
            process = subprocess.Popen(["python3", script_path])
        else:
            process = subprocess.Popen([script_path])
        process.wait()  # Attend que le processus se termine
        print(f"Le script {script_path} a été exécuté avec succès !")
    except Exception as e:
        print(
            f"Une erreur s'est produite lors de l'exécution du script {script_path}: {str(e)}"
        )

print("Tous les scripts ont été exécutés.")
