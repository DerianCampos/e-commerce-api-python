from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError, OperationalError

from src.app.composition.features.products import (
    get_create_product_use_case,
    get_delete_product_use_case,
    get_get_product_by_id_use_case,
    get_list_products_use_case,
    get_update_product_use_case,
)
from src.app.features.product.application.dtos.product_dto import (
    ProductCreateRequest,
    ProductResponse,
    ProductUpdateRequest,
)
from src.app.features.product.application.use_cases.create_product import CreateProductUseCase
from src.app.features.product.application.use_cases.delete_product import DeleteProductUseCase
from src.app.features.product.application.use_cases.get_product_by_id import GetProductByIdUseCase
from src.app.features.product.application.use_cases.list_products import ListProductsUseCase
from src.app.features.product.application.use_cases.update_product import UpdateProductUseCase
from src.app.features.product.domain.exceptions.product_exception import ProductDoesNotExistException

router = APIRouter()


@router.get("/", response_model=List[ProductResponse], status_code=status.HTTP_200_OK)
async def list_products(
    limit: Optional[int] = Query(None, ge=1),
    offset: Optional[int] = Query(None, ge=0),
    use_case: ListProductsUseCase = Depends(get_list_products_use_case),
) -> List[ProductResponse]:
    try:
        return await use_case.execute(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def get_product_by_id(
    product_id: str,
    use_case: GetProductByIdUseCase = Depends(get_get_product_by_id_use_case),
) -> ProductResponse:
    try:
        return await use_case.execute(product_id)
    except ProductDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    payload: ProductCreateRequest,
    use_case: CreateProductUseCase = Depends(get_create_product_use_case),
) -> ProductResponse:
    try:
        return await use_case.execute(payload)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="A product with this name already exists.")
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def update_product(
    product_id: str,
    payload: ProductUpdateRequest,
    use_case: UpdateProductUseCase = Depends(get_update_product_use_case),
) -> ProductResponse:
    try:
        return await use_case.execute(product_id, payload)
    except ProductDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    use_case: DeleteProductUseCase = Depends(get_delete_product_use_case),
) -> None:
    try:
        await use_case.execute(product_id)
    except ProductDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
