from datetime import datetime
from email.message import EmailMessage

import aiosmtplib

from app.config import MAIL_FROM, MAIL_TO, SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_USER


async def send_results(excel_bytes: bytes, photo_count: int) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    msg = EmailMessage()
    msg["Subject"] = f"FodoMeter resultaten - {now}"
    msg["From"] = MAIL_FROM
    msg["To"] = MAIL_TO
    msg.set_content(
        f"Hoi!\n\n"
        f"Hierbij de ingrediëntenlijst van {photo_count} foto('s).\n"
        f"Open het Excel-bestand en voer de ingrediënten in de Eetmeter in.\n\n"
        f"Groet,\nFodoMeter"
    )

    filename = f"fodometer_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    msg.add_attachment(
        excel_bytes,
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename,
    )

    await aiosmtplib.send(
        msg,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USER,
        password=SMTP_PASSWORD,
        start_tls=True,
    )
