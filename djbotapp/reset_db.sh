#!/bin/bash

# Database config
DB_NAME="djbot"
DB_USER="root"
DB_HOST="127.0.0.1"
DB_PORT="3306"

# Detect platform and set MySQL path accordingly
if [[ "$OSTYPE" == "darwin"* ]]; then
    MYSQL="/Applications/XAMPP/xamppfiles/bin/mysql"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    MYSQL="/c/xampp/mysql/bin/mysql.exe"
else
    MYSQL="mysql"  # Fallback for Linux or unknown
fi

# Path to virtualenv activate script (optional)
echo "🚀 Activating virtual environment..."
# --- FIX START ---
# Go up one directory to find djenv
CURRENT_DIR=$(pwd)
cd ..
VENV_PATH="djenv"

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash, WSL, or Cygwin)
    source "$VENV_PATH/Scripts/activate"
else
    # macOS/Linux
    source "$VENV_PATH/bin/activate"
fi

# Return to the original directory where manage.py is
cd "$CURRENT_DIR"
# --- FIX END ---

echo "🧨 Dropping and recreating MySQL database '$DB_NAME' using MySQL from: $MYSQL"
"$MYSQL" -u"$DB_USER" -h"$DB_HOST" -P"$DB_PORT" -e "DROP DATABASE IF EXISTS \`$DB_NAME\`; CREATE DATABASE \`$DB_NAME\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

echo "🧹 Cleaning all migration files..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

echo "⚙️ Running fresh migrations..."
python manage.py makemigrations botcore
python manage.py migrate

echo "📦 Loading initial fixtures..."
python manage.py loaddata botcore/fixtures/initial_fixtures.json
python manage.py loaddata botcore/fixtures/milestone_fixture.json

# Note: Ensure datetime fields in fixture use timezone-aware strings (e.g. ending in 'Z')

echo "🔐 Resetting admin password..."
python manage.py shell -c "
from django.contrib.auth.models import User
user = User.objects.get(username='admin')
user.set_password('Admin123!')
user.save()
print('✔️ Admin password reset completed.')
"

echo "✅ All done! Fresh database '$DB_NAME' is ready to go."