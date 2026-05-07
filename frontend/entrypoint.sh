#!/bin/sh
# Replace the __API_URL__ placeholder in index.html with the actual env var.
# On Railway: VITE_API_URL=https://your-backend.up.railway.app
# On DigitalOcean (docker-compose): VITE_API_URL is set in docker-compose.yml

API_URL="${VITE_API_URL:-}"

if [ -n "$API_URL" ]; then
  sed -i "s|__API_URL__|\"${API_URL}\"|g" /usr/share/nginx/html/index.html
else
  # No URL set — use relative /api path (works with nginx reverse proxy on DO)
  sed -i 's|typeof __API_URL__ !== "undefined" ? __API_URL__ : "/api"|"/api"|g' /usr/share/nginx/html/index.html
fi

# Ensure nginx listens on the port provided by the platform (Railway sets $PORT)
PORT=${PORT:-80}
if [ -f /nginx.conf.template ]; then
  sed "s|__PORT__|${PORT}|g" /nginx.conf.template > /etc/nginx/nginx.conf
fi

exec nginx -g 'daemon off;'
