import pickle
import os
import shutil
import mysql
import logic


def prepare():
    #first time to run
    sync()
    logic.idle_desks = logic.Idle_desks()

def save():
    #save data for resume
    data_dir = os.path.expanduser(logic.data_dir)
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)
    company_file = os.path.expanduser(logic.company_file)
    with open(company_file, 'wb') as f:
        pickle.dump(logic.info, f)
    data_file = os.path.expanduser(logic.data_file)
    with open(data_file, 'wb') as f:
        for k, v in logic.waiting.items():
            v.waiters = set()
        for k, v in logic.tables.items():
            v.waiters = set()
        for k, v in logic.cooks.items():
            v.waiters = set()
        logic.mask.waiters = set()
        data = {'waiting': logic.waiting, 'tables': logic.tables, 'uids': logic.uids, 'cooks': logic.cooks, 'diet': logic.diet,
                'category': logic.category, 'desks': logic.desks, 'cook_do': logic.cook_do, 'uid': logic.global_uid,
                'pid': logic.global_pid}
        pickle.dump(data, f)


def resume():
    #consider the difference between first time and not first time
    if not os.path.isfile(logic.data_file):
        sync()
        return
    # not first time
    if os.path.exists(logic.company_file):
        with open(logic.company_file, 'rb') as f:
            info = pickle.load(f)
    else:
        info =  {'company': '', 'shop': '', 'location': '', 'heading': '', 'welcome': '', 'desp': ''}
    logic.info = info

    with open(logic.data_file, 'rb') as f:
        data = pickle.load(f)
        logic.waiting = data['waiting']
        logic.tables = data['tables']
        logic.uids = data['uids']
        logic.cooks = data['cooks']
        logic.diet = data['diet']
        logic.category = data['category']
        logic.desks = data['desks']
        logic.cook_do = data['cook_do']
        logic.global_pid = data['pid']
        logic.global_uid = data['uid']
        

def sync():
    #company_file
    #import pdb
    #pdb.set_trace()
    #print logic.company_file
    sync_info()
    sync_pid()
    sync_uid()
    #desks and tables
    sync_tables()
    #category
    sync_category()
    #diet
    sync_diet()
    #mask
    #mask = mysql.get_all('mask')
    #logic.mask.content = set()
    #for one in mask:
    #    logic.mask.add(one['did'])
    #faculty
    sync_faculty()
    #cook_do
    sync_cookdo()

def sync_pid():
    result = mysql.get('id', {'name': 'pid'})
    if len(result) == 0:
        mysql.insert('id', {'name': 'pid', 'num': 0})
        logic.global_pid = 0
    else:
        logic.global_pid = result[0]['num']

def sync_uid():
    result = mysql.get('id', {'name': 'uid'})
    if len(result) == 0:
        mysql.insert('id', {'name': 'uid', 'num': 0})
        logic.global_uid = 0
    else:
        logic.global_uid = result[0]['num']

def sync_info():
    if os.path.isfile(logic.company_file):
        with open(logic.company_file, 'rb') as f:
            info = pickle.load(f)
    else:
        info =  {'company': '', 'shop': '', 'location': '', 'heading': '', 'welcome': '', 'desp': ''}
    logic.info = info

def sync_tables():
    desks = mysql.get_all('desks')
    logic.desks = set()
    logic.tables = {}
    for one in desks:
        logic.desks.add(one['desk'])
        logic.tables[one['desk']] = logic.Table(one['desk'])

def sync_category():
    category = mysql.get_all('category')
    logic.category = {}
    for one in category:
        logic.category[one['cid']] = one

def sync_diet():
    diet = mysql.get_all('diet')
    logic.diet = {}
    for one in diet:
        logic.diet[one['did']] = one

def sync_faculty():
    faculty = mysql.get_all('faculty')
    for one in faculty:
        logic.faculty[one['fid']] = one

def sync_cookdo():
    cook_do = mysql.get_all('cook_do')
    logic.cook_do = {}
    for one in cook_do:
        if one['fid'] not in logic.cook_do:
            logic.cook_do[one['fid']] = set()
        logic.cook_do.get(one['fid']).add(one['did'])
    for k, v in logic.cook_do.items():
        if u'all' in v:
            v = set([u'all'])
