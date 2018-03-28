import time
import datetime

import logic
import mysql

def get_cook_range(fid):
    sql = 'select did from cook_do where fid = "%s"' % fid
    dids = mysql.query(sql)
    all = False
    for one in dids:
        if one['did'] == 'all':
            all = True
            break
    result = []
    if all:
        result.append({'did': 'all', 'name': 'all', 'cid': ''})
    else:
        for one in dids:
            item = logic.diet.get(one['did'])
            result.append({'did': one['did'], 'name': item['name'], 'cid': item['cid']})
    return result

#datetime start, datetime end
def achieve(fid, start, end, trend):
    #import pdb
    #pdb.set_trace()
    result = []
    if trend == 0:
        if fid != 'all':
            all_rows = all_cook_flow(start, end)
            result.append({'fid': 'all', 'name': 'all', 'rows': all_rows, 'type': 'all'})
            rows = one_cook_flow(fid, start, end)
            name = logic.faculty.get(fid)['name']
            result.append({'fid': fid, 'name': name, 'rows': rows, 'type': 'cook'})
        else:
            fids = []
            for k, v in logic.faculty.items():
                if v['role'].find('cook') >= 0:
                    fids.append(k)
            all_rows = all_cook_flow(start, end)
            result.append({'fid': 'all', 'name': 'all', 'rows': all_rows, 'type': 'all'})
            fids.sort()
            for fid in fids:
                rows = one_cook_flow(fid, start, end)
                name = logic.faculty.get(fid)['name']
                result.append({'fid': fid, 'name': name, 'rows': rows, 'type': 'cook'})
    elif trend == 1:
        year = start.year
        month = start.month
        day = start.day
        if day > 28:
            day = 28
        start = datetime.datetime(year, month, day)
        nodes = []
        mid = start
        while mid < end:
            nodes.append(mid)
            year = mid.year
            month = mid.month
            day = mid.day
            month += 1
            if month > 12:
                year += 1
                month = 1
            mid = datetime.datetime(year, month, day)
        nodes.append(mid)
        #pdb.set_trace()
        length = len(nodes)
        pos = 0
        while pos < length-1:
            t1 = nodes[pos]
            t2 = nodes[pos+1]
            t1_str = t1.strftime('%Y-%m-%d')
            t2_str = t2.strftime('%Y-%m-%d')
            all_rows = all_cook_flow(t1, t2)
            result.append({'fid': 'all', 'name': 'all', 'rows': all_rows, 'type': 'all-time', 'from': t1_str, 'to': t2_str})
            rows = one_cook_flow(fid, t1, t2)
            name = logic.faculty.get(fid)['name']
            result.append({'fid': fid, 'name': name, 'rows': rows, 'type': 'cook-time', 'from': t1_str, 'to': t2_str})
            pos += 1
    return result
       
        

# start and end is datetime
def all_cook_flow(start, end):
    t1 = time.mktime(start.timetuple())
    t2 = time.mktime(start.timetuple())
    result = {}
    sql = 'select diet.did, sum(num) as number from diet,order_history,cook_history where diet.did = order_history.did and order_history.uid = cook_history.uid and cook_history.stamp > %s and cook_history.stamp < %s group by diet.did' % (t1, t2)
    rows = mysql.query(sql)
    diet = logic.diet
    for row in rows:
        did = row['did']
        result[did] = {'did': did, 'num': row['number']}
    for k, v in diet.items():
        if k in result:
            result[k]['name'] = v['name']
        else:
            result[k] = {'did': k, 'name': v['name'], 'num': 0}
    ############################################################
    sql = 'select diet.did, sum(num) as number, fb from diet,order_history,cook_history,feedback where diet.did = order_history.did and order_history.uid = cook_history.uid and cook_history.uid = feedback.uid and cook_history.stamp > %s and cook_history.stamp < %s group by diet.did,fb' % (t1, t2)
    rows = mysql.query(sql)
    for row in rows:
        did = row['did']
        num = row['number']
        if row['fb'] == -1:
            result[did]['bad-num'] = num
        elif row['fb'] == 0:
            result[did]['normal-num'] = num
        elif row['fb'] == 1:
            result[did]['good-num'] = num
    for k, v in result.items():
        if 'good-num' not in v:
            v['good-num'] = 0
        if 'normal-num' not in v :
            v['normal-num'] = 0
        if 'bad-num' not in v:
            v['bad-num'] = 0
        v['fb-num'] = v['good-num'] + v['normal-num'] + v['bad-num']
        if v['fb-num'] == 0:
            v['good-rate'] = 0
            v['bad-rate'] = 0
        else:
            v['good-rate'] = v['good-num']*100 / float(v['fb-num'])
            v['bad-rate'] = v['bad-num']*100 / float(v['fb-num'])
    result = result.values()
    result.sort(key=lambda x: x['did'])
    return result
        
def one_cook_flow(fid, start, end):
    t1 = time.mktime(start.timetuple())
    t2 = time.mktime(start.timetuple())
    result = {}
    sql = 'select diet.did, sum(num) as number from diet,order_history,cook_history where diet.did = order_history.did and order_history.uid = cook_history.uid and fid = "%s" and cook_history.stamp > %s and cook_history.stamp < %s group by diet.did' % (fid, t1, t2)
    rows = mysql.query(sql)
    diet = logic.diet
    for row in rows:
        did = row['did']
        result[did] = {'did': did, 'num': row['number']}
    for k, v in diet.items():
        if k in result:
            result[k]['name'] = v['name']
        else:
            result[k] = {'did': k, 'name': v['name'], 'num': 0}
    ############################################################
    sql = 'select diet.did, sum(num) as number, fb from diet,order_history,cook_history,feedback where diet.did = order_history.did and order_history.uid = cook_history.uid and cook_history.uid = feedback.uid and fid = "%s" and cook_history.stamp > %s and cook_history.stamp < %s group by diet.did,fb' % (fid, t1, t2)
    rows = mysql.query(sql)
    for row in rows:
        did = row['did']
        num = row['number']
        if row['fb'] == -1:
            result[did]['bad-num'] = num
        elif row['fb'] == 0:
            result[did]['normal-num'] = num
        elif row['fb'] == 1:
            result[did]['good-num'] = num
    for k, v in result.items():
        if 'good-num' not in v:
            v['good-num'] = 0
        if 'normal-num' not in v :
            v['normal-num'] = 0
        if 'bad-num' not in v:
            v['bad-num'] = 0
        v['fb-num'] = v['good-num'] + v['normal-num'] + v['bad-num']
        if v['fb-num'] == 0:
            v['good-rate'] = 0
            v['bad-rate'] = 0
        else:
            v['good-rate'] = v['good-num']*100 / float(v['fb-num'])
            v['bad-rate'] = v['bad-num']*100 / float(v['fb-num'])
    result = result.values()
    result.sort(key=lambda x: x['did'])
    return result
        
    
