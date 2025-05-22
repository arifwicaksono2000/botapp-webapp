#!/bin/bash

# Database config
DB_NAME="djbot"
DB_USER="root"
DB_HOST="127.0.0.1"
DB_PORT="3306"
MYSQL="/Applications/XAMPP/xamppfiles/bin/mysql"

# Path to virtualenv activate script
VENV_ACTIVATE="./djenv/bin/activate"

echo "🧨 Dropping and recreating MySQL database '$DB_NAME' using XAMPP..."
$MYSQL -u"$DB_USER" -h"$DB_HOST" -P"$DB_PORT" -e "DROP DATABASE IF EXISTS \`$DB_NAME\`; CREATE DATABASE \`$DB_NAME\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

echo "🧹 Cleaning all migration files..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# echo "🚀 Activating virtual environment..."
# source "$VENV_ACTIVATE" 

echo "⚙️ Running fresh migrations..."
python manage.py makemigrations
python manage.py migrate

echo "📦 Loading initial fixtures..."
python manage.py loaddata botcore/fixtures/initial_fixtures.json
python manage.py loaddata botcore/fixtures/milestone_fixture.json

echo "🔐 Resetting admin password..."
python manage.py shell <<EOF
from django.contrib.auth.models import User
user = User.objects.get(username='admin')
user.set_password('Admin123!')
user.save()
EOF

echo "✅ All done! Fresh database '$DB_NAME' is ready to go."