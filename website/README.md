## API Ollert

### Board

#### `make-board`
Crea una board
```
{
    name: <nome>,
    description: <descrizione>,
    category: <categoria>,
    favorite: <true|false>
}
```

#### `delete-board`
Elimina una board
```
{
    name: <nome>
}
```

#### `edit-board`
Modifica uno o più campi di una board
```
{
    board: <nome board>
    edits: <lista delle modifiche>
    [...
        {
            target_field: <name|category|favorite|background|description>
            new_value: <nuovo valore del target_field>
        },
    ...]
}
```
`edits` è la lista delle modifiche da apportare, ciascuna a sua volta in formato JSON
<br>

### Liste e Card

#### `create-board-content`
Crea Lista/Card. Si hanno due formati del JSON, uno per quando l'azione è eseguita su una lista e una per quando è eseguita su una card
```
{
    target_type: list
    owner: <username utente modificante>
    target_id:
    {
        target_id_board: <nome della board>
    }
    new_data:
    { 
        list_name: <nome lista>
    }
}
```
```
{
    target_type: card
    owner: <username utente modificante>
    target_id:
    {
        target_id_board: <nome della board>
        target_id_list: <id della lista>
    }
    new_data:
    { 
        card_name: <nome card>
        card_descr: <descrizione card>
        card_date: <data card>
        card_img: <immagine card (non so ancora come)>
        card_checks: <checklist card (non so ancora come)>
        card_members: <elenco utenti assegnati alla card (non so ancora come)>
        card_tags: <elenco tag assegnati alla card>
    }
}
```
<br>

#### `delete-board-content`
Elimina uno o più oggetti
```
{
    board: <nome della board>
    targets: <oggetti da eliminare>
    [...
        {
            target_type: <list|card>
            target_id: {
                target_id_list: <id della lista>
                target_id_card: <id della card> #se si deve eliminare una card
            }
        },
    ...]
}
```
<br>

#### `edit-board-content`
Modifica un campo di una lista o card. Anche in questo caso, si hanno due formati JSON
```
{
    target_type: <list>
    target_id: {
        target_id_board: <nome della board>
        target_id_list: <id della lista>
    }
    new_value: <nuovo valore del target field>
}
```
```
{
    target_type: <card>
    target_id: {
        target_id_board: <nome della board>
        target_id_list: <id della lista>
        target_id_card: <id della card>
    }
    target_field: <name|description|date|img|checks|members|tags>
    new_value: <nuovo valore del target field>
}
```
Da notare che `target_field` non sia necessario per una lista in quanto solo il titolo è modificabile
<br>

### Categorie

#### `create-category`
Crea una categoria
```
{
    new_cat_name: <nome>
}
```
<br>

#### `delete-category`
Elimina una categoria
```
{
    cat_name: <nome>
}
```
<br>

#### `rename-category`
Rinomina una categoria
```
{
    cat_name: <nome>
    new_vale: <nuovo nome>
}
```
<br>

### Gestione utenti Board/Card
Il campo `action` deve contenere una di due stringhe possibili, `ADDED` o `REMOVED` 

#### Board
```
{
    receiver: <nome destinatario>
    board_name: <nome board>
    action: <ADDED|REMOVED>
}
```

#### Card
```
{
    receiver: <nome destinatario>
    board_name: <nome board>
    list_id: <pos lista>
    card_id: <pos card>
    action: <ADDED|REMOVED>
}
```

### Formattare dati particolari

#### Checklist
La checklist deve essere un JSON nel formato:
```
{
    ...
    <nome del check>: <true|false>
    ...
}
```
ossia un dizionario dei check, ciascuno associato a `true` (è selezionato) o `false`
<br>

#### Membri
Gli utenti membri di una card o board si specificano con una semplice lista di nomi:
```
[ n1, n2, n3, ... ]
```

