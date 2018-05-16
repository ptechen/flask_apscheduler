#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dao.db_module import execute_getinfo, execute_into
import json


def get_configlist(source, status):
    table_name = 'anomaly_detection_config'
    if source == '' and status == '':
        sql = "select * from {}".format(table_name)
    else:
        sql = "select * from {} where source='{}' and status='{}'".format(table_name, source, status)

    data = execute_getinfo(sql)
    if isinstance(data, list) and data:
        data_dict = dict()
        data_dict['resultObj'] = data
        data_dict['msg'] = ''
        data_dict['success'] = True
        json.dumps(data_dict)
        return data_dict


def get_resultlist():
    table_name = 'anomaly_detection_result'
    sql = "select * from {}".format(table_name)
    data = execute_getinfo(sql)
    if isinstance(data, list) and data:
        data_dict = dict()
        data_dict['resultObj'] = data
        data_dict['msg'] = '查询成功'
        data_dict['success'] = True
        json.dumps(data_dict)
        return data_dict


def insert_db(data):
    """
    插入配置数据
    :param data: dict
    :return: json
    """
    if isinstance(data, dict):
        sql = create_insert_sql(table_name='anomaly_detection_config', data=data)
        return_data = execute_into(sql)
        return_data = json.dumps(return_data)
        return return_data


def update_db(data):
    """
    以id， source更新配置数据
    :param data: dict
    :return: json
    """
    if isinstance(data, dict):
        query_terms = "where id='{}' and source='{}'".format(data.pop('id'), data.pop('source'))
        sql = create_update_sql(table_name='anomaly_detection_config', data=data, query_terms=query_terms)
        return_data = execute_into(sql)
        return_data = json.dumps(return_data)
        return return_data


def create_update_sql(table_name, data, query_terms=None):
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


def create_insert_sql(table_name, data):
    """生成insert语句"""
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


if __name__ == '__main__':
    data = {
        'id': 12,
        "source": "tesr",
        "timeUnit": "10S",
        'cycle': None,
        "referenceValue": "1,2,3",
        "judgeRule": "[{\"level\":1,\"minusDiffer\":-1.0,\"minusDifferPercent\":-10.0,\"plusDiffer\":1.0,\"plusDifferPercent\":10.0},{\"level\":2,\"minusDiffer\":-2.0,\"minusDifferPercent\":-20.0,\"plusDiffer\":2.0,\"plusDifferPercent\":20.0},{\"level\":3,\"minusDiffer\":-3.0,\"minusDifferPercent\":-30.0,\"plusDiffer\":3.0,\"plusDifferPercent\":30.0}]\r\n",
        'status': 'INIT',
    }
    update_db(data)