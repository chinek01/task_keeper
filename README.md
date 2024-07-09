# Task Keeper Project
<hr>
<br>

### Spis treści:
- [Opis projektu](#opis-projektu)
- [Instalacja](#instalacja)
- [Obsługa API](#obsługa-api)

## Opis projektu
<p>
Celem projektu było stworzenie aplikacji back-end w technologii Python, Django, Django Rest Framework i PostgresSQL do zarządzania zadaniami. 

Projekt zawiera dwa modele z następującymi polami: 
- Task

``` py
class Task(models.Model):
    STATUS = [
        (0, 'Nowy'),
        (1, "W toku"),
        (2, "Rozwiązany")
    ]

    task_name = models.CharField(max_length=124, blank=False, null=False)
    task_description = models.TextField(default='', blank=None, null=None)
    task_status = models.PositiveSmallIntegerField(choices=STATUS, default=0)
    task_user = models.ForeignKey(User, 
                                  on_delete=models.CASCADE, 
                                  blank=True, null=True)

    def __str__(self):
        return "{}".format(self.task_name)

```

- Log 

``` py 

class Log(models.Model):
    task_field_name = models.CharField(max_length=32, null=False, blank=False)
    prev_value = models.TextField(default='', null=True, blank=True)
    new_value = models.TextField(default='', null=True, blank=True)
    change_time = models.DateTimeField(auto_now_add=True)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE,
                                blank=False, null=False)
    
    def __str__(self) -> str:
        return "{} -> {}".format(self.task_id, self.task_field_name)


```

<br>
Poprzez wystawione końcówki (HTTP API Endpoints) aplikacja umożliwia: 
<ol>
<li>Dodawanie zadanie z wypełnionymi polami jak w modelu</li>
<li>Edycję już stworzonego zadania </li>
<li>Filtrowanie listy zadań po możliwych polach</li>
<li>Przedstawienie szczegółów pojedynczego zadania</li>
<li>Usuwanie zadania</li>
<li>Przedstawia historię zmian dokonywanych dla poszczególnych zadań </li>
</ol>

</p>

<p>

Projekt posiada system uwierzytelniania oraz uprawnień. Zwykły user (należący do grupy api_users) może dla modelu:

<ul>
<li>Task:
<ul>
<li>dodawać</li>
<li>zmieniać</li>
<li>przeglądać zadania</li>
<li>nie może usuwać</li>
</ul>
</li>
<li>Log:
<ul>
<li>przeglądać log</li>
<li>nie może zmieniać</li>
<li>nie może usuwać</li>
<li>nie może dodawać </li>
</ul>
</li>
</ul>
Wpisy w modelu Log są tworzone automatycznie w momencie zmiany jakiegoś pola w modelu Task.

</p>

<hr>

## Instalacja

<p>

#### Aby uruchomić projekt należy: 

##### Dla serwera lokalnego

<p>

<ol>
<li>Mieć komputer/serwer z zainstalowanym Python’em, którego można pobrać dla swojego systemu operacyjnego ze strony <a href="https://www.python.org/downloads/" target="_blank">Python.org</a></li>
<li>Założyć katalog i wgrać do niego pliki projektu</li>
<li>Mieć zainstalowany serwer baz danych  PostgresSQL oraz założyć bazę danych i użytkownika bazy danych. Do pliku konfiguracyjnego (.env) należy podać odpowiednie parametry takie jak np:  
<ul>
<li>DB_NAME=TaskKeeperDB</li>
<li>DB_USER=postgres</li>
<li>DB_PASSWORD=******</li>
<li>DB_HOST=localhost</li>
<li>DB_PORT=5433</li>
</ul>
</li>
<li>Zainstalować pakiety potrzebne do poprawnego działania aplikacji, które znajdują się w pliku <b>requirements.txt</b>. Za pomocą polecenia: 
<br><br>

``` bash
pip install -r requirements.txt
```

</li>
<li>Należy się upewnić, czy katalog api/migrations nie ma plików migracyjnych takich jak 0001_initial.py, w tym katalogu powinien znajdować się tylko plik __init__.py</li>
<li>W celu założenia tabel bazy danych aplikacji należy wykonać dwa polecenia:
<br><br>

``` bash 
 python3 manage.py makemigrations 
 python3 manage.py migrate 
```

<br>
Polecenia tworzą w bazie danych podstawową strukturę tabel dla Django oraz modele wykorzystywane w projekcie 
</li>
<li>Tworzenie superusera dla aplikacji, w tym celu należy wykonać polecenie: 
<br><br>

``` bash
python manage.py createsuperuser --username admin --email admin@example.com
```

<br>
Gdzie należy podać nazwę dla użytkownika oraz opcjonalnie adres email. W wyniku wykonania polecenia system zapyta o hasło, które trzeba nadać dla użytkownika
</li>
<li>
W celu uruchomienia aplikacji należy wykonać polecenie
<br><br>

``` bash 
python3 manage.py runserver
```

</li>
</ol>

</p>
<hr>

##### Dla serwera gunicorn

<p>
Brakuje mi wiedzy, aby uruchomić projekt na serwerze gunicorm. Będę wdzięczny za pomoc i możliwość zdobycia nowej wiedzy. 
</p>

<hr>

#### Ustawienia końcowe

<p>

##### Tworzenie grup użytkowników 

Po poprawnym uruchomieniu serwera aplikacji należy zalogować się do końcówki admin/ i utworzyć grupę użytkowników o nazwie api_users, która jest niezbędna, ponieważ jest automatycznie dodawana podczas tworzenia nowego użytkownika poprzez API. Uprawnienia jaki są nadane dla tej grupy to: 
<br><br>
<ul>
<li> API | log | Can view log</li>
<li> API | task | Can add task</li>
<li> API | task | Can change task</li>
<li> API | task | Can view task</li>
</ul>
</li>

</p>

<p>

##### Tworzenie i aktualizowanie pliku .env

Należy stworzyć lub zaktualizować plik konfiguracyjny .env, który musi zawierać takie pola jak:

```txt
SECRET_KEY=django-insecure-=@-a!zyjyz46zc!w$_(fzqv286ez#zc_ld0q64)qk)@l1(%yz%
DEBUG=False
DB_NAME=TaskKeeperDB
DB_USER=postgres
DB_PASSWORD=********
DB_HOST=localhost
DB_PORT=5433
```

</p>

</p>

<hr>

## Obsługa API

<p>

##### Przykład korzystania z API 

W celu prawidłowego wykonywania poleceń potrzeba podać w nagłówku Token uwierzytelniający

``` bash
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

<ol>
<li>Dodawanie nowego zadania do bazy danych → POST task/

Zapytanie: 

```bash
curl -X POST http://127.0.0.1:8000/api/task/ -H 'Authorization: Token 783770134349cea8888eeb1542122ffdd255bccc' -d '{"task_name": "task from curl"}' -H "Content-Type: application/json"
```

</li>
<li>Przeglądanie listy zadań → GET task/

Zapytanie:

``` bash
curl -X GET http://127.0.0.1:8000/api/task/ -H 'Authorization: Token 783770134349cea8888eeb1542122ffdd255bccc'
```

Przykład odpowiedzi z serwera:

``` json
[
    {
        "id": 1,
        "task_name": "firts for PG",
        "task_description": "upgrade some description",
        "task_status": 0,
        "task_user": null
    },
    {
        "id": 5,
        "task_name": "inne 3 dla PG",
        "task_description": "dla usera bez grupy",
        "task_status": 0,
        "task_user": null
    },
    {
        "id": 6,
        "task_name": "inne 4 dla PG",
        "task_description": "dla usera bez grupy",
        "task_status": 0,
        "task_user": null
    },
    {
        "id": 2,
        "task_name": "drugie dla PG",
        "task_description": "",
        "task_status": 2,
        "task_user": null
    }
]
```

</li>
<li>Przeglądanie pojedynczego zadania → GET task/id/

Zapytanie: 

``` bash 
curl -X GET http://127.0.0.1:8000/api/task/2/ -H 'Authorization: Token 783770134349cea8888eeb1542122ffdd255bccc' 
```

Przykład odpowiedzi z serwera:

``` json
{
    "id": 2,
    "task_name": "drugie dla PG",
    "task_description": "",
    "task_status": 2,
    "task_user": null
}
```

</li>
<li>Usuwanie zadanie z bazy → DELETE task/id/

Zapytanie:

``` bash
curl -X DELETE http://127.0.0.1:8000/api/task/6/ -H 'Authorization: Token 783770134349cea8888eeb1542122ffdd255bccc' 
```

</li>
<li>Edytowanie zadanie → PATCH task/id/

Zapytanie:

```bash 
curl -X PATCH http://127.0.0.1:8000/api/task/8/ -H 'Authorization: Token 783770134349cea8888eeb1542122ffdd255bccc' -d '{"task_description": "task from curl description"}' -H "Content-Type: application/json"
```

</li>
<li>Przeglądanie całego loga → GET log/

Zapytanie:

``` bash 
curl -X GET http://127.0.0.1:8000/api/log/ -H 'Authorization: Token 783770134349cea8888eeb1542122ffdd255bccc'
```

Przykład odpowiedzi z serwera:

```json 
[
    {
        "id": 1,
        "task_field_name": "task_description",
        "prev_value": "",
        "new_value": "upgrade some description",
        "change_time": "2024-07-08T13:29:00.734081Z",
        "task_id": 1
    },
    {
        "id": 3,
        "task_field_name": "task_status",
        "prev_value": "0",
        "new_value": "2",
        "change_time": "2024-07-08T21:27:07.442772Z",
        "task_id": 2
    }
]
```

</li>
<li>Przeglądanie pojedynczego loga → GET log/id/

Zapytanie: 

``` bash 
curl -X GET http://127.0.0.1:8000/api/log/1/ -H 'Authorization: Token 783770134349cea8888eeb1542122ffdd255bccc'
```

Przykład odpowiedzi z serwera:

``` json 
{
    "id": 1,
    "task_field_name": "task_description",
    "prev_value": "",
    "new_value": "upgrade some description",
    "change_time": "2024-07-08T13:29:00.734081Z",
    "task_id": 1
}
```

</li>
<li>Filtrowanie zadań → GET task/?

Zapytanie: 

```bash
curl -X GET http://127.0.0.1:8000/api/task?fTask_id=&fTask_name=&fTask_desctiption=curl&fTask_staus=&fTask_user= -H 'Authorization: Token 783770134349cea8888eeb1542122ffdd255bccc'
```

Przykład odpowiedzi z serwera:

```json
[
    {
        "id": 8,
        "task_name": "task from curl",
        "task_description": "task from curl description",
        "task_status": 2,
        "task_user": null
    }
]
```


</li>
<li>Filtrowanie loga → GET log/?

Zapytanie: 

```bash 
curl -X GET http://127.0.0.1:8000/api/log?fTask_id=8 -H 'Authorization: Token 783770134349cea8888eeb1542122ffdd255bccc'  
```

Przykład odpowiedzi z serwera:

```json
[
    {
        "id": 4,
        "task_field_name": "task_description",
        "prev_value": "",
        "new_value": "task from curl description",
        "change_time": "2024-07-09T13:43:05.948235Z",
        "task_id": 8
    },
    {
        "id": 5,
        "task_field_name": "task_status",
        "prev_value": "0",
        "new_value": "2",
        "change_time": "2024-07-09T13:47:46.297464Z",
        "task_id": 8
    }
]
```

</li>
<li>Dodawanie nowego użytkownika do bazy danych POST user/

Zapytanie: 

```bash 
curl -X POST http://127.0.0.1:8000/users/ -H "Content-Type: application/json" -d '{"username": "test_api_user_curl", "password":"********"}'
```

</li>
<li>Uzyskanie Tokena uwierzytelniającego GET user/

Zapytanie: 

```bash
curl -X POST http://127.0.0.1:8000/auth/ -H "Content-Type: application/json" -d '{"username":"test_api_user_01", "password":"********"}'
```

Przykład odpowiedzi z serwera:

```json
{
    "token": "7d7fe01266174bbc3eeb3bab247a10ce698474dc"
}
```

</li>
</ol>

</p>

## Dziękuję za uwagę, miłej zabawy z projektem
