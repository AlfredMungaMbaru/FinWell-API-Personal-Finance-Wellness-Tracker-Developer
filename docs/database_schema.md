# Database Schema

## User
- id (AutoField, PK)
- username (CharField, unique)
- email (EmailField, unique)
- password (CharField)
- date_joined (DateTimeField)

## Category
- id (AutoField, PK)
- name (CharField)
- user (ForeignKey to User, nullable)
- type (CharField: income/expense)

## Transaction
- id (AutoField, PK)
- user (ForeignKey to User)
- category (ForeignKey to Category)
- amount (DecimalField)
- date (DateField)
- description (TextField, optional)

## Budget
- id (AutoField, PK)
- user (ForeignKey to User)
- category (ForeignKey to Category)
- amount (DecimalField)
- start_date (DateField)
- end_date (DateField)
