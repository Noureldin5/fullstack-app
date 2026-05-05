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

exec nginx -g 'daemon off;'
