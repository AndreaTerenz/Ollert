# Ollert

Web App kanban realizzata come progetto universitario.
Una volta clonata la repository, prima di essere avviata è necessario eseguire, dalla root directory:
```
pipenv install                      # installa i pacchetti necessari all'esecuzione
pipenv shell                        # avvia l'ambiente virtuale
python manage.py makemigrations     # .
python manage.py migrate            # inizializzano il database
```
Successivamente, ogni volta viene avviata con
```
python manage.py runserver
```