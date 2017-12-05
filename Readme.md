## This project just takes a few hours of work. It's still have a lot of problems.

[<http://www.jianshu.com/p/ae7c7b25c5a7>](http://www.jianshu.com/p/ae7c7b25c5a7)

看了flask_peewee，下一步可能还是更想完善这个模块，将最终的用法与flask_resetful等相一致，等这个课题完成投稿之后，就会开始着手学习处理这个东西了，争取最晚过年期间开始吧

The framework that I used,
- Flask - web microframework - [<http://flask.pocoo.org/>](http://flask.pocoo.org/)
- peewee - manage database - [<http://docs.peewee-orm.com/en/latest/>](http://docs.peewee-orm.com/en/latest/)
- datatables - data display - [<https://www.datatables.net/>](https://www.datatables.net/)
- sqlite3

You could run the example locally


Some tables of mime just too big for the zero configuration datatables, therefore, I google for a while do not find any solution, then here we are.

> The way I solve this is just anaysis the parameters that datatables added, then do something about it.

#### simple usage
```python
from flask import Blueprint
from flask import jsonify
from models import Employee            # peewee table
from intermediary import WorkWithDataTables


api = Blueprint("api", __name__, "templates")


@api.route("/")
def index():
    u"""
    the api
    """

    # first of all choose which columns you needed
    columns = [
        Employee.name, Employee.position,
        Employee.office, Employee.age,
        Employee.date, Employee.salary
    ]

    # init the class with peewee table, and the specific columns
    query = WorkWithDataTables(table=Employee, columns=columns)

    # using .query() to get the databack
    return jsonify(query.query())
```

#### parameters of WorkWithDataTables

1. `query = WorkWithDatatables(table=some table, columns=None, join=None)`
    - **table**: the table you want to query, Essential
    - **columns**: which columns you want to select, 
        - iterable eg: list, tuples,
        - if this parameters is None, default select all the columns of the table you submit
    - **join**: if you want select data from join table, submit the joint table at here

2. `query.query(condition=None, search=True, order=None, **kwargs)`
    - **condition**: Query conditions, 
        - eg: (Employee.name == "test") & (Employee.salary >= 500)
    - **search**: if False, you will disable the query function, using the query box of datatables
        - means: whatever you input in the query box of datatables, nothing gonna happend.
    - **order**: the default order, submit the peewee column here
        - eg: Employee.salary
    - **\*\*kwargs**: just a total for now, 
        - **total**: if your table is too big and the Count function of peewee is kind of slow, you could just set the total here

#### javascript usage

The html page:
```html
<!-- the table with thead -->
<table id="example" class="table table-striped table-bordered" width="100%" cellspacing="0">
    <thead>
        <tr>
            <th>Name</th>
            <th>Position</th>
            <th>Office</th>
            <th>Age</th>
            <th>Start date</th>
            <th>Salary</th>
        </tr>
    </thead>
    <tfoot>
        <tr>
            <th>Name</th>
            <th>Position</th>
            <th>Office</th>
            <th>Age</th>
            <th>Start date</th>
            <th>Salary</th>
        </tr>
    </tfoot>
</table>

<!-- javascripts to init datatables -->
<script>
    $(document).ready(function() {
        var table = $('#example').DataTable( {
            "processing": true,         // using serverside to process data
            "serverSide": true,
            "pagingType": "full_numbers",       // nothing important
            ajax: {                         // set api url with jinja
                url: "{{ url_for('api.index')|safe }}",
            },
            "columns": [                    // modify the retrived data to match the columns
                { data: "name"},
                { data: "position", "searchable": false },
                { data: "office", "searchable": false },
                { data: "age" },
                { data: "date" },
                { 
                    data: "salary",
                    "render": function( data, type, row, meta ){
                        return "$" + data; 
                    }
                }
            ]                  
        } );
    } );
</script>

```
