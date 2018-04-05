import time
import datetime
import re
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

def time_nodes(start, end, interval='month'):
    if interval == 'month':
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
        return nodes
    if interval == '30m':
        span = datetime.timedelta(seconds=60*30)
        nodes = []
        mid = start
        while mid < end:
            nodes.append(mid)
            mid += span
        nodes.append(mid)
        return nodes

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
        nodes = time_nodes(start, end)
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
    t2 = time.mktime(end.timetuple())
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

#start end is datetime
def one_cook_flow(fid, start, end):
    t1 = time.mktime(start.timetuple())
    t2 = time.mktime(end.timetuple())
    #print 't1, t2:', t1, ',', t2
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

#start and end is datatime
def flow(start, end, trend):
    result = []
    if trend == 0:
        rows = flow_data(start, end)
        t1 = start.strftime('%Y-%m-%d')
        t2 = end.strftime('%Y-%m-%d')
        result.append({'type': '', 'rows': rows, 'from': t1, 'to': t2})
    else:
        nodes = time_nodes(start, end)
        length = len(nodes)
        pos = 0
        while pos < length-1:
            t1 = nodes[pos]
            t2 = nodes[pos+1]
            t1_str = t1.strftime('%Y-%m-%d')
            t2_str = t2.strftime('%Y-%m-%d')
            rows = flow_data(t1, t2)
            result.append({'type': 'trend', 'rows': rows, 'from': t1_str, 'to': t2_str})
            pos += 1
    return result


def flow_data(start, end):
    start = time.mktime(start.timetuple())
    end = time.mktime(end.timetuple())
    result = {}
    sql = 'select order_history.did,name,diet.price,sum(num) as number, sum(order_history.price*order_history.num) as sales from diet,order_history,cash_history where diet.did = order_history.did and order_history.uid = cash_history.uid and status ="success" and order_history.stamp > %s and order_history.stamp < %s group by order_history.did' % (start, end)
    rows = mysql.query(sql)
    num = 0
    sales = 0
    for row in rows:
        did = row['did']
        if did not in result:
            result[did] = {}
        result[did]['did'] = did
        result[did]['name'] = row['name']
        result[did]['price'] = row['price']
        result[did]['num'] = row['number']
        result[did]['sales'] = row['sales']
        num += row['number']
        sales += row['sales']
    sql = 'select diet.did,name,fb,sum(num) as number from diet,order_history,feedback where order_history.uid = feedback.uid and order_history.did = diet.did and order_history.stamp > %s and order_history.stamp < %s group by diet.did,fb' % (start, end)
    rows = mysql.query(sql)
    for row in rows:
        did = row['did']
        if did not in result:
            result[did] = {}
        if row['fb'] == -1:
            result[did]['bad-num'] = row['number']
        elif row['fb'] == 0:
            result[did]['normal-num'] = row['number']
        elif row['fb'] == 1:
            result[did]['good-num'] = row['number']
    for k, v in logic.diet.items():
        if k not in result:
            result[k] = {}
        if 'did' not in result[k]:
            result[k]['did'] = v['did']
        if 'name' not in result[k]:
            result[k]['name'] = v['name']
        if 'price' not in result[k]:
            result[k]['price'] = v['price']
        if 'num' not in result[k]:
            result[k]['num'] = 0
        if 'sales' not in result[k]:
            result[k]['sales'] = 0
        if 'bad-num' not in result[k]:
            result[k]['bad-num'] = 0
        if 'normal-num' not in result[k]:
            result[k]['normal-num'] = 0
        if 'good-num' not in result[k]:
            result[k]['good-num'] = 0
        if 'fb-num' not in result[k]:
            result[k]['fb-num'] = result[k]['good-num'] + result[k]['normal-num'] + result[k]['bad-num']
        if 'bad-rate' not in result[k]:
            if result[k]['fb-num'] == 0:
                result[k]['bad-rate'] = 0
            else:
                result[k]['bad-rate'] = result[k]['bad-num'] * 100.0 / result[k]['fb-num']
        if 'normal-rate' not in result[k]:
            if result[k]['fb-num'] == 0:
                result[k]['normal-rate'] = 0
            else:
                result[k]['normal-rate'] = result[k]['normal-num'] * 100.0 / result[k]['fb-num']
        if 'good-rate' not in result[k]:
            if result[k]['fb-num'] == 0:
                result[k]['good-rate'] = 0
            else:
                result[k]['good-rate'] = result[k]['good-num'] * 100.0 / result[k]['fb-num']
        if 'num-rate' not in result[k]:
            if num == 0:
                result[k]['num-rate'] = 0
            else:
                result[k]['num-rate'] = result[k]['num'] * 100.0 / num
        if 'sales-rate' not in result[k]:
            if sales == 0:
                result[k]['sales-rate'] = 0
            else:
                result[k]['sales-rate'] = result[k]['sales'] * 100.0 / sales
    
    result = result.values()
    result.sort(key=lambda x: x['did'])
    return result

def one_diet(did, start, end, trend):
    result = []
    if trend == 0:
        table = one_diet_table(did, start, end)
        result.append(table)

    elif trend == 1:
        nodes = time_nodes(start, end)
        length = len(nodes)
        pos = 0
        while pos < length -1:
            table = one_diet_table(did, nodes[pos], nodes[pos+1])
            result.append(table)
            pos += 1
    return result

        
def one_diet_table(did, start, end):
    table = {}
    t1 = start.strftime('%Y-%m-%d')
    t2 = end.strftime('%Y-%m-%d')
    table['from'] = t1
    table['to'] = t2
    all_num = 0
    all_sales = 0
    all_fb_num = 0
    all_good_num = 0
    all_normal_num = 0
    all_bad_num = 0
    rows = flow_data(start, end)
    for row in rows:
        all_num += row['num']
        all_sales += row['sales']
        all_fb_num += row['fb-num']
        all_good_num += row['good-num']
        all_normal_num += row['normal-num']
        all_bad_num += row['bad-num']
        if row['did'] == did:
            table['did'] = did
            table['name'] = row['name']
            table['price'] = row['price']
            table['num'] = row['num']
            table['sales'] = row['sales']
            table['num-rate'] = row['num-rate']
            table['sales-rate'] = row['sales-rate']
            table['fb-num'] = row['fb-num']
            table['good-num'] = row['good-num']
            table['normal-num'] = row['normal-num']
            table['bad-num'] = row['bad-num']
            table['good-rate'] = row['good-rate']
            table['normal-rate'] = 100 - row['good-rate'] - row['bad-rate']
            table['bad-rate'] = row['bad-rate']
    table['all-num'] = all_num
    table['all-sales'] = all_sales
    table['all-fb-num'] = all_fb_num
    table['all-good-num'] = all_good_num
    table['all-normal-num'] = all_normal_num
    table['all-bad-num'] = all_bad_num
    table['all-good-rate'] = all_good_num*100.0/all_fb_num if all_fb_num !=0 else 0
    table['all-normal-rate'] = all_normal_num*100.0/all_fb_num if all_fb_num !=0 else 0
    table['all-bad-rate'] = all_bad_num*100.0/all_fb_num if all_fb_num !=0 else 0
    rows = one_diet_fb_cook(did, start, end)
    table['rows'] = rows
    return table

def one_diet_fb_cook(did, start, end):
    start = time.mktime(start.timetuple())
    end = time.mktime(end.timetuple())
    result = {}
    sql = 'select fid, fb, sum(num) as number from order_history, feedback, cook_history where order_history.uid = feedback.uid and order_history.uid = cook_history.uid and did = "%s" and cook_history.stamp > %s and cook_history.stamp < %s group by fid, fb' % (did, start, end)
    rows = mysql.query(sql)
    for row in rows:
        fid = row['fid']
        if row['fid'] not in result:
            result[fid] = {'fid': fid}
        if row['fb'] == -1:
            result[fid]['bad-num'] = row['number']
        elif row['fb'] == 0:
            result[fid]['normal-num'] = row['number']
        elif row['fb'] == 1:
            result[fid]['good-num'] = row['number']
    sql = 'select fid, sum(num) as number from order_history, cook_history where order_history.uid = cook_history.uid and order_history.did = "%s" and cook_history.stamp > %s and cook_history.stamp < %s group by fid' % (did, start, end)
    rows = mysql.query(sql)
    for row in rows:
        fid = row['fid']
        if fid not in result:
            result[fid] = {'fid': fid}
        result[fid]['num'] = row['number']
    cooks = []
    for k, v in logic.faculty.items():
        if v['role'].find('cook') >=0:
            cooks.append({'fid': k, 'name': v['name']})
    cook_result = []
    for cook in cooks:
        fid = cook['fid']
        if fid not in result:
            result[fid] = {}
        if 'fid' not in result[fid]:
            result[fid]['fid'] = fid
        if 'name' not in result[fid]:
            result[fid]['name'] = logic.faculty.get(fid)['name']
        if 'num' not in result[fid]:
            result[fid]['num'] = 0
        if 'bad-num' not in result[fid]:
            result[fid]['bad-num'] = 0
        if 'normal-num' not in result[fid]:
            result[fid]['normal-num'] = 0
        if 'good-num' not in result[fid]:
            result[fid]['good-num'] = 0
        if 'fb-num' not in result[fid]:
            result[fid]['fb-num'] = result[fid]['good-num'] + result[fid]['normal-num'] + result[fid]['bad-num']
        if result[fid]['fb-num'] == 0:
            result[fid]['good-rate'] = 0
            result[fid]['normal-rate'] = 0
            result[fid]['bad-rate'] = 0
        else:
            result[fid]['good-rate'] = result[fid]['good-num']*100.0/result[fid]['fb-num']
            result[fid]['normal-rate'] = result[fid]['normal-num']*100.0/result[fid]['fb-num']
            result[fid]['bad-rate'] = result[fid]['bad-num']*100.0/result[fid]['fb-num']
        cook_result.append(result[fid])
    cook_result.sort(key=lambda x: x['fid'])
    return cook_result
    
#day is datetime
def frequency(day, request=0, kitchen=0, cash=0):
    year = day.year
    month = day.month
    day = day.day
    
    pattern = '(\d+):(\d+)-(\d+):(\d+)'
    #print logic.info['time']
    m = re.match(pattern, logic.info['time'])
    h1 = int(m.group(1))
    m1 = int(m.group(2))
    h2 = int(m.group(3))
    m2 = int(m.group(4))

    start = datetime.datetime(year, month, day, h1, m1)
    end = datetime.datetime(year, month, day, h2, m2)

    nodes = time_nodes(start, end, interval='30m')

    t1 = time.mktime(start.timetuple())
    t2 = time.mktime(end.timetuple())

    intervals = []
    pos = 0
    while pos < len(nodes) -1:
        n1 = nodes[pos]
        n2 = nodes[pos+1]
        intervals.append((time.mktime(n1.timetuple()), time.mktime(n2.timetuple())))
        pos += 1

    result = []
    #for request
    if request == 1:
        sql = 'select * from request where stamp >= %s and stamp < %s' % (t1, t2)
        rows = mysql.query(sql)
        nums = []
        while len(nums) < len(intervals):
            nums.append(0)
        for row in rows:
            for span in intervals:
                if row['stamp'] >= span[0] and row['stamp'] < span[1]:
                    index = intervals.index(span)
                    nums[index] += 1
                    break
        t = []
        for index in range(len(intervals)):
            n1 = intervals[index][0]
            n2 = intervals[index][1]
            n1 = datetime.datetime.fromtimestamp(n1)
            n2 = datetime.datetime.fromtimestamp(n2)
            n1_str = n1.strftime('%H:%M')
            n2_str = n2.strftime('%H:%M')
            t.append({'from': n1_str, 'to': n2_str, 'num': nums[index]})
        table = {'type': 'request', 'rows': t}
        result.append(table)
    if kitchen == 1:
        sql = 'select num, cook_history.stamp from cook_history, order_history where cook_history.uid = order_history.uid and cook_history.stamp >= %s and cook_history.stamp < %s' % (t1, t2)
        rows = mysql.query(sql)
        
        nums = []
        while len(nums) < len(intervals):
            nums.append(0)
        for row in rows:
            for span in intervals:
                if row['stamp'] >= span[0] and row['stamp'] < span[1]:
                    index = intervals.index(span)
                    nums[index] += row['num']
                    break
        t = []
        for index in range(len(intervals)):
            n1 = intervals[index][0]
            n2 = intervals[index][1]
            n1 = datetime.datetime.fromtimestamp(n1)
            n2 = datetime.datetime.fromtimestamp(n2)
            n1_str = n1.strftime('%H:%M')
            n2_str = n2.strftime('%H:%M')
            t.append({'from': n1_str, 'to': n2_str, 'num': nums[index]})
        table = {'type': 'kitchen', 'rows': t}
        result.append(table)
    if cash == 1:
        sql = 'select max(stamp) as time from cash_history where stamp > %s and stamp < %s group by pid' % (t1, t2)
        rows = mysql.query(sql)
        nums = []
        while len(nums) < len(intervals):
            nums.append(0)
        for row in rows:
            for span in intervals:
                if row['time'] >= span[0] and row['time'] < span[1]:
                    index = intervals.index(span)
                    nums[index] += 1
                    break
        t = []
        for index in range(len(intervals)):
            n1 = intervals[index][0]
            n2 = intervals[index][1]
            n1 = datetime.datetime.fromtimestamp(n1)
            n2 = datetime.datetime.fromtimestamp(n2)
            n1_str = n1.strftime('%H:%M')
            n2_str = n2.strftime('%H:%M')
            t.append({'from': n1_str, 'to': n2_str, 'num': nums[index]})
        table = {'type': 'cash', 'rows': t}
        result.append(table)
    return result
