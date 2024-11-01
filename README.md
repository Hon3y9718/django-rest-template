# Setup
## Create .env on Root

### Allowed Domain
- ALLOWED_DOMAIN=https://domain.com (https://*.domain.com - for Subdomains)

### Database
- DB_NAME=TemplateDB
- DB_USER=username
- DB_PASSWORD=password
- DB_HOST=ip/host
- DB_PORT=port

> Note: This is setup to use Postgres

### Email (SMTP)
- EMAIL_HOST=SMTPDomain
- EMAIL_USE_TLS=True/False
- EMAIL_PORT=PORT
- EMAIL_HOST_USER=EmailID
- EMAIL_HOST_PASSWORD=Password

> Note: SMTP Supported will extend to other options with helper functions.

### AWS S3
- AWS_ACCESS_KEY_ID=ID
- AWS_SECRET_ACCESS_KEY=Key
- AWS_STORAGE_BUCKET_NAME=BucketName
- AWS_S3_SIGNATURE_NAME=Signature (Default - s3v4),
- AWS_S3_REGION_NAME=Region
- AWS_S3_FILE_OVERWRITE=True/False
- AWS_DEFAULT_ACL=None/ACL
- AWS_S3_VERITY=True/False

> Note: Will expand to Azure/GCP as well

# Run

## Virtual Environment

1. Fork - <a href="https://github.com/Hon3y9718/django-rest-template/fork">Fork this repo</a>
2. Clone - ``` git clone repo-name ```
3. Setup Virtual Environment - ``` python3 -m venv virtualenvname ```
4. Install Requirements - ``` pip install -r requirements.txt ```
5. Run - ``` python manage.py runserver ```

> Note: This project will run on Daphne Server by default and have Websocket setup for ease.

## Docker Compose

1. Docker Compose - ``` docker-compose up --build ```
