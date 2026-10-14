def login(cursor, name, password, login):
    # ruleid: openctem.python.sqli.string-built-query
    sql_query = "SELECT * FROM users WHERE user='" + name + "' AND password='" + password + "'"
    # ruleid: openctem.python.sqli.string-built-query
    val = login.objects.raw(sql_query)
    # ok: openctem.python.sqli.string-built-query
    cursor.execute("SELECT * FROM users WHERE user = %s", (name,))
    # ok: openctem.python.sqli.string-built-query
    label = "hello " + name
    return val, label
