FROM nginx:alpine

# Copy static files
COPY index.html /usr/share/nginx/html/index.html

# Copy and enable the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
