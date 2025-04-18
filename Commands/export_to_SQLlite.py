# api/management/commands/export_to_sqlite.py
import sqlite3
from django.core.management.base import BaseCommand
from api.models import Inspector, Registry, Object, SuperVisor, Contractor, Work, ContractorMan, Chislo, Violation

class Command(BaseCommand):
    help = 'Экспортирует данные из моделей Django в SQLite'

    def handle(self, *args, **kwargs):
        # Подключение к SQLite
        conn = sqlite3.connect('exported_data.db')
        cursor = conn.cursor()

        # Создаем таблицы в SQLite для каждой модели Django
        cursor.execute('''CREATE TABLE IF NOT EXISTS Inspector (
                            id INTEGER PRIMARY KEY,
                            NominativeName TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Registry (
                            id INTEGER PRIMARY KEY,
                            ParentID INTEGER,
                            Context TEXT,
                            Name TEXT,
                            iValue INTEGER,
                            dValue REAL,
                            sValue TEXT,
                            dtValue TEXT,
                            rValue TEXT,
                            Info TEXT,
                            iValue1 INTEGER,
                            iValue2 INTEGER,
                            sValue1 TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Object (
                            id INTEGER PRIMARY KEY,
                            ParentID INTEGER,
                            NodeTypeID INTEGER,
                            Name TEXT,
                            RegionCode TEXT,
                            Code TEXT,
                            iValue INTEGER,
                            IsLock INTEGER)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS SuperVisor (
                            id INTEGER PRIMARY KEY,
                            Login TEXT,
                            GuID TEXT,
                            FullName TEXT,
                            ShortName TEXT,
                            IsMain INTEGER)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Contractor (
                            id INTEGER PRIMARY KEY,
                            NominativeName TEXT,
                            GenitiveName TEXT,
                            IsBranch INTEGER,
                            IsCustomer INTEGER,
                            IsBuildWatch INTEGER,
                            Series TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Work (
                            id INTEGER PRIMARY KEY,
                            Context TEXT,
                            Name TEXT,
                            Ord INTEGER,
                            Tmp1 INTEGER,
                            Tmp2 INTEGER)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS ContractorMan (
                            id INTEGER PRIMARY KEY,
                            ContractorID INTEGER,
                            ShortName TEXT,
                            NominativeName TEXT,
                            IsBoss INTEGER)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Chislo (
                            id INTEGER PRIMARY KEY,
                            Chislooo TEXT)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Violation (
                            id INTEGER PRIMARY KEY,
                            description TEXT,
                            document TEXT)''')

        # Экспорт данных из моделей Django в SQLite
        self.export_data(cursor, Inspector, 'Inspector', ['id', 'NominativeName'])
        self.export_data(cursor, Registry, 'Registry', ['id', 'ParentID', 'Context', 'Name', 'iValue', 'dValue', 'sValue', 'dtValue', 'rValue', 'Info', 'iValue1', 'iValue2', 'sValue1'])
        self.export_data(cursor, Object, 'Object', ['id', 'ParentID', 'NodeTypeID', 'Name', 'RegionCode', 'Code', 'iValue', 'IsLock'])
        self.export_data(cursor, SuperVisor, 'SuperVisor', ['id', 'Login', 'GuID', 'FullName', 'ShortName', 'IsMain'])
        self.export_data(cursor, Contractor, 'Contractor', ['id', 'NominativeName', 'GenitiveName', 'IsBranch', 'IsCustomer', 'IsBuildWatch', 'Series'])
        self.export_data(cursor, Work, 'Work', ['id', 'Context', 'Name', 'Ord', 'Tmp1', 'Tmp2'])
        self.export_data(cursor, ContractorMan, 'ContractorMan', ['id', 'ContractorID', 'ShortName', 'NominativeName', 'IsBoss'])
        self.export_data(cursor, Chislo, 'Chislo', ['id', 'Chislooo'])
        self.export_data(cursor, Violation, 'Violation', ['id', 'description', 'document'])

        # Сохраняем изменения в базе данных SQLite
        conn.commit()
        conn.close()

        self.stdout.write(self.style.SUCCESS('Данные успешно экспортированы в SQLite!'))

    def export_data(self, cursor, model, table_name, fields):
        """Экспортирует данные из модели Django в таблицу SQLite"""
        queryset = model.objects.all()
        for obj in queryset:
            values = [getattr(obj, field) for field in fields]
            placeholders = ', '.join('?' for _ in values)
            cursor.execute(f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({placeholders})", tuple(values))

