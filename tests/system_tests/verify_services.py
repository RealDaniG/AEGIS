#!/usr/bin/env python3
"""
Service Verification Script for METATRONV2 System

This script verifies that all required services are running for 
Unified State Retrieval to work properly.
"""

import asyncio
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def verify_service(session, service_name: str, url: str) -> bool:
    """Verify that a service is running"""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
            if response.status == 200:
                logger.info(f"✅ {service_name}: Running")
                return True
            else:
                logger.error(f"❌ {service_name}: Not responding (Status: {response.status})")
                return False
    except Exception as e:
        logger.error(f"❌ {service_name}: Not running ({str(e)})")
        return False

async def verify_all_services():
    """Verify that all required services are running"""
    logger.info("Verifying METATRONV2 System Services...")
    logger.info("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        services = {
            "Metatron-ConsciousnessAI": "http://localhost:8003/api/health",
            "Open-A.G.I": "http://localhost:8090/health",
            "Unified API": "http://localhost:8005/health"
        }
        
        results = {}
        for service_name, url in services.items():
            results[service_name] = await verify_service(session, service_name, url)
        
        logger.info("=" * 50)
        logger.info("SERVICE VERIFICATION SUMMARY")
        logger.info("=" * 50)
        
        all_running = all(results.values())
        if all_running:
            logger.info("🎉 ALL SERVICES ARE RUNNING!")
            logger.info("\nYou can now access the unified system at:")
            logger.info("  - Unified State: http://localhost:8005/state")
            logger.info("  - WebSocket: ws://localhost:8005/ws")
            logger.info("  - API Documentation: http://localhost:8005/docs")
        else:
            logger.warning("⚠️  SOME SERVICES ARE NOT RUNNING")
            logger.info("\nTo enable Unified State Retrieval, please start:")
            not_running = [name for name, running in results.items() if not running]
            for service in not_running:
                logger.info(f"  - {service}")
        
        return all_running

def main():
    """Main entry point"""
    try:
        result = asyncio.run(verify_all_services())
        return 0 if result else 1
    except KeyboardInterrupt:
        logger.info("Verification interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Error during verification: {e}")
        return 1

if __name__ == "__main__":
    exit(main())