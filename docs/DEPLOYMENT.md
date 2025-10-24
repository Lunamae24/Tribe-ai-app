# Production Deployment Guide

This guide covers the complete process for deploying the Tribe AI Application to production.

## Pre-Deployment Checklist

### 1. Environment Setup

- [ ] Server/Cloud infrastructure provisioned
- [ ] Domain name configured and DNS pointing to server
- [ ] SSL/TLS certificates obtained (Let's Encrypt recommended)
- [ ] Firewall rules configured (allow 80, 443, deny all others)

### 2. Credentials and Secrets

- [ ] OpenAI API key obtained
- [ ] Anthropic API key obtained
- [ ] Strong SECRET_KEY generated (min 32 characters)
- [ ] Strong JWT_SECRET generated
- [ ] Database credentials configured
- [ ] Sentry DSN obtained (optional but recommended)

### 3. Database Setup

- [ ] PostgreSQL database created
- [ ] Database user with appropriate permissions created
- [ ] Database backup strategy implemented
- [ ] Redis instance configured

### 4. Security Configuration

- [ ] `.env` file created with production values (NEVER commit this)
- [ ] `APP_DEBUG` set to `false`
- [ ] `ALLOWED_ORIGINS` configured with actual domain(s)
- [ ] Rate limits configured appropriately
- [ ] Security headers verified in nginx.conf

## Deployment Methods

### Option 1: Docker Compose (Recommended for Single Server)

1. **Clone the repository**
   ```bash
   git clone https://github.com/Lunamae24/Tribe-ai-app.git
   cd Tribe-ai-app
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your production values
   ```

3. **Setup SSL certificates**
   ```bash
   mkdir -p nginx/ssl
   # Copy your SSL certificates:
   cp /path/to/cert.pem nginx/ssl/cert.pem
   cp /path/to/key.pem nginx/ssl/key.pem
   ```

4. **Deploy**
   ```bash
   chmod +x scripts/deploy.sh
   ./scripts/deploy.sh
   ```

5. **Verify deployment**
   ```bash
   curl https://yourdomain.com/health
   ```

### Option 2: Kubernetes

1. **Create namespace**
   ```bash
   kubectl create namespace tribe-ai
   ```

2. **Create secrets**
   ```bash
   kubectl create secret generic tribe-ai-secrets \
     --from-literal=openai-api-key=your_key \
     --from-literal=secret-key=your_secret \
     -n tribe-ai
   ```

3. **Deploy application**
   ```bash
   kubectl apply -f k8s/ -n tribe-ai
   ```

4. **Check status**
   ```bash
   kubectl get pods -n tribe-ai
   kubectl logs -f deployment/tribe-ai-app -n tribe-ai
   ```

### Option 3: Cloud Platform (AWS, GCP, Azure)

#### AWS Elastic Beanstalk
1. Install EB CLI
2. Run `eb init` and `eb create`
3. Configure environment variables in EB console
4. Deploy with `eb deploy`

#### Google Cloud Run
1. Build image: `gcloud builds submit --tag gcr.io/PROJECT_ID/tribe-ai`
2. Deploy: `gcloud run deploy --image gcr.io/PROJECT_ID/tribe-ai`
3. Configure secrets in Cloud Console

#### Azure Container Apps
1. Create container app
2. Configure container image
3. Set environment variables
4. Deploy

## Post-Deployment Tasks

### 1. Verification

- [ ] Health endpoint responding: `/health`
- [ ] API endpoints working: `/api/v1/ai/chat`
- [ ] SSL certificate valid
- [ ] Logs being generated properly
- [ ] Metrics being collected (if monitoring setup)

### 2. Monitoring Setup

- [ ] Configure Sentry for error tracking
- [ ] Setup uptime monitoring (UptimeRobot, Pingdom, etc.)
- [ ] Configure log aggregation (ELK, CloudWatch, etc.)
- [ ] Setup performance monitoring (New Relic, DataDog, etc.)

### 3. Backup Configuration

- [ ] Database automatic backups configured
- [ ] Backup retention policy set
- [ ] Test backup restoration process
- [ ] Document backup/restore procedures

### 4. Scaling Configuration

- [ ] Horizontal scaling rules defined
- [ ] Auto-scaling policies configured (if applicable)
- [ ] Load balancer configured (if multiple instances)
- [ ] CDN setup for static assets (if applicable)

## Maintenance

### Regular Updates

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose build
docker-compose down
docker-compose up -d
```

### Database Migrations

```bash
# If using Alembic
docker-compose exec app alembic upgrade head
```

### Viewing Logs

```bash
# Application logs
docker-compose logs -f app

# Nginx logs
docker-compose logs -f nginx

# All logs
docker-compose logs -f
```

### Rollback Procedure

```bash
# Revert to previous version
git checkout <previous-commit>
./scripts/deploy.sh
```

## Troubleshooting

### Application Won't Start

1. Check logs: `docker-compose logs app`
2. Verify environment variables are set correctly
3. Check database connectivity
4. Verify API keys are valid

### High Memory Usage

1. Check for memory leaks in logs
2. Adjust worker count in Dockerfile
3. Implement caching (Redis)
4. Scale horizontally

### Slow Response Times

1. Enable detailed health check: `/health/detailed`
2. Check database query performance
3. Implement caching
4. Review rate limiting settings

## Security Checklist

- [ ] All secrets in environment variables, not code
- [ ] HTTPS enforced (no HTTP traffic)
- [ ] Security headers configured
- [ ] Rate limiting active
- [ ] API keys rotated regularly
- [ ] Dependency updates automated (Dependabot)
- [ ] Regular security audits scheduled
- [ ] Backup encryption enabled
- [ ] Access logs monitored
- [ ] Intrusion detection configured

## Performance Optimization

### Recommended Production Settings

```env
# Workers based on CPU cores: 2-4 × number of cores
# Set in docker-compose or start script

# Database connection pooling
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=0

# Redis connection pooling
REDIS_MAX_CONNECTIONS=50

# Caching
CACHE_TTL=300
```

### Load Testing

Before going live, perform load testing:

```bash
# Install Apache Bench
apt-get install apache2-utils

# Test health endpoint
ab -n 1000 -c 10 https://yourdomain.com/health

# Test API endpoint
ab -n 100 -c 5 -T 'application/json' \
   -p request.json \
   https://yourdomain.com/api/v1/ai/chat
```

## Cost Optimization

1. **API Usage**: Monitor AI API costs closely
2. **Database**: Use read replicas for scaling reads
3. **Caching**: Implement Redis caching to reduce API calls
4. **Auto-scaling**: Scale down during off-peak hours
5. **Reserved Instances**: Use reserved instances for predictable workloads

## Compliance

- [ ] GDPR compliance verified (if applicable)
- [ ] Data retention policies implemented
- [ ] Privacy policy published
- [ ] Terms of service published
- [ ] User consent mechanisms implemented

## Support and Incident Response

### On-Call Procedures

1. **Incident Detection**: Monitoring alerts or user reports
2. **Initial Response**: Check health endpoints and logs
3. **Diagnosis**: Review error logs and metrics
4. **Resolution**: Apply fix or rollback
5. **Post-Mortem**: Document incident and prevention measures

### Contact Information

- **Technical Lead**: [Add contact]
- **DevOps Team**: [Add contact]
- **Emergency Contact**: [Add contact]

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Best Practices](https://wiki.postgresql.org/wiki/Don%27t_Do_This)
- [Nginx Configuration](https://nginx.org/en/docs/)
