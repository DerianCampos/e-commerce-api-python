import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.config.app_config import AppConfig
from src.app.features.band.presentation.band_routes import router as band_router
from src.app.features.product.presentation.product_routes import router as product_router
from src.app.features.product_variant.presentation.product_variant_routes import router as product_variant_router
from src.app.features.t_shirt_size.presentation.t_shirt_size_routes import router as t_shirt_size_router
from src.app.features.user.presentation.user_routes import router as user_router

ENV = os.getenv("APP_ENV", "local")

config = AppConfig.instance()
app_name = config.get_config("app.name")
app_version = config.get_config("app.version")

fastapi_app = FastAPI(title=app_name, version=app_version)

if ENV not in ("local", "container"):
    fastapi_app.docs_url = None
    fastapi_app.redoc_url = None
    fastapi_app.openapi_url = None

# --- CORS Origins from config ---
origins = ["http://localhost:8080"]

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@fastapi_app.get("/")
def read_root():
    return {"message": "Welcome to the E-Commerce API"}


@fastapi_app.get("/health")
def get_health_check():
    return "Ok"


fastapi_app.include_router(user_router, prefix="/api/v1/user", tags=["User"])
fastapi_app.include_router(band_router, prefix="/api/v1/bands", tags=["Band"])
fastapi_app.include_router(product_router, prefix="/api/v1/products", tags=["Product"])
fastapi_app.include_router(t_shirt_size_router, prefix="/api/v1/sizes", tags=["T-Shirt Size"])
fastapi_app.include_router(product_variant_router, prefix="/api/v1/variants", tags=["Product Variant"])
