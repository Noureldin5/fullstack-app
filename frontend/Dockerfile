FROM nginx:alpine

# Copy static files
COPY index.html /usr/share/nginx/html/index.html

# Copy and enable the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copy the nginx template that will be populated at container start
COPY nginx.conf.template /nginx.conf.template

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
