# Setup
## .env

### Allowed Domain
- ALLOWED_DOMAIN=https://domain.com (https://*.domain.com - for Subdomains)

### Database
- DB_NAME=TemplateDB
- DB_USER=username
- DB_PASSWORD=password
- DB_HOST=ip/host
- DB_PORT=port

Note: This is setup to use Postgres

### Email (SMTP)
- EMAIL_HOST=SMTPDomain
- EMAIL_USE_TLS=True/False
- EMAIL_PORT=PORT
- EMAIL_HOST_USER=EmailID
- EMAIL_HOST_PASSWORD=Password

### AWS S3
- AWS_ACCESS_KEY_ID=ID
- AWS_SECRET_ACCESS_KEY=Key
- AWS_STORAGE_BUCKET_NAME=BucketName
- AWS_S3_SIGNATURE_NAME=Signature (Default - s3v4),
- AWS_S3_REGION_NAME=Region
- AWS_S3_FILE_OVERWRITE=True/False
- AWS_DEFAULT_ACL=None/ACL
- AWS_S3_VERITY=True/False
