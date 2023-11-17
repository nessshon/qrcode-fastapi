import aiohttp
import base64


class QRCodeAPIError(Exception):
    """Custom exception class for QRCodeAPI errors."""


class QRCodeAPI:
    BASE_URL = "https://qrcode.ness.su"

    def __init__(self, base_url: str = None) -> None:
        self.base_url = base_url if base_url else self.BASE_URL

    async def _fetch(self, endpoint: str, params: dict = None) -> bytes:
        """
        Make an asynchronous HTTP GET request to the QR code API.

        :param endpoint: The API endpoint.
        :param params: Parameters to include in the request. Defaults to None.
        :return bytes: Response content in bytes.
        :raise QRCodeAPIError: If there is an error during the request or an unexpected error occurs.
        """
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/{endpoint}"
                async with session.get(url, params=params) as response:
                    await self._handle_response(response)
                    return await response.read()
        except Exception as e:
            raise QRCodeAPIError(e)

    @staticmethod
    async def _handle_response(response: aiohttp.ClientResponse) -> None:
        """
        Handle the response from the API.

        :param response: aiohttp.ClientResponse object.
        :raise QRCodeAPIError: If the response status is not 200.
        """
        if response.status != 200:
            response_data = await response.json()
            detail = response_data.get("detail", f"Unexpected error: {response.status}")
            raise QRCodeAPIError(detail)

    @staticmethod
    def encode_data(data: str) -> str:
        """
        Encode data using base64.

        :param data: The data to encode.
        :return: The base64 encoded data.
        :raise QRCodeAPIError: If there is an error during data encoding.
        """
        try:
            return base64.b64encode(data.encode('utf-8')).decode('utf-8')
        except Exception as e:
            raise QRCodeAPIError(f"Error encoding data: {e}")

    async def create(
            self,
            data: str,
            border: int = 3,
            box_size: int = 30,
            image_url: str = None,
            image_round: int = 50,
            image_padding: int = 10,
    ) -> bytes:
        """
        Generate a QR code.

        :param data: Data or base64 encoded data to be encoded in QR code.
        :param border: QR code border size (0 to 50). Defaults to 3.
        :param box_size: QR code box size (20 to 100). Defaults to 50.
        :param image_url: URL or base64 encoded URL of the image to be included in the QR code. Defaults to None.
        :param image_round: Radius for rounding corners of the optional image in the QR code.
        :param image_padding: Padding around the optional image in the QR code.
        :return bytes: Generated QR code image in bytes.
        :raise QRCodeAPIError: If there is an error during QR code generation or an unexpected error occurs.
        """
        try:
            params = {
                "data": data,
                "border": border,
                "box_size": box_size,
            }
            if image_url:
                params["image_url"] = image_url
                params["image_round"] = image_round
                params["image_padding"] = image_padding

            return await self._fetch("create", params=params)
        except Exception as e:
            raise QRCodeAPIError(e)
