#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from peewee import CharField
from peewee import DateField
from peewee import IntegerField
from peewee import Model
from peewee import SqliteDatabase


__dir__ = os.path.dirname(os.path.abspath(__file__))
db = SqliteDatabase(os.path.join(__dir__, "test.db"))


class BaseModel(Model):
    u"""
    base model
    """

    class Meta:
        u"""
        set the datatabse
        """
        database = db


class Employee(BaseModel):
    u"""
    Test table
    """
    name = CharField()
    position = CharField()
    office = CharField()
    age = IntegerField()
    date = DateField()
    salary = IntegerField()

    class Meta:
        u"""
        set table name, etc.
        """
        db_table = 'employee'


def _insert_example_data_():
    u"""
    import data to database
    """
    import re
    from bs4 import BeautifulSoup

    keys = [
        "name", "position", "office",
        "age", "date", "salary"
    ]

    with open(os.path.join(os.path.dirname(__dir__), "templates/test.html")) as r:
        html = r.read()

    soup = BeautifulSoup(html, "lxml")

    table = soup.find("table", {"id": "example"})

    data = []
    for tr in table.find("tbody").find_all("tr"):
        tem = {key: value.text for key, value in zip(keys, tr.find_all("td"))}
        tem.update({"salary": re.sub(r"[,$]", "", tem.pop("salary"))})
        data.append(tem)

    if not Employee.table_exists():
        Employee.create_table()

    Employee.insert_many(data).execute()


if __name__ == '__main__':
    _insert_example_data_()
