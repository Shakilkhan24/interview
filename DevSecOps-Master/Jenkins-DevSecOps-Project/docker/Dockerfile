# Multi-stage Dockerfile for DevSecOps Application

# Stage 1: Build dependencies
FROM node:18-alpine AS builder

WORKDIR /app

# Install security updates
RUN apk update && \
    apk upgrade && \
    apk add --no-cache python3 make g++

# Copy package files
COPY package*.json ./
COPY requirements.txt* ./

# Install Node.js dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Install Python dependencies (if present)
RUN if [ -f requirements.txt ]; then \
        pip3 install --no-cache-dir -r requirements.txt; \
    fi

# Stage 2: Build application
FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build || echo "No build script found"

# Stage 3: Production
FROM node:18-alpine AS production

# Install security updates
RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
    dumb-init \
    curl \
    && rm -rf /var/cache/apk/*

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package*.json ./

# Copy built application
COPY --from=build /app/dist ./dist
COPY --from=build /app/app ./app

# Copy application files
COPY *.py* ./ 2>/dev/null || true
COPY *.js* ./ 2>/dev/null || true

# Change ownership
RUN chown -R nodejs:nodejs /app

# Switch to non-root user
USER nodejs

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})" || \
    curl -f http://localhost:3000/health || exit 1

# Expose port
EXPOSE 3000

# Use dumb-init for proper signal handling
ENTRYPOINT ["dumb-init", "--"]

# Start application
CMD ["node", "dist/index.js"] || ["python3", "app.py"] || ["npm", "start"]

