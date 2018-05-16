#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request
from service.service_app import get_configlist, insert_db, update_db, get_resultlist
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
import json

class Config(object):

    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='sqlite:///flask_context.db')
    }

    SCHEDULER_API_ENABLED = True


def my_job(a, b):
    print(str(a) + ' ' + str(b))


def pr():
    print('ok')


app = Flask(__name__)
app.config.from_object(Config)
scheduler = APScheduler()


@app.route('/addjob/', methods=['GET', 'POST'])
def ajob():
    try:
        scheduler.add_job(id='3', func=my_job, args=(1, 2), seconds=2, trigger='interval')
    except Exception as E:
        print(E)
        return
    return 'ok'


@app.route('/anomalyConfig/createSchedulerById')
def createschedulerbyid():
    get_data = {'id': '1'}
    scheduler.resume_job(id=get_data['id'])
    return scheduler.get_job(get_data['id'])


@app.route('/anomalyConfig/removeSchedulerById')
def removeschedulerbyid():
    get_data = {'id': '1'}
    scheduler.remove_job(id=get_data['id'])
    return scheduler.get_job(get_data['id'])


@app.route('/anomalyConfig/pauseSchedulerById')
def pauseschedulerbyid():

    scheduler.pause_job(id='3')
    print(scheduler.get_job(id='3'))
    return 'ok'


@app.route('/anomalyConfig/resumeSchedulerById')
def resumeschedulerbyid():

    scheduler.resume_job(id='1')
    print(scheduler.get_job(id='1'))
    return 'ok'


@app.route('/stop/', methods=['GET', 'POST'])
def stop():
    try:
        scheduler.shutdown()
        print(scheduler.state)
    except Exception as E:
        print(E)
        print(scheduler.state)
    return "ok"


@app.route('/start/', methods=['GET', 'POST'])
def start():
    try:
        scheduler.start(paused=True)
        print(scheduler.state)
    except Exception as E:
        print(E)
        print(scheduler.state)
    return 'Hello World!'


@app.route('/anomalyConfig/queryConfigLIst/')
def queryConfigLIst():
    """
    根据source, status获取ConfigLIst
    :return:
    """
    source = 'source1'
    status = '1'
    data = get_configlist(source, status)

    return json.dumps(data)


@app.route('/anomalyConfig/addConfig/')
def addconfig():
    get_data = {
        "source": "tesr",
        "timeUnit": "15S",
        "referenceValue": "1,2,3",
        "judgeRule": "[{\"level\":1,\"minusDiffer\":-1.0,\"minusDifferPercent\":-10.0,\"plusDiffer\":1.0,\"plusDifferPercent\":10.0},{\"level\":2,\"minusDiffer\":-2.0,\"minusDifferPercent\":-20.0,\"plusDiffer\":2.0,\"plusDifferPercent\":20.0},{\"level\":3,\"minusDiffer\":-3.0,\"minusDifferPercent\":-30.0,\"plusDiffer\":3.0,\"plusDifferPercent\":30.0}]\r\n",
    }
    return_data = insert_db(get_data)
    return return_data


@app.route('/anomalyConfig/updateConfig/')
def updateconfig():
    get_data = {
        'id': 23,
        "source": "33",
        "timeUnit": "10S",
        'cycle': 'null',
        "referenceValue": "1,2,3",
        "judgeRule": "[{\"level\":1,\"minusDiffer\":-1.0,\"minusDifferPercent\":-10.0,\"plusDiffer\":1.0,\"plusDifferPercent\":10.0},{\"level\":2,\"minusDiffer\":-2.0,\"minusDifferPercent\":-20.0,\"plusDiffer\":2.0,\"plusDifferPercent\":20.0},{\"level\":3,\"minusDiffer\":-3.0,\"minusDifferPercent\":-30.0,\"plusDiffer\":3.0,\"plusDifferPercent\":30.0}]\r\n",
        'status': 'INIT',
    }
    return_data = update_db(get_data)
    return return_data


@app.route('/anomalyConfig/addData')
def adddata():
    get_data = {'source': 'source1', 'value': 18}


@app.route('/anomalyConfig/queryResultList/')
def queryresultlist():
    return_data = get_resultlist()
    return return_data


if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run()
