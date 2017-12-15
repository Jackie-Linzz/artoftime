import mysql
import logic


def prepare():
    desks = mysql.get_all('desks')
    for one in desks:
        logic.tables[one['desk']] = logic.Table(one['desk'])
    category = mysql.get_all('category')
    for one in category:
        logic.category[one['cid']] = one
    diet = mysql.get_all('diet')
    for one in diet:
        logic.diet[one['did']] = one
    faculty = mysql.get_all('faculty')
    for one in faculty:
        logic.fids[one['fid']] = one
