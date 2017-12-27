import pickle
import os
import shutil
import mysql
import logic


def prepare():
    #first time to run
    sync()

def save():
    #save data for resume
    if not os.path.isdir(logic.data_dir):
        os.mkdir(logic.data_dir)
    with open(logic.company_file, 'wb') as f:
        pickle.dump(logic.info, f)
    with open(logic.data_file, 'wb') as f:
        logic.waiting.waiters = set()
        logic.tables.waiters = set()
        logic.cooks.waiters = set()
        logic.mask.waiters = set()
        data = {'waiting': logic.waiting, 'tables': logic.tables, 'uids': logic.uids, 'cooks': logic.cooks, 'diet': logic.diet,
                'category': logic.category, 'desks': logic.desks, 'cook_do': logic.cook_do, 'uid': logic.global_uid,
                'pid': logic.global_pid, 'mask': logic.mask}
        pickle.dump(data, f)


def resume():
    #consider the difference between first time and not first time
    if not os.path.exists(logic.data_file):
        sync()
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
        logic.mask = data['mask']

def sync():
    #company_file
    if os.path.exists(logic.company_file):
        with open(logic.company_file, 'rb') as f:
            info = pickle.load(f)
    else:
        info =  {'company': '', 'shop': '', 'location': '', 'heading': '', 'welcome': '', 'desp': ''}
    logic.info = info
    #desks and tables
    desks = mysql.get_all('desks')
    logic.desks = set()
    logic.tables = {}
    for one in desks:
        logic.desks.add(one['desk'])
        logic.tables[one['desk']] = logic.Table(one['desk'])
    #category
    category = mysql.get_all('category')
    logic.category = {}
    for one in category:
        logic.category[one['cid']] = one
    #diet
    diet = mysql.get_all('diet')
    logic.diet = {}
    for one in diet:
        logic.diet[one['did']] = one
    #mask
    mask = mysql.get_all('mask')
    logic.mask.content = set()
    for one in mask:
        logic.mask.add(one['did'])
    #cook_do
    cook_do = mysql.get_all('cook_do')
    logic.cook_do = {}
    for one in cook_do:
        if one['fid'] not in logic.cook_do:
            logic.cook_do[one['fid']] = set()
        logic.cook_do.get(one['fid']).add(one['did'])
    for k, v in logic.cook_do.items():
        if u'all' in v:
            v = set([u'all'])
