# Frontend image for the AI-First CRM HCP UI (#63)
#
# Stage 1 builds the React app with Vite.
# Stage 2 serves the static files with nginx (no Node.js at runtime).
#
# Build:  docker build -t ai-first-crm-frontend ./frontend
#         docker build --build-arg VITE_API_URL=http://localhost:8000 -t ai-first-crm-frontend ./frontend
# Run:    docker run --rm -p 8080:80 ai-first-crm-frontend

# ---------- Stage 1: build ----------
FROM node:22-alpine AS build

WORKDIR /app

# Install dependencies first so this layer is cached
# when only source files change.
COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# Vite embeds VITE_* variables at build time.
# This is the backend URL as seen from the user's browser.
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=${VITE_API_URL}

RUN npm run build

# ---------- Stage 2: serve ----------
FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q -O /dev/null http://127.0.0.1/health || exit 1
