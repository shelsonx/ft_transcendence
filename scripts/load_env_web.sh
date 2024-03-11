# script to export environment variables for web server
# Usage: source load_env_web.sh

set -a
source ../.env.web
set +a
echo "Environment variables for web server loaded"
