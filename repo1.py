from git import Repo
import os

def git_push(repo_path, commit_message):
    try:
        # Initialiser le repo
        repo = Repo(repo_path)
        
        # Vérifier s'il y a des changements
        if not repo.is_dirty(untracked_files=True):
            print("Aucun changement à commiter.")
            return
        
        # Ajouter tous les fichiers modifiés
        repo.git.add(all=True)
        
        # Commiter les changements
        repo.index.commit(commit_message)
        
        # Obtenir la branche actuelle
        branch = repo.active_branch
        
        # Push vers le remote "origin"
        origin = repo.remote(name='origin')
        origin.push(branch)
        
        print(f"Push réussi vers {branch} sur GitHub.")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")

# Utilisation
repo_path = "/users/danielcallebaut/bookmarkpy"
commit_message = "Mise à jour automatique"

git_push(repo_path, commit_message)