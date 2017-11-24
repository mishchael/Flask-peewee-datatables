#!/usr/bin/env python3
# -*- coding:utf-8 -*-
u"""
api
"""
from flask import Blueprint
from flask import jsonify
from db.models import Employee
from src.intermediary import WorkWithDataTables


api = Blueprint("api", __name__, "templates")


@api.route("/")
def index():
    u"""
    the api
    """

    columns = [
        Employee.name, Employee.position,
        Employee.office, Employee.age,
        Employee.date, Employee.salary
    ]

    query = WorkWithDataTables(table=Employee, columns=columns)

    return jsonify(query.query())
