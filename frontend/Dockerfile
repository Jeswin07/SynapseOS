# -----------------------------
# Stage 1: Build React App
# -----------------------------
FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

RUN npm run build

# -----------------------------
# Stage 2: Production Image
# -----------------------------
FROM nginx:1.28-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx","-g","daemon off;"]