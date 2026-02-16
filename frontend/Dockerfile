# Stage 1: Build React app
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve with nginx + envsubst for runtime config
FROM nginx:alpine

# Install envsubst (gettext)
RUN apk add --no-cache gettext

# Copy built assets
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx config as a template (envsubst will process it)
COPY nginx.conf /etc/nginx/templates/default.conf.template

# Defaults — Cloud Run overrides PORT, BACKEND_URL is set at deploy time
ENV PORT=8080
ENV BACKEND_URL=http://localhost:8000

# Remove default nginx config to avoid conflicts
RUN rm -f /etc/nginx/conf.d/default.conf

# Startup script: envsubst the template, then start nginx
RUN printf '#!/bin/sh\nset -e\nenvsubst "\$PORT \$BACKEND_URL" < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf\nnginx -g "daemon off;"\n' > /start.sh && chmod +x /start.sh

EXPOSE 8080

CMD ["/start.sh"]
