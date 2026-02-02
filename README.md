# FodoMeter

Maak foto's van je maaltijden en ontvang een ingrediëntenlijst per e-mail, klaar om in te voeren in de [Eetmeter](https://mijn.voedingscentrum.nl/nl/eetmeter/).

## Hoe werkt het?

1. Open FodoMeter op je telefoon
2. Selecteer foto's van je maaltijden
3. Druk op **Analyseer en mail resultaten**
4. Je ontvangt een Excel-bestand per e-mail met per foto: ingrediënt, gewicht (g) en bereiding

## Installatie op Synology (Docker)

### 1. Configuratie

Kopieer `.env.example` naar `.env` en vul je gegevens in:

```bash
cp .env.example .env
```

| Variabele | Omschrijving |
|---|---|
| `OPENAI_API_KEY` | Je OpenAI API key |
| `SMTP_HOST` | SMTP server (bijv. `smtp.gmail.com`) |
| `SMTP_PORT` | SMTP poort (standaard `587`) |
| `SMTP_USER` | SMTP gebruikersnaam |
| `SMTP_PASSWORD` | SMTP wachtwoord / app-password |
| `MAIL_TO` | E-mailadres waar resultaten naartoe gaan |
| `MAIL_FROM` | Afzenderadres (optioneel, standaard = `SMTP_USER`) |

### 2. Starten

```bash
docker compose up -d --build
```

De app draait op poort **8099**. Open `http://<synology-ip>:8099` op je telefoon.

### 3. Stoppen

```bash
docker compose down
```

## Technologie

- Python / FastAPI
- OpenAI GPT-4o Vision
- openpyxl (Excel)
- aiosmtplib (e-mail)
