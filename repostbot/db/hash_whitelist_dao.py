import sqlite3
from sqlite3 import Row
from typing import Iterable


class HashWhitelistDAO:

    @staticmethod
    def init_db():
        """Автоматически создает таблицу hash_whitelist при ее отсутствии"""
        with sqlite3.connect('repostdb.sqlite') as connection:
            cursor = connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hash_whitelist (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER NOT NULL,
                    hash_value TEXT NOT NULL
                )
            ''')
            connection.commit()

    @staticmethod
    def get_whitelisted_hashes_for_group(group_id: int) -> set[str]:
        HashWhitelistDAO.init_db()
        with sqlite3.connect('repostdb.sqlite') as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            result: list[Row] = cursor.execute(
                'select hash_value from hash_whitelist where group_id = ?',
                (group_id,)
            ).fetchall()
            return {row['hash_value'] for row in result}

    @staticmethod
    def insert_whitelist_hashes_for_group(group_id: int, hashes_to_add: Iterable[str]):
        HashWhitelistDAO.init_db()
        with sqlite3.connect('repostdb.sqlite') as connection:
            cursor = connection.cursor()
            cursor.executemany(
                'insert into hash_whitelist(group_id, hash_value) values (?, ?)',
                ((group_id, hash_value) for hash_value in hashes_to_add)
            )

    @staticmethod
    def remove_whitelist_hashes_for_group(group_id: int, hashes_to_remove: Iterable[str]):
        HashWhitelistDAO.init_db()
        with sqlite3.connect('repostdb.sqlite') as connection:
            cursor = connection.cursor()
            cursor.executemany(
                'delete from hash_whitelist where group_id = ? and hash_value = ?',
                ((group_id, hash_value) for hash_value in hashes_to_remove)
            )

    @staticmethod
    def remove_all_whitelist_hashes_for_group(group_id: int):
        HashWhitelistDAO.init_db()
        with sqlite3.connect('repostdb.sqlite') as connection:
            cursor = connection.cursor()
            cursor.execute(
                'delete from hash_whitelist where group_id = ?',
                (group_id,)
            )