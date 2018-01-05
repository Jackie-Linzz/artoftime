import MySQLdb
# don't forget to adjust conn.close() cursor.close()

HOST = 'localhost'
PORT = 3306
USER = 'artoftime'
PASSWD = 'artoftime'
DB = 'artoftime'


#row is dict
def insert(table, row):

    if not isinstance(row, dict):
        return False
    columns = []
    values = []
    for k, v in row.items():
        
        columns.append(unicode(k))
        if isinstance(v, (str, unicode)):
            v = '"%s"' % v
            
        values.append(unicode(v))
    columns = ','.join(columns)
    values = ','.join(values)

    conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB, charset='utf8')
    conn.autocommit(False)
    cursor = conn.cursor()
    sql = 'insert into %s (%s) values (%s)' % (table, columns, values)
    try:

        cursor.execute(sql)
        conn.commit()
        return True
    except Exception as e:
        print e
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def insert_many(table, rows):
    #check row key consistence
    if not isinstance(rows, (list, tuple)):
        return False
    if len(rows) < 1:
        return False
    if not isinstance(rows[0], dict):
        return False
    keys = rows[0].keys()
    columns = ','.join(keys)
    template = ','.join(['%s'] * len(keys))

    values = []
    for row in rows:
        if set(keys) != set(row.keys()):
            return False
        temp = []
        for key in keys:
            v = row[key]
            #if isinstance(v, (str, unicode)):#error
            #    v = '"%s"' % v
            temp.append(v)
        values.append(temp)

    conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB, charset='utf8')
    conn.autocommit(False)
    cursor = conn.cursor()
    sql = 'insert into %s (%s) values (%s)' % (table, columns, template)

    try:

        cursor.executemany(sql, values)
        conn.commit()
        return True
    except Exception as e:
        print e
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def delete(table, con):

    if not isinstance(con, dict):
        return False
    condition = []
    for k, v in con.items():
        if isinstance(v, (str, unicode)):
            v = '"%s"' % v
        condition.append('%s = %s' % (k, v))
    condition = ' and '.join(condition)
    condition = unicode(condition)
    sql = 'delete from %s where %s' % (table, condition)

    conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB, charset='utf8')
    conn.autocommit(False)
    cursor = conn.cursor()
    try:

        cursor.execute(sql)
        conn.commit()
        return True
    except Exception as e:
        print e
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def delete_all(table):

    conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB, charset='utf8')
    conn.autocommit(False)
    cursor = conn.cursor()
    sql = 'delete from %s' % table
    try:

        cursor.execute(sql)
        conn.commit()
        return True
    except Exception as e:
        print e
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def update(table, con, row):

    conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB, charset='utf8')
    conn.autocommit(False)
    cursor = conn.cursor()

    if not isinstance(con, dict):
        return False
    condition = []
    for k, v in con.items():
        if isinstance(v, (str, unicode)):
            v = '"%s"' % v
        condition.append('%s = %s' % (k, v))
    condition = ' and '.join(condition)

    if not isinstance(row, dict):
        return False
    new_row = []
    for k, v in row.items():

        if isinstance(v, (str, unicode)):
            v = '"%s"' % v
        new_row.append('%s=%s' % (k, v))
    new_value = ','.join(new_row)

    sql = 'update %s set %s where %s' % (table, new_value, condition)
    try:

        cursor.execute(sql)
        conn.commit()
        return True
    except Exception as e:
        print e
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def execute(sql):
    conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB, charset='utf8')
    conn.autocommit(False)
    cursor = conn.cursor()
    try:

        cursor.execute(sql)
        conn.commit()
        return True
    except Exception as e:
        print e
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def query(sql):
    conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB, charset='utf8')
    conn.autocommit(False)
    cursor = conn.cursor()
    try:
        
        cursor.execute(sql)
        conn.commit()
        columns = [d[0] for d in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result
    except Exception as e:
        print e
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()

def get(table, con):

    if not isinstance(con, dict):
        return False
    condition = []
    for k, v in con.items():
        if isinstance(v, (str, unicode)):
            v = '"%s"' % v
        condition.append('%s = %s' % (k, v))
    condition = ' and '.join(condition)
    sql = 'select * from %s where %s' % (table, condition)

    conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB, charset='utf8')
    conn.autocommit(False)
    cursor = conn.cursor()
    try:

        cursor.execute(sql)
        conn.commit()
        columns = [d[0] for d in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result
    except Exception as e:
        print e
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()


def get_all(table):
    sql = 'select * from %s' % table

    conn = MySQLdb.connect(host=HOST, port=PORT, user=USER, passwd=PASSWD, db=DB, charset='utf8')
    conn.autocommit(False)
    cursor = conn.cursor()
    try:

        cursor.execute(sql)
        conn.commit()
        columns = [d[0] for d in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result
    except Exception as e:
        print e
        conn.rollback()
        return None
    finally:
        cursor.close()
        conn.close()





