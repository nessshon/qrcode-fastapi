import base64
from contextlib import suppress

from fastapi import FastAPI, HTTPException
from fastapi.params import Param
from fastapi.responses import Response

from qrcode_generator import generate_qrcode

app = FastAPI(
    title="QR Code Generator API",
    description=(
        "API for generating QR codes with optional image inclusion. "
        "Supports both base64-encoded data and plain text."
    ),
    docs_url="/",
    version="0.0.1",
    openapi_tags=[
        {
            "name": "QRCode",
            "description": "Generate QR codes with optional image inclusion",
        },
    ],
)


@app.get(
    "/create",
    tags=["QRCode"],
    summary="Generate QR Code",
    response_description="Generated QR code image",
)
async def create_qrcode(
        data: str = Param(
            ...,
            description="Data or base64 encoded data to be encoded in QR code",
        ),
        border: int = Param(
            3,
            ge=0,
            le=50,
            description="QR code border size",
        ),
        box_size: int = Param(
            30,
            ge=20,
            le=100,
            description="QR code box size",
        ),
        image_url: str = Param(
            None,
            description="URL or base64 encoded URL of the image to be included in the QR code",
        ),
        image_round: int = Param(
            50,
            ge=0,
            le=100,
            description="Roundness of the image in the QR code",
        ),
        image_padding: int = Param(
            10,
            ge=0,
            le=100,
            description="Padding around the image in the QR code",
        )
) -> Response:
    """
    Endpoint to generate a QR code.

    Parameters:
    - **data**: Data or base64 encoded data to be encoded in QR code.
    - **image_url**: URL or base64 encoded URL of the image to be included in the QR code.
    - **border**: QR code border size (0 to 50).
    - **box_size**: QR code box size (20 to 100).

    Returns:
    - **Response**: Generated QR code image in PNG format.

    Raises:
    - **HTTPException 500**: If an error occurs during QR code generation.
    """
    try:
        # Attempt to decode data and image_url from base64, suppress exceptions if they occur
        with suppress(Exception):
            data = base64.b64decode(data).decode('utf-8')
        if image_url:
            with suppress(Exception):
                image_url = base64.b64decode(image_url).decode('utf-8')

        # Call the generate_qrcode function to create the QR code image
        image = await generate_qrcode(data, border, box_size, image_url, image_padding, image_round)
        return Response(content=image, media_type="image/png")

    except Exception as e:
        # Raise an HTTPException with a 500 status code and the error details
        raise HTTPException(status_code=500, detail=str(e))
