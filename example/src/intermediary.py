#!/usr/bin/env python3
# -*- coding:utf-8 -*-
u"""
The way I mix everything together
"""
import re
from collections import OrderedDict
from flask import request
from peewee import BooleanField
from peewee import IntegerField
from peewee import FloatField


# flask配合datatables使用的类
class WorkWithDataTables(object):
    u"""
    2017.11.15
    开始设计类，想办法自行处理dtatables返回的参数
    """

    def __init__(self, table, columns=None, join=None):
        u"""
        初始化
        :param columns: 列表，传入查询的columns
        """
        # 构建
        if columns is None:
            columns = list(table._meta.fields.values())

            if join:
                columns += list(join._meta.fields.values())

        start = 0
        tem = []
        for i in columns:
            tem.append([start, i])
            start += 1
        self.columns = OrderedDict(tem)
        self.table = table
        self.join = join

    @staticmethod
    def get_parameter(label, default=None):
        tem = request.args.get(label)

        if tem is None:
            return default
        return tem.strip()

    def _searchable_(self, index):
        if self.get_parameter("columns[%d][searchable]" % index) == "true":
            return True
        else:
            return False

    def _set_order_(self):
        u"""
        指定order
        :param querys:
        :return:
        """
        # 指定排序方式
        order = self.get_parameter("order[0][column]")
        order_by = None

        if order:
            order = int(order)
            order_by = self.columns.get(order)
            order_dir = self.get_parameter("order[0][dir]")

            if order_by and order_dir == "desc":
                order_by = order_by.desc()

        return order_by

    def _set_search_(self):
        # 指定排序
        search = self.get_parameter("search[value]")

        # 判断一下输入的是否是boolean值
        if search is not None:
            if re.search(r"^(true|yes)$", search, re.I):
                search = True
            elif re.search(r"^(false|no)$", search, re.I):
                search = False
            else:
                search = search

        search_condition = None
        if search:
            for i in self.columns:
                if self._searchable_(i):
                    # 如果遇到布尔型，需要独特的处理方法
                    if isinstance(self.columns[i], BooleanField) and\
                            not isinstance(search, bool):
                        if search_condition is None:
                            search_condition = (self.columns[i] == None)
                        else:
                            search_condition = (
                                self.columns[i] == None) | search_condition
                        continue

                    # if this column is integer type
                    if isinstance(self.columns[i], IntegerField):
                        try:
                            search = int(search)
                            if search_condition is None:
                                search_condition = (self.columns[i] == search)
                            else:
                                search_condition = (
                                    self.columns[i] == search
                                ) | search_condition
                        except:
                            continue
                        continue

                    # if this column is float type
                    if isinstance(self.columns[i], FloatField):
                        try:
                            search = float(search)
                            if search_condition is None:
                                search_condition = (self.columns[i] == search)
                            else:
                                search_condition = (
                                    self.columns[i] == search
                                ) | search_condition
                        except:
                            continue
                        continue

                    # 如果符合要求就不用管了，正常处理即可
                    if search_condition is None:
                        search_condition = (
                            self.columns[i].regexp(str(search) + ".*"))
                    else:
                        search_condition = (self.columns[i].regexp(
                            str(search) + ".*")) | search_condition
        return search_condition

    def query(self, condition=None, search=True, order=None, **kwargs):
        u"""
        查询
        :param condition: 
        :return: 
        """
        # 获取参数
        page = int(self.get_parameter("start", 1)) / 10 + 1
        per_page = int(self.get_parameter("length", 10))
        draw = int(self.get_parameter("draw", 1))

        querys = self.table.select(*self.columns.values())

        if order:
            querys = querys.order_by(order)

        # 指定非第一次的查询，才会通过这个排序方式排序
        if draw > 1:
            order = self._set_order_()
            querys = querys.order_by(order)

        # 如果有外链表，就外链
        if self.join:
            querys = querys.join(self.join)

        # 如果有查询条件或者搜索条件，就分别指定不同的条件
        if condition and search:
            search_condition = self._set_search_()

            if search_condition:
                condition = condition & search_condition
        elif search:
            condition = self._set_search_()

        if condition:
            querys = querys.where(condition)

        if kwargs.get("total") is not None:
            total = kwargs["total"]
        else:
            total = querys.count()
        querys = querys.paginate(page, per_page)

        data = [x for x in querys.dicts()]

        return {
            "data": data,
            "draw": draw,
            "start": page,
            "length": per_page,
            "recordsTotal": total,
            "recordsFiltered": total
        }
