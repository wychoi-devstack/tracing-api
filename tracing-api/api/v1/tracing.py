from __future__ import annotations

from pathlib import PurePath
from typing import Any, List, Optional, Tuple, Union

from fastapi import APIRouter, Depends, Form, Header, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse

from config import CONF

from common.jaeger import (
        get_error_traces,
        get_floating_ip_error_traces,
        get_quota_error_traces,
)

from typing import List

import os
import schemas
import subprocess

router = APIRouter()

@router.get(
    "/traces/errors",
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
    "/traces/errors/floating-ip",
    description="Get Floating IP Error Traces",
    responses={
        200: {"model": List[str]},
        500: {"model": schemas.InternalServerErrorMessage},
    },
    response_model=List[str],
    status_code=status.HTTP_200_OK,
    response_description="OK"
)
async def get_floating_ip_errors(
    request: Request,
    response: Response,
) -> List[str]:
    try:
        res = await get_floating_ip_error_traces()

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
    "/traces/errors/quota",
    description="Get Quota IP Error Traces",
    responses={
        200: {"model": List[str]},
        500: {"model": schemas.InternalServerErrorMessage},
    },
    response_model=List[str],
    status_code=status.HTTP_200_OK,
    response_description="OK"
)
async def get_quota_errors(
    request: Request,
    response: Response,
) -> List[str]:
    try:
        res = await get_quota_error_traces()

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
