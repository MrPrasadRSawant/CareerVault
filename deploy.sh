#!/usr/bin/env bash
# Deploy CareerVault from a checked-out production repository.
# Run as root: sudo bash deploy.sh

set -Eeuo pipefail

APP_DIR="${APP_DIR:-/var/www/CareerVault/Dev}"
SERVICE_NAME="${SERVICE_NAME:-careervault.service}"
NGINX_SITE_NAME="${NGINX_SITE_NAME:-careervault}"
BACKEND_DIR="$APP_DIR/backend"
FRONTEND_DIR="$APP_DIR/frontend"
NGINX_AVAILABLE="/etc/nginx/sites-available/$NGINX_SITE_NAME"
NGINX_ENABLED="/etc/nginx/sites-enabled/$NGINX_SITE_NAME"

fail() {
  echo "Deployment failed: $*" >&2
  exit 1
}

[[ "${EUID}" -eq 0 ]] || fail "run this script with sudo or as root"
[[ -d "$APP_DIR/.git" ]] || fail "not a Git checkout: $APP_DIR"
[[ -f "$BACKEND_DIR/.venv/bin/python" ]] || fail "virtual environment missing: $BACKEND_DIR/.venv"
[[ -f "$BACKEND_DIR/.env" ]] || fail "production environment file missing: $BACKEND_DIR/.env"
command -v git >/dev/null || fail "git is not installed"
command -v npm >/dev/null || fail "npm is not installed"
command -v nginx >/dev/null || fail "nginx is not installed"
command -v curl >/dev/null || fail "curl is not installed"

echo "==> Updating source"
git -C "$APP_DIR" fetch --prune origin
git -C "$APP_DIR" pull --ff-only origin main

echo "==> Installing backend dependencies"
"$BACKEND_DIR/.venv/bin/python" -m pip install --upgrade pip
"$BACKEND_DIR/.venv/bin/python" -m pip install -r "$BACKEND_DIR/requirements.txt"

echo "==> Applying database migrations"
(
  cd "$BACKEND_DIR"
  "$BACKEND_DIR/.venv/bin/alembic" upgrade head
)

echo "==> Building frontend"
(
  cd "$FRONTEND_DIR"
  npx quasar build
)

echo "==> Installing service and Nginx configuration"
install -m 0644 "$APP_DIR/careervault.service" "/etc/systemd/system/$SERVICE_NAME"
install -m 0644 "$APP_DIR/nginx.conf" "$NGINX_AVAILABLE"
ln -sfn "$NGINX_AVAILABLE" "$NGINX_ENABLED"

systemctl daemon-reload
nginx -t
systemctl enable "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"
systemctl reload nginx

echo "==> Checking application health"
sleep 2
systemctl --no-pager --full status "$SERVICE_NAME"
curl --fail --silent --show-error http://127.0.0.1:8004/api/v1/health >/dev/null

echo "Deployment completed successfully."
