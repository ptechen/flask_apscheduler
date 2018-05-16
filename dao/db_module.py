#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import string
import datetime

import mysql.connector

config = {'host': '127.0.01',  # 默认127.0.0.1
          'user': 'root',
          'password': '',
          'port': 3306,  # 默认即为3306
          'database': 'yujing',
          'pool_size': 10,
          'charset': 'utf8',  # 默认即为utf8
          }


# 隐式的创建数据库连接池,conn.close()如果conn是直接新建的连接则它会被关闭，如果是从线程池中分配一个连接则会被归还给连接池

def get_conn():
    """返回mysql数据库连接"""
    flag = True
    conn = ""
    while flag:
        try:
            conn = mysql.connector.connect(**config)
            flag = False
        except Exception as E:
            print(E)
            flag = True
            time.sleep(3)
    return conn


def execute_getinfo(sql):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    ret = ()
    try:
        cursor.execute(sql)
        ret = cursor.fetchall()
    except Exception as e:
        conn.rollback()
    cursor.close()
    conn.close()
    return ret


def execute_select(sql):
    """
    查询无返回查询结果
    :param sql: sql语句
    :return:
    """
    conn = get_conn()
    cursor = conn.cursor()
    ret = ()
    try:
        ret = cursor.execute(sql)
    except Exception as e:
        conn.rollback()

    cursor.close()

    conn.close()
    return ret


def execute_into(sql):
    """
    更新or插入
    :param sql: sql语句
    :return:
    """
    conn = get_conn()
    message = {"success": True, 'msg': '新增成功', 'resultObj': True}
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
    except Exception as E:
        print(E)
        message = {"success": False, 'msg': '新增失败', 'resultObj': False}
        conn.rollback()
    conn.commit()
    cursor.close()
    conn.close()
    return message


def structure_sql(the_type, table_name, query_terms=None, args="*", **kwargs):
    """
    构造对数据库的添加，删除，修改 功能的sql语句。
    第一个参数是the_type，表示操作的类型：add,delete,edit
    第二个参数是要操作的表名。
    第三个参数是是查询的条件的sql语句部分，包括where order by等，
    例如：query_terms='where sn=123 and name like '%张%'order by create_date desc'
    **kwargs表示关键字参数，是user_info的表的列名和值组成的字典。例如：
    {"user_name":username,....,"user_password":user_password}
    """
    if the_type == "add":
        """生成insert语句"""
        data = kwargs
        print(data)
        sql = "insert into {}".format(table_name)
        keys = "("
        values = "values("
        for k, v in data.items():
            keys += "{},".format(k)
            values += "'{}',".format(v) if isinstance(v, str) else "{},".format(v)
        keys = keys.rstrip(",")
        values = values.rstrip(",")
        keys += ") "
        values += ")"
        sql += keys + values
        return sql
    elif the_type == 'edit':
        """生成update语句"""
        data = kwargs
        sql = "update {} set ".format(table_name)
        part = ""
        for k, v in data.items():
            part += "{0}={1},".format(k, "'{}'".format(v) if isinstance(v, str) else v)
        part = part.rstrip(",")
        if query_terms is None:
            raise ValueError("编辑时，筛选条件不能为空")
        else:
            # print(sql + part + " " + query_terms)
            return sql + part + " " + query_terms

    elif the_type == "delete":
        """生成delete语句"""
        sql = "delete from {0}".format(table_name)
        if query_terms is None:
            raise ValueError("删除时，筛选条件不能为空")
        else:
            return sql + query_terms
    elif the_type == "select":
        """生成select语句"""
        sql = "select {} from {}".format(args, table_name)
        if not query_terms:
            # print(sql)
            return sql
        print(sql + query_terms)
        return sql + query_terms
    else:
        raise KeyError("未知的操作类型")


def current_datetime(number=0):
    """获取当前的日期和时间，以字符串类型返回，格式为：2016-12-19 14:33:03
    number是指在当前日期上延后多少天，默认是0
    """
    now = datetime.datetime.now() + datetime.timedelta(days=number)
    return now.strftime("%Y-%m-%d %H:%M:%S")


def str_format(result, local=False):
    """对数据库查询的结果中的datetime和date对象进行格式化，第一个参数是查询的结果集，元组类型。
    第二个参数是是否用中文年月日表示。以list类型返回处理过的结果"""
    data = []
    if result is not None:
        for x in result:
            if isinstance(x, datetime.datetime):
                temp = x.strftime("%Y{}%m{}%d{} %H{}%M{}%S{}")
                if local:
                    temp = temp.format("年", "月", "日", "时", "分", "秒")
                else:
                    temp = temp.format("-", "-", "", ":", ":", "")
                data.append(temp)
            elif isinstance(x, datetime.date):
                temp = x.strftime("%Y{}%m{}%d{}")
                if local:
                    temp = temp.format("年", "月", "日")
                else:
                    temp = temp.format("-", "-", "")
                data.append(temp)
            else:
                data.append(x)
    else:
        pass
    return data


def validate_arg(arg, pop_char=None):
    """检测输入参数是否被注入攻击语句的方法
    arg 是待检测的参数。
    pop_char是语句中允许包含的常见攻击字符【!"#$%&'()*+,-./:;<=>?@[\]^_`{|}】
    比如一般用户名许可下划线，那这是的pop_char='_'
    return 合法的参数返回True
    """
    pattern = string.punctuation
    if arg is None:
        raise ValueError("参数不能为None")
        return False
    elif isinstance(arg, str):
        if pop_char is None:
            pass
        else:
            chars = set(pop_char)
            for x in chars:
                pattern = pattern.replace(x, "")
        return not set(str(arg)) & set(pattern)
    else:
        raise TypeError("参数必须是str对象,而不是{}".format(str(type(arg))))
        return False


def check_phone(phone):
    """检查手机号码的合法性，合法的手机返回True"""
    if phone is None:
        return False
    elif isinstance(phone, str) or isinstance(phone, int):
        phone = str(phone).strip()
        if len(phone) == 11 and phone.startswith("1"):
            return True
        else:
            return False
    else:
        return False
