from __future__ import annotations
from collections import defaultdict

import os
import re
import time
import uuid
import requests
import datetime
from pytz import timezone
from typing import Optional, List

from fastapi import APIRouter, HTTPException, Request, Response, Header, Form, status

import schemas
from config import CONF

from constant import constants

from common.time import date2unix


async def get_error_traces() -> List[str]:
    try:
        now = datetime.datetime.now(timezone('Asia/Seoul'))
        end = await date2unix(now)
        start = await date2unix((now - datetime.timedelta(hours=int(CONF.jaeger.gap))))

        jaeger_url = CONF.jaeger.url
        service = CONF.jaeger.service_horizon
        microsec = now.microsecond
        if len(str(now.microsecond)) < 6:
            microsec = int(str(now.microsecond).zfill(6))
        res = requests.get('%s/api/traces?service=%s&tags={"error":"true"}&start=%s%s&end=%s%s' % (jaeger_url, service, start, microsec, end, microsec))

        errors = []
        t_len = len(res.json()["data"])
        for t in range(0, t_len):
            s_len = len(res.json()["data"][t]["spans"])
            for s in range(0, s_len):
                if res.json()["data"][t]["spans"][s]["tags"][4]["key"] == "error":
                    errors.append(res.json()["data"][t]["spans"][s]["traceID"])

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    else:
        return errors

async def get_floating_ip_error_traces() -> List[str]:
    try:
        now = datetime.datetime.now(timezone('Asia/Seoul'))
        end = await date2unix(now)
        start = await date2unix((now - datetime.timedelta(hours=int(CONF.jaeger.gap))))

        jaeger_url = CONF.jaeger.url
        service = CONF.jaeger.service_horizon
        microsec = now.microsecond
        if len(str(now.microsecond)) < 6:
            microsec = int(str(now.microsecond).zfill(6))
        res = requests.get('%s/api/traces?service=%s&tags={"error":"true"}&start=%s%s&end=%s%s' % (jaeger_url, service, start, microsec, end, microsec))

        errors = []
        t_len = len(res.json()["data"])
        for t in range(0, t_len):
            s_len = len(res.json()["data"][t]["spans"])
            for s in range(0, s_len):
                if res.json()["data"][t]["spans"][s]["tags"][4]["key"] == "error":
                    if "Floating IP" in res.json()["data"][t]["spans"][s]["logs"][0]["fields"][2]["value"]:
                        errors.append(res.json()["data"][t]["spans"][s]["traceID"])

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    else:
        return errors


async def get_solved_floating_ip_traces() -> List[str]:
    try:
        now = datetime.datetime.now(timezone('Asia/Seoul'))
        end = await date2unix(now)
        start = await date2unix((now - datetime.timedelta(hours=5)))

        jaeger_url = CONF.jaeger.url
        service = CONF.jaeger.service_neutron
        microsec = now.microsecond
        if len(str(now.microsecond)) < 6:
            microsec = int(str(now.microsecond).zfill(6))
        res = requests.get('%s/api/traces?service=%s&start=%s%s&end=%s%s' % (jaeger_url, service, start, microsec, end, microsec))

        solved = []
        t_len = len(res.json()["data"])
        for t in range(0, t_len):
            if not res.json()["data"][t]["spans"][0]["operationName"] == "openstack_dashboard.api.neutron.li":
                continue;
            s_len = len(res.json()["data"][t]["spans"])
            for s in range(0, s_len):
                if res.json()["data"][t]["spans"][s]["operationName"] == "openstack_dashboard.api.neutron.associate" and res.json()["data"][t]["spans"][s]["tags"][4]["key"] == "span.kind":
                    solved.append(res.json()["data"][t]["spans"][s]["traceID"])

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    else:
        return solved


async def get_quota_error_traces() -> List[str]:
    try:
        now = datetime.datetime.now(timezone('Asia/Seoul'))
        end = await date2unix(now)
        start = await date2unix((now - datetime.timedelta(hours=int(CONF.jaeger.gap)))) 

        jaeger_url = CONF.jaeger.url 
        service = CONF.jaeger.service_horizon
        microsec = now.microsecond
        if len(str(now.microsecond)) < 6:
            microsec = int(str(now.microsecond).zfill(6))
        res = requests.get('%s/api/traces?service=%s&tags={"error":"true"}&start=%s%s&end=%s%s' % (jaeger_url, service, start, microsec, end, microsec))

        errors = []
        t_len = len(res.json()["data"])
        for t in range(0, t_len):
            s_len = len(res.json()["data"][t]["spans"])
            for s in range(0, s_len):
                if res.json()["data"][t]["spans"][s]["tags"][4]["key"] == "error":
                    if "exceeds allowed gigabytes quota" in res.json()["data"][t]["spans"][s]["logs"][0]["fields"][2]["value"]:
                        errors.append(res.json()["data"][t]["spans"][s]["traceID"])
                    if "Maximum number of volumes" in res.json()["data"][t]["spans"][s]["logs"][0]["fields"][2]["value"]:
                        errors.append(res.json()["data"][t]["spans"][s]["traceID"])

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    else:
        return errors

async def get_solved_quota_traces() -> List[str]:
    try:
        now = datetime.datetime.now(timezone('Asia/Seoul'))
        end = await date2unix(now)
        start = await date2unix((now - datetime.timedelta(hours=5)))

        jaeger_url = CONF.jaeger.url
        service = CONF.jaeger.service_cinder
        microsec = now.microsecond
        if len(str(now.microsecond)) < 6:
            microsec = int(str(now.microsecond).zfill(6))
        res = requests.get('%s/api/traces?service=%s&start=%s%s&end=%s%s' % (jaeger_url, service, start, microsec, end, microsec))

        solved = []
        t_len = len(res.json()["data"])
        for t in range(0, t_len):
            s_len = len(res.json()["data"][t]["spans"])
            if not (res.json()["data"][t]["spans"][0]["operationName"] == "openstack_dashboard.api.cinder.volume_list_paged"):
                continue;
            for s in range(0, s_len):
                if "WSGI_POST_/v3/87bd44da47334afb8c610c12c8b17aab/backups/" in res.json()["data"][t]["spans"][s]["operationName"] and res.json()["data"][t]["spans"][s]["tags"][4]["key"] == "span.kind":
                    solved.append(res.json()["data"][t]["spans"][s]["traceID"])

#            if not (res.json()["data"][t]["spans"][0]["operationName"] == "openstack_dashboard.api.nova.server_create" and instance_name in res.json()["data"][t]["spans"][0]["tags"][1]["value"]):
#                continue;
#            for s in range(0, s_len):
#                if res.json()["data"][t]["spans"][s]["operationName"] == "WSGI_POST_/v3/87bd44da47334afb8c610c12c8b17aab/attachments" and res.json()["data"][t]["spans"][s]["tags"][4]["key"] == "span.kind":
#                    solved.append(res.json()["data"][t]["spans"][s]["traceID"])

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    else:
        return solved

async def get_volume_detachment_error_traces() -> List[dict]:
    try:
        now = datetime.datetime.now(timezone('Asia/Seoul'))
        end = await date2unix(now)
        start = await date2unix((now - datetime.timedelta(hours=int(CONF.jaeger.gap))))

        jaeger_url = CONF.jaeger.url
        service = CONF.jaeger.service_horizon
        microsec = now.microsecond 
        if len(str(now.microsecond)) < 6:
            microsec = int(str(now.microsecond).zfill(6))
        res = requests.get('%s/api/traces?service=%s&tags={"error":"true"}&start=%s%s&end=%s%s' % (jaeger_url, service, start, microsec, end, microsec))

        errors = []
        t_len = len(res.json()["data"])
        for t in range(0, t_len):
            s_len = len(res.json()["data"][t]["spans"])
            for s in range(0, s_len):
                if res.json()["data"][t]["spans"][s]["tags"][4]["key"] == "error":
                    if "Cannot detach a root device volume" in res.json()["data"][t]["spans"][s]["logs"][0]["fields"][2]["value"]:
                        errors.append(res.json()["data"][t]["spans"][s]["traceID"])

        print(start, microsec)
        print(end)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    else:
        return errors

async def get_solved_volume_detachment_traces() -> List[dict]:
    try:
        now = datetime.datetime.now(timezone('Asia/Seoul'))
        end = await date2unix(now)
        start = await date2unix((now - datetime.timedelta(hours=4)))

        jaeger_url = CONF.jaeger.url
        service = CONF.jaeger.service_cinder
        microsec = now.microsecond
        if len(str(now.microsecond)) < 6:
            microsec = int(str(now.microsecond).zfill(6))
        res = requests.get('%s/api/traces?service=%s&start=%s%s&end=%s%s' % (jaeger_url, service, start, microsec, end, microsec))

        solved = []
        t_len = len(res.json()["data"])
        for t in range(0, t_len):
            s_len = len(res.json()["data"][t]["spans"])
            if not (res.json()["data"][t]["spans"][0]["operationName"] == "openstack_dashboard.api.cinder.volume_list_paged"):
                continue;
            for s in range(0, s_len):
                if "WSGI_POST_/v2.1/87bd44da47334afb8c610c12c8b17aab/servers/" and "/os-volume_attachments" in res.json()["data"][t]["spans"][s]["operationName"] and res.json()["data"][t]["spans"][s]["tags"][4]["key"] == "span.kind":
                    solved.append(res.json()["data"][t]["spans"][s]["traceID"])

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    else:
        return solved

async def get_traces_json(trace_ids) -> List[dict]:
    try:
        traces = []
        jaeger_url = CONF.jaeger.url

        for t_id in trace_ids:
            res = requests.get("%s/api/traces/%s" % (jaeger_url, t_id))
            traces.append(res.json())   

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    else:
        return traces
