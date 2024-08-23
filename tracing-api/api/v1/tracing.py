from __future__ import annotations

from pathlib import PurePath
from typing import Any, List, Optional, Tuple, Union

from fastapi import APIRouter, Depends, Form, Header, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse

from config import CONF

from common.jaeger import (
        get_error_traces,
        get_floating_ip_error_traces,
        get_solved_floating_ip_traces,
        get_quota_error_traces,
        get_solved_quota_traces,
        get_volume_detachment_error_traces, 
        get_solved_volume_detachment_traces,
        get_traces_json, 
)

from typing import List

import os
import schemas
import subprocess

router = APIRouter()

@router.get(
    "/traces/error",
    description="Get Error Tagged Traces",
    responses={
        200: {"model": List[str]},
        500: {"model": schemas.InternalServerErrorMessage},
    },
    response_model=List[str],
    status_code=status.HTTP_200_OK, 
    response_description="OK"
)
async def get_errors(
    request: Request,
    response: Response,
) -> List[str]:
    try: 
        res = await get_error_traces() 

    except Exception as e:
        code = status.HTTP_500_INTERNAL_SERVER_ERROR

        if '500' in str(e):
            e = "failed to get traces with error tag"

        return HTTPException(
            status_code=code,
            detail=str(e)
        )
    else: 
        return res

@router.get(
    "/traces/error/floating-ip",
    description="Get Floating IP Error Traces",
    responses={
        200: {"model": List[dict]},
        500: {"model": schemas.InternalServerErrorMessage},
    },
    response_model=List[dict],
    status_code=status.HTTP_200_OK,
    response_description="OK"
)
async def get_floating_ip_errors(
    request: Request,
    response: Response,
) -> List[dict]:
    try:
        ids = await get_floating_ip_error_traces()
        jsons = await get_traces_json(ids)

        res = []
        for i in range(0, len(ids)):
            res.append(jsons[i])

    except Exception as e:
        code = status.HTTP_500_INTERNAL_SERVER_ERROR

        if '500' in str(e):
            e = "failed to get traces with floating ip error tag"

        return HTTPException(
            status_code=code,
            detail=str(e)
        )
    else:
        return res

@router.get(
    "/traces/solved/floating-ip",
    description="Get Solved Floatin IP Error Traces",
    responses={
        200: {"model": List[dict]},
        500: {"model": schemas.InternalServerErrorMessage},
    },
    response_model=List[dict],
    status_code=status.HTTP_200_OK,
    response_description="OK"
)
async def get_solved_floating_ip_error(
    request: Request,
    response: Response,
) -> List[dict]:
    try:
        ids = await get_solved_floating_ip_traces()
        jsons = await get_traces_json(ids)
        
        res = []
        for i in range(0, len(ids)):
            res.append(jsons[i])

    except Exception as e:
        code = status.HTTP_500_INTERNAL_SERVER_ERROR

        if '500' in str(e):
            e = "failed to get traces with floating ip error tag"

        return HTTPException(
            status_code=code,
            detail=str(e)
        )
    else:
        return res

@router.get(
    "/traces/error/quota",
    description="Get Quota Error Traces",
    responses={
        200: {"model": List[dict]},
        500: {"model": schemas.InternalServerErrorMessage},
    },
    response_model=List[dict],
    status_code=status.HTTP_200_OK,
    response_description="OK"
)
async def get_quota_errors(
    request: Request,
    response: Response,
) -> List[dict]:
    try:
        ids = await get_quota_error_traces()
        jsons = await get_traces_json(ids)

        res = []
        for i in range(0, len(ids)):
            res.append(jsons[i])

    except Exception as e:
        code = status.HTTP_500_INTERNAL_SERVER_ERROR

        if '500' in str(e):
            e = "failed to get traces with floating ip error tag"

        return HTTPException(
            status_code=code,
            detail=str(e)
        )
    else:
        return res

@router.get(
    "/traces/solved/quota",
    description="Get Solved Quota Error Traces",
    responses={
        200: {"model": List[dict]},
        500: {"model": schemas.InternalServerErrorMessage},
    },
    response_model=List[dict],
    status_code=status.HTTP_200_OK,
    response_description="OK"
)
async def get_solved_quota_error(
    request: Request,
    response: Response,
) -> List[dict]:
    try:
        ids = await get_solved_quota_traces()
        jsons = await get_traces_json(ids)

        res = []
        for i in range(0, len(ids)):
            res.append(jsons[i])

    except Exception as e:
        code = status.HTTP_500_INTERNAL_SERVER_ERROR

        if '500' in str(e):
            e = "failed to get traces with floating ip error tag"

        return HTTPException(
            status_code=code,
            detail=str(e)
        )
    else:
        return res

@router.get(
    "/traces/error/volume",
    description="Get Root Device Volume Detachment Error Trace",
    responses={
        200: {"model": List[dict]},
        500: {"model": schemas.InternalServerErrorMessage},
    },
    response_model=List[dict],
    status_code=status.HTTP_200_OK,
    response_description="OK"
)
async def get_volume_detachment_error(
    request: Request, 
    response: Response, 
) -> List[dict]:
    try: 
        ids = await get_volume_detachment_error_traces()
        jsons = await get_traces_json(ids)

        res = []
        for i in range(0, len(ids)):
            res.append(jsons[i])

    except Exception as e:
        code = status.HTTP_500_INTERNAL_SERVER_ERROR

        if '500' in str(e):
            e = "failed to get traces with root device detachment error tag"

        return HTTPException(
            status_code=code,
            detail=str(e)
        )
    else:
        return res
    
@router.get(
    "/traces/solved/volume",
    description="Get Solved Root Device Volume Detachment Trace",
    responses={
        200: {"model": List[dict]},
        500: {"model": schemas.InternalServerErrorMessage},
    },
    response_model=List[dict],
    status_code=status.HTTP_200_OK,
    response_description="OK"
)
async def get_solved_volume_detachment_error(
    request: Request, 
    response: Response, 
) -> List[dict]:
    try:
        ids = await get_solved_volume_detachment_traces()
        jsons = await get_traces_json(ids)

        res = []
        for i in range(0, len(ids)):
            res.append(jsons[i])
    except Exception as e:
        code = status.HTTP_500_INTERNAL_SERVER_ERROR

        if '500' in str(e):
            e = "failed to get traces with solved root device detachment"

        return HTTPException(
            status_code=code,
            detail=str(e)
        )
    else:
        return res
