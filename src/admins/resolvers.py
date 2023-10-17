from src.database.db import DBManager
from src.admins.models import AdminRead, AdminCreate


def get(*, db_manager: DBManager, admin_id: int) -> AdminRead:
    params = (admin_id, )
    admin = db_manager.execute('SELECT id, user_id, first_name, last_name '
                               'FROM admins '
                               'WHERE admin_id=? ',
                               params=params)
    if not admin:
        return None 
    return AdminRead(id=admin[0], user_id=admin[1], first_name=admin[2], last_name=admin[3])


def create(*, db_manager: DBManager, admin_in: AdminCreate) -> int:
    params = (admin_in.user_id, admin_in.fist_name, admin_in.last_name)
    admin_id = db_manager.execute('INSERT INTO admin(user_id, first_name, last_name) '
                                  'VALUES(?, ?, ?) '
                                  'RETURNING id ',
                                  params=params)[0]
    return admin_id


def delete(*, db_manager: DBManager, admin_id: int):
    params = (admin_id, )
    db_manager.execute('DELETE FROM admin'
                       'WHERE id=?',
                       params=params)
