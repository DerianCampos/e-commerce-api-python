from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError, OperationalError

from src.app.composition.features.product_variants import (
    get_create_product_variant_use_case,
    get_delete_product_variant_use_case,
    get_get_product_variant_by_id_use_case,
    get_list_product_variants_use_case,
    get_update_product_variant_use_case,
)
from src.app.features.product_variant.application.dtos.product_variant_dto import (
    ProductVariantCreateRequest,
    ProductVariantResponse,
    ProductVariantUpdateRequest,
)
from src.app.features.product_variant.application.use_cases.create_product_variant import CreateProductVariantUseCase
from src.app.features.product_variant.application.use_cases.delete_product_variant import DeleteProductVariantUseCase
from src.app.features.product_variant.application.use_cases.get_product_variant_by_id import (
    GetProductVariantByIdUseCase,
)
from src.app.features.product_variant.application.use_cases.list_product_variants import ListProductVariantsUseCase
from src.app.features.product_variant.application.use_cases.update_product_variant import UpdateProductVariantUseCase
from src.app.features.product_variant.domain.exceptions.product_variant_exception import (
    ProductVariantDoesNotExistException,
)

router = APIRouter()


@router.get("/", response_model=List[ProductVariantResponse], status_code=status.HTTP_200_OK)
async def list_product_variants(
    limit: int = Query(None, ge=1),
    offset: int = Query(None, ge=0),
    use_case: ListProductVariantsUseCase = Depends(get_list_product_variants_use_case),
) -> List[ProductVariantResponse]:
    try:
        return await use_case.execute(limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{variant_id}", response_model=ProductVariantResponse, status_code=status.HTTP_200_OK)
async def get_product_variant_by_id(
    variant_id: str,
    use_case: GetProductVariantByIdUseCase = Depends(get_get_product_variant_by_id_use_case),
) -> ProductVariantResponse:
    try:
        return await use_case.execute(variant_id)
    except ProductVariantDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/", response_model=ProductVariantResponse, status_code=status.HTTP_201_CREATED)
async def create_product_variant(
    payload: ProductVariantCreateRequest,
    use_case: CreateProductVariantUseCase = Depends(get_create_product_variant_use_case),
) -> ProductVariantResponse:
    try:
        return await use_case.execute(payload)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="A product variant with this SKU already exists."
        )
    except OperationalError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/{variant_id}", response_model=ProductVariantResponse, status_code=status.HTTP_200_OK)
async def update_product_variant(
    variant_id: str,
    payload: ProductVariantUpdateRequest,
    use_case: UpdateProductVariantUseCase = Depends(get_update_product_variant_use_case),
) -> ProductVariantResponse:
    try:
        return await use_case.execute(variant_id, payload)
    except ProductVariantDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{variant_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_variant(
    variant_id: str,
    use_case: DeleteProductVariantUseCase = Depends(get_delete_product_variant_use_case),
) -> None:
    try:
        await use_case.execute(variant_id)
    except ProductVariantDoesNotExistException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
