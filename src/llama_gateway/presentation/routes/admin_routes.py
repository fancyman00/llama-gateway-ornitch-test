from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from llama_gateway.application.dto.api_key import ApiKeyCreateRequest, ApiKeyCreateResponse, ApiKeyResponse
from llama_gateway.application.dto.employee import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from llama_gateway.application.service.api_key_service import ApiKeyService
from llama_gateway.application.service.employee_service import EmployeeService
from llama_gateway.infrastructure.database.sqlite import SQLiteDatabaseAdapter

router = APIRouter()


def _get_db(request: Request) -> SQLiteDatabaseAdapter:
    return request.app.state.db


def _get_employee_service(request: Request) -> EmployeeService:
    db = _get_db(request)
    return EmployeeService(db)


def _get_api_key_service(request: Request) -> ApiKeyService:
    db = _get_db(request)
    return ApiKeyService(db)


EmployeeServiceDep = Annotated[EmployeeService, Depends(_get_employee_service)]
ApiKeyServiceDep = Annotated[ApiKeyService, Depends(_get_api_key_service)]


@router.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee",
)
async def create_employee(
    dto: EmployeeCreate,
    service: EmployeeServiceDep,
) -> EmployeeResponse:
    employee = await service.create(dto)
    return EmployeeResponse.model_validate(employee)


@router.get(
    "/employees",
    response_model=list[EmployeeResponse],
    summary="List all employees",
)
async def list_employees(
    service: EmployeeServiceDep,
) -> list[EmployeeResponse]:
    employees = await service.list_all()
    return [EmployeeResponse.model_validate(e) for e in employees]


@router.get(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
    summary="Get employee by ID",
)
async def get_employee(
    employee_id: str,
    service: EmployeeServiceDep,
) -> EmployeeResponse:
    employee = await service.get(employee_id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return EmployeeResponse.model_validate(employee)


@router.patch(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
    summary="Update employee",
)
async def update_employee(
    employee_id: str,
    dto: EmployeeUpdate,
    service: EmployeeServiceDep,
) -> EmployeeResponse:
    updated = await service.update(employee_id, dto)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return EmployeeResponse.model_validate(updated)


@router.delete(
    "/employees/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete employee",
)
async def delete_employee(
    employee_id: str,
    service: EmployeeServiceDep,
) -> None:
    deleted = await service.delete(employee_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return None


@router.post(
    "/api-keys",
    response_model=ApiKeyCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new API key",
)
async def create_api_key(
    dto: ApiKeyCreateRequest,
    service: ApiKeyServiceDep,
) -> ApiKeyCreateResponse:
    api_key, raw_key = await service.create(dto)
    if api_key is None or raw_key is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee '{dto.employee_id}' not found",
        )
    assert api_key.employee_id is not None
    return ApiKeyCreateResponse(
        key=raw_key,
        key_id=api_key.id,
        employee_id=api_key.employee_id,
        key_prefix=api_key.key_prefix,
        created_at=api_key.created_at,
    )


@router.get(
    "/api-keys",
    response_model=list[ApiKeyResponse],
    summary="List API keys",
)
async def list_api_keys(
    service: ApiKeyServiceDep,
    employee_id: str | None = Query(default=None),
) -> list[ApiKeyResponse]:
    keys = await service.list_by_employee(employee_id)
    return [ApiKeyResponse.model_validate(k) for k in keys]


@router.get(
    "/api-keys/{key_id}",
    response_model=ApiKeyResponse,
    summary="Get API key by ID",
)
async def get_api_key(
    key_id: str,
    service: ApiKeyServiceDep,
) -> ApiKeyResponse:
    api_key = await service.get(key_id)
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found")
    return ApiKeyResponse.model_validate(api_key)


@router.patch(
    "/api-keys/{key_id}/revoke",
    response_model=ApiKeyResponse,
    summary="Revoke an API key",
)
async def revoke_api_key(
    key_id: str,
    service: ApiKeyServiceDep,
) -> ApiKeyResponse:
    api_key = await service.revoke(key_id)
    if api_key is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found")
    return ApiKeyResponse.model_validate(api_key)


@router.delete(
    "/api-keys/{key_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an API key",
)
async def delete_api_key(
    key_id: str,
    service: ApiKeyServiceDep,
) -> None:
    deleted = await service.delete(key_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found")
    return None
