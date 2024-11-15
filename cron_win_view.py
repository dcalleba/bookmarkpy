import win32com.client
import datetime

class WindowsTaskViewer:
    """Classe pour visualiser les tâches planifiées Windows"""
    
    def __init__(self):
        """Initialise la connexion au planificateur de tâches"""
        self.scheduler = win32com.client.Dispatch('Schedule.Service')
        self.scheduler.Connect()
        self.root_folder = self.scheduler.GetFolder("\\")

    def list_all_tasks(self):
        """Liste toutes les tâches planifiées avec leurs détails"""
        tasks = []
        try:
            tasks_collection = self.root_folder.GetTasks(0)
            
            for task in tasks_collection:
                # Récupère les informations de base
                task_info = {
                    'nom': task.Name,
                    'état': 'Activé' if task.Enabled else 'Désactivé',
                    'dernière_execution': task.LastRunTime,
                    'prochaine_execution': task.NextRunTime,
                    'statut': self._get_task_status(task.State)
                }
                tasks.append(task_info)
                
        except Exception as e:
            print(f"Erreur lors de la lecture des tâches: {str(e)}")
            
        return tasks

    def _get_task_status(self, state):
        """Convertit le code d'état en texte compréhensible"""
        states = {
            0: "Inconnu",
            1: "Désactivé",
            2: "En file d'attente",
            3: "Prêt",
            4: "En cours"
        }
        return states.get(state, "État inconnu")

    def display_tasks(self):
        """Affiche les tâches de manière formatée"""
        tasks = self.list_all_tasks()
        
        if not tasks:
            print("Aucune tâche planifiée trouvée")
            return
            
        print("\nListe des tâches planifiées :")
        print("-" * 80)
        
        for task in tasks:
            print(f"Nom: {task['nom']}")
            print(f"État: {task['état']}")
            print(f"Dernière exécution: {task['dernière_execution']}")
            print(f"Prochaine exécution: {task['prochaine_execution']}")
            print(f"Statut: {task['statut']}")
            print("-" * 80)

if __name__ == "__main__":
    try:
        viewer = WindowsTaskViewer()
        viewer.display_tasks()
    except Exception as e:
        print(f"Erreur lors de l'initialisation: {str(e)}")