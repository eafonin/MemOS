#!/usr/bin/env python3
"""Debug-enabled startup script for MemOS API"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if os.getenv("DEBUG_MODE") == "true" else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add src to path
sys.path.insert(0, '/app/src')

def setup_debugpy():
    """Setup debugpy if enabled"""
    if os.getenv("DEBUGPY_ENABLE", "false").lower() == "true":
        try:
            import debugpy
            # Kill any existing debugpy listeners
            try:
                debugpy.listen(("0.0.0.0", 5678))
                logger.info("⏸ Debugger listening on port 5678")
                if os.getenv("DEBUGPY_WAIT", "false").lower() == "true":
                    logger.info("⏸ Waiting for debugger to attach...")
                    debugpy.wait_for_client()
                    logger.info("▶️ Debugger attached!")
            except RuntimeError as e:
                if "Address already in use" in str(e):
                    logger.warning("Debugger already listening on port 5678")
                else:
                    raise
        except Exception as e:
            logger.error(f"Failed to setup debugpy: {e}")

def main():
    """Main function to start the API"""
    setup_debugpy()
    
    import uvicorn
    
    # Disable reload in container (causes multiprocessing issues)
    # File watching still works through volume mounts
    try:
        logger.info("Starting MemOS API server (product_api)...")
        uvicorn.run(
            "memos.api.product_api:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload to avoid multiprocessing issues
            log_level="debug" if os.getenv("DEBUG_MODE") == "true" else "info",
            access_log=True
        )
    except Exception as e:
        logger.error(f"Failed with product_api: {e}")
        logger.info("Trying start_api...")
        try:
            uvicorn.run(
                "memos.api.start_api:app",
                host="0.0.0.0",
                port=8000,
                reload=False,
                log_level="debug",
                access_log=True
            )
        except Exception as e2:
            logger.error(f"Failed to start server: {e2}")
            logger.info("Keeping container alive for debugging...")
            import time
            while True:
                time.sleep(60)

if __name__ == "__main__":
    main()
