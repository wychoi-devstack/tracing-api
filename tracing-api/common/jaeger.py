from __future__ import annotations
from collections import defaultdict

import os
import re
import time
import uuid
import requests
import datetime
from typing import Optional, List

from fastapi import APIRouter, HTTPException, Request, Response, Header, Form, status

import schemas
from config import CONF

from constant import constants

from common.time import date2unix


async def get_error_traces() -> List[str]:
    try:
        now = datetime.datetime.now()
        end = await date2unix(now)
        start = await date2unix((now - datetime.timedelta(hours=int(CONF.jaeger.gap))))

        jaeger_url = CONF.jaeger.url
        service = CONF.jaeger.service_horizon
        res = requests.get('%s/api/traces?service=%s&tags={"error":"true"}&start=%s540000&end=%s540000' % (jaeger_url, service, start, end))

        errors = []
        t_len = len(res.json()["data"])
        for t in range(0, t_len):
            s_len = len(res.json()["data"][t]["spans"])
            for s in range(0, s_len):
                if res.json()["data"][t]["spans"][s]["tags"][4]["key"] == "error":
                    print(res.json()["data"][t]["spans"][s]["traceID"])
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
        now = datetime.datetime.now()
        end = await date2unix(now)
        start = await date2unix((now - datetime.timedelta(hours=int(CONF.jaeger.gap))))

        jaeger_url = CONF.jaeger.url
        service = CONF.jaeger.service_horizon
        res = requests.get('%s/api/traces?service=%s&tags={"error":"true"}&start=%s540000&end=%s540000' % (jaeger_url, service, start, end))

        errors = []
        t_len = len(res.json()["data"])
        for t in range(0, t_len):
            s_len = len(res.json()["data"][t]["spans"])
            for s in range(0, s_len):
                if res.json()["data"][t]["spans"][s]["tags"][4]["key"] == "error":
                    if "Floating IP" in res.json()["data"][t]["spans"][s]["logs"][0]["fields"][2]["value"]:
                        print(res.json()["data"][t]["spans"][s]["traceID"])
                        errors.append(res.json()["data"][t]["spans"][s]["traceID"])

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    else:
        return errors

async def get_quota_error_traces() -> List[str]:
    try:
        now = datetime.datetime.now()
        end = await date2unix(now)
        start = await date2unix((now - datetime.timedelta(hours=int(CONF.jaeger.gap)))) 

        jaeger_url = CONF.jaeger.url 
        service = CONF.jaeger.service_cinder
        res = requests.get('%s/api/traces?service=%s&tags={"error":"true"}&start=%s540000&end=%s540000' % (jaeger_url, service, start, end))

        errors = []
        t_len = len(res.json()["data"])
        for t in range(0, t_len):
            s_len = len(res.json()["data"][t]["spans"])
            for s in range(0, s_len):
                if res.json()["data"][t]["spans"][s]["tags"][4]["key"] == "error":
                    if "exceeds allowed gigabytes quota" in res.json()["data"][t]["spans"][s]["logs"][0]["fields"][2]["value"]:
                        print(res.json()["data"][t]["spans"][s]["traceID"])
                        errors.append(res.json()["data"][t]["spans"][s]["traceID"])

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    else:
        return errors
