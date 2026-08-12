"""
QR Code Service

Generates QR codes for shortened URLs.
"""

from io import BytesIO

import qrcode


class QRCodeService:
    
    # Handles QR code generation.

    def generate(
        self,
        short_url: str,
    ) -> BytesIO:
        
        # Generate a QR code image for a short URL.

        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4,
        )

        qr.add_data(short_url)
        qr.make(fit=True)

        image = qr.make_image(
            fill_color="black",
            back_color="white",
        )

        buffer = BytesIO()

        image.save(
            buffer,
            format="PNG",
        )

        buffer.seek(0)

        return buffer