chmod +x cron_job.shcrontab -e#!/bin/bash
# ================================
# CRON JOB FOR CRYPTO TRACKER
# ================================

# Set working directory to the script's location
cd "$(dirname "$0")"

# Activate virtual environment if you use one
# source venv/bin/activate

# Run the data fetch function using Python
python3 << EOF
from app import app, fetch_all_data
with app.app_context():
    fetch_all_data()
EOF

# Log the execution time
echo "$(date): Crypto/Weather/News data updated successfully" >> cron_log.txt