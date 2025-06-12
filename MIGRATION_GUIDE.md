# Data Migration Guide: SQLite to Supabase PostgreSQL

This guide walks you through migrating your Elden Ring Challenges Website data from your local SQLite development database to your production Supabase PostgreSQL database.

## Overview

The migration process consists of three main steps:

1. **Export** data from your local SQLite database
2. **Setup** the production PostgreSQL database
3. **Verify** the migration was successful

## Prerequisites

Before starting the migration, ensure you have:

- [x] Local development database with data to migrate (`mybackend/db.sqlite3`)
- [x] Supabase PostgreSQL database configured
- [x] Environment variables set in `mybackend/.env.prod`
- [x] Python dependencies installed (`pip install -r requirements.txt`)
- [x] Network access to your Supabase database

## Migration Scripts

### 1. Export Script (`mybackend/scripts/export_dev_data.py`)

Exports data from your local SQLite database to JSON fixtures.

### 2. Setup Script (`mybackend/scripts/setup_production.py`)

Sets up the production database and imports the exported data.

### 3. Verification Script (`mybackend/scripts/verify_migration.py`)

Verifies that the migration was successful and data integrity is maintained.

## Step-by-Step Migration Process

### Step 1: Export Development Data

First, export your development data from SQLite:

```bash
cd mybackend
python scripts/export_dev_data.py
```

**What this does:**

- Creates a `data_exports/` directory
- Exports core data (categories, challenges, admin users, site settings)
- Exports optional data (regular users, submissions, forum data)
- Creates admin credentials file
- Generates migration summary

**Expected output:**

```
🚀 Starting data export from development database...
✅ Exported 8 Challenge_Category records to challenge_categories_20250602_105930.json
✅ Exported 156 Challenge records to challenges_20250602_105930.json
✅ Exported 1 SiteSettings records to site_settings_20250602_105930.json
✅ Admin credentials exported to admin_credentials_20250602_105930.json
✅ Migration summary created: migration_summary_20250602_105930.json
✅ Data export completed successfully!
```

### Step 2: Setup Production Database

Next, set up your production database and import the data:

```bash
cd mybackend
python scripts/setup_production.py
```

**What this does:**

- Tests connection to Supabase PostgreSQL
- Runs Django migrations to create tables
- Imports core data in correct dependency order
- Creates admin user for production
- Sets up site settings
- Verifies data integrity

**Expected output:**

```
🚀 Starting production database setup...
✅ Database connection successful
✅ Migrations completed successfully
✅ Imported 8 records, skipped 0 existing records from challenge_categories_20250602_105930.json
✅ Imported 156 records, skipped 0 existing records from challenges_20250602_105930.json
✅ Created new admin user: admin@eldenring.com
✅ Site settings already exist
✅ Data integrity verification passed
✅ Production setup completed!
```

### Step 3: Verify Migration

Finally, verify that the migration was successful:

```bash
cd mybackend
python scripts/verify_migration.py
```

**What this does:**

- Tests database connection
- Verifies all expected tables exist
- Checks data counts in core tables
- Validates foreign key relationships
- Tests admin functionality
- Verifies challenge data integrity
- Tests site settings configuration
- Generates verification report

**Expected output:**

```
🔍 Starting migration verification...
✅ Database connection successful
✅ All expected tables exist (16 tables)
✅ Data counts look good
✅ All foreign key relationships are valid
✅ Admin user 'admin@eldenring.com' is properly configured
✅ Challenge data integrity verified (156 challenges)
✅ Site settings configured
✅ ALL VERIFICATION TESTS PASSED!
🎉 Migration completed successfully!
```

## Data That Gets Migrated

### Core Data (Essential)

- **Challenge Categories**: All challenge categories (Boss Fights, Speedruns, etc.)
- **Challenges**: All challenge definitions with points, difficulty, descriptions
- **Admin Users**: Administrative user accounts (passwords need to be reset)
- **Site Settings**: Site configuration and settings

### Optional Data (If Present)

- **Regular Users**: Non-admin user accounts
- **Submissions**: Challenge submissions and their status
- **Forum Data**: Forum categories, discussion threads, comments
- **Notifications**: User notifications
- **Badges**: Badge definitions and user badge assignments

## Important Notes

### Admin Credentials

After migration, you'll have an admin user with these default credentials:

- **Email**: `admin@eldenring.com` (or from your development data)
- **Password**: `EldenRing123!`

**⚠️ IMPORTANT**: Change this password immediately after first login!

### Environment Variables

Ensure your `mybackend/.env.prod` file has the correct Supabase credentials:

```env
# Supabase PostgreSQL
DB_NAME=postgres
DB_USER=postgres.cfkixfqgkvixjodnbvlh
DB_PASSWORD=your_supabase_password
DB_HOST=aws-0-ca-central-1.pooler.supabase.com
DB_PORT=6543

# Other required settings
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Django Settings

The scripts use `mybackend.settings_supabase` by default. Make sure this settings file:

- Points to your Supabase database
- Has SSL enabled (`sslmode: require`)
- Uses the correct environment variables

## Troubleshooting

### Common Issues

#### 1. Database Connection Failed

```
❌ Database connection error: FATAL: password authentication failed
```

**Solution**: Check your database credentials in `.env.prod`

#### 2. Migration Failed

```
❌ Migration failed: relation "api_challenge" already exists
```

**Solution**: Your database already has tables. Either:

- Drop existing tables and re-run
- Use `--fake-initial` flag if this is expected

#### 3. Import Errors

```
❌ Error importing from challenges_20250602_105930.json
```

**Solution**: Check that:

- Categories were imported first (dependency order)
- JSON files are not corrupted
- Foreign key references are valid

#### 4. No Export Files Found

```
⚠️ No export files found. Running basic setup only.
```

**Solution**: Run the export script first, or check that `data_exports/` directory exists

### Manual Recovery

If something goes wrong, you can:

1. **Re-run export**: Safe to run multiple times
2. **Reset production DB**: Drop all tables and start over
3. **Import specific data**: Modify scripts to import only certain models
4. **Manual data entry**: Use Django admin to add missing data

## File Structure After Migration

```
mybackend/
├── scripts/
│   ├── export_dev_data.py          # Export script
│   ├── setup_production.py         # Setup script
│   └── verify_migration.py         # Verification script
├── data_exports/                   # Created during export
│   ├── challenge_categories_*.json
│   ├── challenges_*.json
│   ├── admin_credentials_*.json
│   ├── site_settings_*.json
│   └── migration_summary_*.json
└── migration_verification_report_*.json  # Created during verification
```

## Next Steps After Migration

1. **Test Admin Login**: Log in to Django admin with the provided credentials
2. **Change Admin Password**: Update the default password
3. **Test Website**: Verify that challenges load correctly
4. **Configure Production**: Update environment variables for production
5. **Set up Monitoring**: Implement logging and monitoring
6. **Backup Strategy**: Set up regular database backups

## Security Considerations

- Admin passwords are not migrated (for security)
- Sensitive data is excluded from exports
- All connections use SSL/TLS
- Environment variables keep credentials secure
- Verification logs help with audit trails

## Support

If you encounter issues:

1. Check the verification report for specific failures
2. Review Django logs for detailed error messages
3. Verify your Supabase database is accessible
4. Ensure all environment variables are correctly set
5. Test database connection manually using Django shell

The migration scripts are designed to be safe and can be run multiple times without causing data corruption.
