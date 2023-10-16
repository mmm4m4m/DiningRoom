from typing import Optional

from src.database.db import DBManager
from src.clients.models import ClientRead, ClientCreate


def get(*, db_manager: DBManager, client_id: int) -> Optional[ClientRead]:
    params = (client_id, )
    client = db_manager.execute('SELECT id, user_id ' 
                                'FROM clients '
                                'WHERE id=? ',
                                params=params)
    if not client:
        return None 
    return ClientRead(id=client[0], user_id=client[1])


def create(*, db_manager: DBManager, client_in: ClientCreate) -> int:
    params = (client_in.user_id, )
    client_id = db_manager.execute('INSERT INTO clients(user_id) '
                                   'VALUES(?) '
                                   'RETURNING id ',
                                   params=params)
    return client_id


def delete(*, db_manager: DBManager, client_id: int):
    params = (client_id, )
    db_manager.execute('DELETE FROM clients '
                       'WHERE id=?',
                       params=params)
    