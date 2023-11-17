# QRCodeAPI

[![PyPI](https://img.shields.io/pypi/v/qrcodeapi.svg)](https://pypi.python.org/pypi/qrcodeapi)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/downloads/release)

QRCodeAPI is a Python library designed to seamlessly interact with the QR code generation API
from [qrcode.ness.su](https://qrcode.ness.su). Leveraging FastAPI and aiohttp, it provides a convenient and asynchronous
experience for generating QR codes.

## Features

* **Simplicity**: Generate QR codes with a simple and intuitive interface.
* **Customization**: Fine-tune QR code parameters, including data encoding, border size, box size, and optional image
  inclusion.

## Installation

```bash
pip install qrcodeapi
```

## Usage

```python
import asyncio
from qrcodeapi import QRCodeAPI


async def main():
    # Create an instance of QRCodeAPI
    qrcode_api = QRCodeAPI()

    # Example: Generate a basic QR code and save it to a file
    data = "Hello, QR Code!"
    filename = "qrcode.png"
    qr_code_image = await qrcode_api.create(data)
    with open(filename, "wb") as f:
        f.write(qr_code_image)

    # Example: Generate a QR code with an image and save it to a file
    data_with_image = "Example Data"
    image_url = "https://example.com/logo.png"
    filename_with_image = "qrcode_with_image.png"
    qr_code_image_with_image = await qrcode_api.create(
        data_with_image,
        border=5,
        box_size=40,
        image_url=image_url,
        image_round=20,
        image_padding=5,
    )
    with open(filename_with_image, "wb") as f:
        f.write(qr_code_image_with_image)


if __name__ == '__main__':
    asyncio.run(main())
```

## Licensing

QRCodeAPI is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
