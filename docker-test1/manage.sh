#!/bin/bash
# MemOS Instance Management Script
# Manages docker-test1 instance lifecycle

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTANCE_NAME="test1"

cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

case "${1:-}" in
    start)
        log_info "Starting MemOS $INSTANCE_NAME instance..."
        docker-compose up -d
        log_info "Waiting for services to be healthy..."
        sleep 10
        docker-compose ps
        log_info "Instance started! API available at http://localhost:8001"
        log_info "Neo4j browser at http://localhost:7475 (neo4j/memospassword123)"
        log_info "Qdrant at http://localhost:6334"
        ;;

    stop)
        log_info "Stopping MemOS $INSTANCE_NAME instance..."
        docker-compose stop
        log_info "Instance stopped"
        ;;

    restart)
        log_info "Restarting MemOS $INSTANCE_NAME instance..."
        docker-compose restart
        log_info "Instance restarted"
        ;;

    down)
        log_warn "Stopping and removing containers for $INSTANCE_NAME..."
        docker-compose down
        log_info "Containers removed (data preserved)"
        ;;

    clean)
        log_warn "This will remove all data for $INSTANCE_NAME instance!"
        read -p "Are you sure? (yes/no): " -r
        if [[ $REPLY == "yes" ]]; then
            log_warn "Stopping containers..."
            docker-compose down -v
            log_warn "Removing data directories..."
            rm -rf data/neo4j data/qdrant data/memos data/hf-cache logs/*
            log_info "Instance cleaned"
        else
            log_info "Clean cancelled"
        fi
        ;;

    logs)
        docker-compose logs -f "${2:-memos-api}"
        ;;

    status)
        log_info "Status of $INSTANCE_NAME instance:"
        docker-compose ps
        echo ""
        log_info "Health checks:"
        docker-compose ps --format json | jq -r '.[] | "\(.Name): \(.Health)"' 2>/dev/null || docker-compose ps
        ;;

    shell)
        SERVICE="${2:-memos-api}"
        log_info "Opening shell in $SERVICE..."
        docker-compose exec "$SERVICE" /bin/bash
        ;;

    test-api)
        log_info "Testing API endpoints..."
        echo ""
        echo "1. Health check:"
        curl -s http://localhost:8001/health | jq . || echo "Failed"
        echo ""
        echo "2. API docs:"
        curl -s http://localhost:8001/docs > /dev/null && echo "✓ Docs available at http://localhost:8001/docs" || echo "✗ Docs unavailable"
        ;;

    rebuild)
        log_info "Rebuilding MemOS API image..."
        docker-compose build --no-cache memos-api
        log_info "Rebuild complete"
        ;;

    *)
        echo "MemOS Instance Manager - $INSTANCE_NAME"
        echo ""
        echo "Usage: $0 {command} [options]"
        echo ""
        echo "Commands:"
        echo "  start        Start the instance"
        echo "  stop         Stop the instance"
        echo "  restart      Restart the instance"
        echo "  down         Stop and remove containers (preserve data)"
        echo "  clean        Remove all data and containers (DESTRUCTIVE)"
        echo "  logs [svc]   Show logs (default: memos-api)"
        echo "  status       Show instance status"
        echo "  shell [svc]  Open shell in service (default: memos-api)"
        echo "  test-api     Test API endpoints"
        echo "  rebuild      Rebuild memos-api image"
        echo ""
        echo "Examples:"
        echo "  $0 start"
        echo "  $0 logs neo4j"
        echo "  $0 shell memos-api"
        echo "  $0 test-api"
        ;;
esac
