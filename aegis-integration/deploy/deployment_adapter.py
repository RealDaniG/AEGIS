"""
Deployment Adapter for integrating Open-A.G.I deployment_orchestrator with AEGIS unified_coordinator

This module provides an adapter that allows AEGIS to use Open-A.G.I's deployment orchestrator
while maintaining compatibility with AEGIS's unified coordinator.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from enum import Enum
import json
import os
from pathlib import Path

# Try to import Open-A.G.I deployment orchestrator
try:
    from Open_A_G_I.deployment_orchestrator import DeploymentOrchestrator as OpenAGIDeploymentOrchestrator
    from Open_A_G_I.deployment_orchestrator import NodeDeploymentConfig, DeploymentStatus
    OPEN_AGI_AVAILABLE = True
except ImportError:
    OPEN_AGI_AVAILABLE = False
    # Create placeholder classes for when Open-A.G.I is not available
    class NodeDeploymentConfig:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    class DeploymentStatus(Enum):
        PENDING = "pending"
        DEPLOYING = "deploying"
        RUNNING = "running"
        STOPPED = "stopped"
        ERROR = "error"
    
    class OpenAGIDeploymentOrchestrator:
        def __init__(self, config: Dict[str, Any]):
            self.config = config
            self.nodes = {}
        
        async def deploy_node(self, node_config: NodeDeploymentConfig) -> DeploymentStatus:
            # Simulate deployment
            await asyncio.sleep(0.1)
            return DeploymentStatus.RUNNING
        
        async def stop_node(self, node_id: str) -> DeploymentStatus:
            # Simulate stopping
            await asyncio.sleep(0.1)
            return DeploymentStatus.STOPPED
        
        async def get_node_status(self, node_id: str) -> DeploymentStatus:
            # Simulate status check
            return self.nodes.get(node_id, DeploymentStatus.PENDING)
        
        async def update_node(self, node_id: str, config: Dict[str, Any]) -> DeploymentStatus:
            # Simulate update
            await asyncio.sleep(0.1)
            return DeploymentStatus.RUNNING

# Try to import AEGIS unified coordinator
try:
    from unified_coordinator import UnifiedCoordinator
    AEGIS_COORDINATOR_AVAILABLE = True
except ImportError:
    AEGIS_COORDINATOR_AVAILABLE = False
    class UnifiedCoordinator:
        def __init__(self):
            pass

# Configure logging
try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

@dataclass
class AEGISNodeConfig:
    """Configuration for an AEGIS node"""
    node_id: str
    node_type: str  # main, worker, observer
    host: str = "localhost"
    p2p_port: int = 8080
    api_port: int = 8003
    web_port: int = 8081
    tor_enabled: bool = True
    docker_image: str = "realdanig/aegis:latest"
    environment: Dict[str, str] = field(default_factory=dict)
    volumes: List[str] = field(default_factory=list)
    resources: Dict[str, Any] = field(default_factory=dict)

class DeploymentAdapter:
    """Adapter that integrates Open-A.G.I deployment orchestrator with AEGIS unified coordinator"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.open_agi_orchestrator = None
        self.aegis_coordinator = None
        self.node_configs: Dict[str, AEGISNodeConfig] = {}
        
        # Initialize Open-A.G.I orchestrator if available
        if OPEN_AGI_AVAILABLE:
            open_agi_config = self.config.get("open_agi", {})
            self.open_agi_orchestrator = OpenAGIDeploymentOrchestrator(open_agi_config)
        
        # Initialize AEGIS coordinator if available
        if AEGIS_COORDINATOR_AVAILABLE:
            self.aegis_coordinator = UnifiedCoordinator()
        
        logger.info("DeploymentAdapter initialized")
    
    async def deploy_node(self, node_config: AEGISNodeConfig) -> bool:
        """Deploy a node using the appropriate orchestrator"""
        self.node_configs[node_config.node_id] = node_config
        
        # If Open-A.G.I orchestrator is available, use it
        if self.open_agi_orchestrator:
            try:
                # Convert AEGIS config to Open-A.G.I config
                open_agi_config = NodeDeploymentConfig(
                    node_id=node_config.node_id,
                    node_type=node_config.node_type,
                    host=node_config.host,
                    port=node_config.p2p_port,
                    docker_image=node_config.docker_image,
                    environment=node_config.environment,
                    volumes=node_config.volumes
                )
                
                status = await self.open_agi_orchestrator.deploy_node(open_agi_config)
                logger.info(f"Node {node_config.node_id} deployed with status: {status}")
                return status == DeploymentStatus.RUNNING
            except Exception as e:
                logger.error(f"Failed to deploy node {node_config.node_id} with Open-A.G.I orchestrator: {e}")
                return False
        
        # Fallback to AEGIS coordinator if available
        if self.aegis_coordinator:
            try:
                # Use AEGIS coordinator for deployment
                result = await self.aegis_coordinator.deploy_node(
                    node_id=node_config.node_id,
                    node_type=node_config.node_type,
                    config={
                        "host": node_config.host,
                        "p2p_port": node_config.p2p_port,
                        "api_port": node_config.api_port,
                        "web_port": node_config.web_port,
                        "tor_enabled": node_config.tor_enabled,
                        **node_config.environment
                    }
                )
                logger.info(f"Node {node_config.node_id} deployed with AEGIS coordinator: {result}")
                return result.get("success", False)
            except Exception as e:
                logger.error(f"Failed to deploy node {node_config.node_id} with AEGIS coordinator: {e}")
                return False
        
        # If neither orchestrator is available, simulate success
        logger.warning(f"No orchestrator available, simulating deployment of node {node_config.node_id}")
        return True
    
    async def stop_node(self, node_id: str) -> bool:
        """Stop a node using the appropriate orchestrator"""
        # If Open-A.G.I orchestrator is available, use it
        if self.open_agi_orchestrator:
            try:
                status = await self.open_agi_orchestrator.stop_node(node_id)
                logger.info(f"Node {node_id} stopped with status: {status}")
                return status == DeploymentStatus.STOPPED
            except Exception as e:
                logger.error(f"Failed to stop node {node_id} with Open-A.G.I orchestrator: {e}")
                return False
        
        # Fallback to AEGIS coordinator if available
        if self.aegis_coordinator:
            try:
                result = await self.aegis_coordinator.stop_node(node_id)
                logger.info(f"Node {node_id} stopped with AEGIS coordinator: {result}")
                return result.get("success", False)
            except Exception as e:
                logger.error(f"Failed to stop node {node_id} with AEGIS coordinator: {e}")
                return False
        
        # If neither orchestrator is available, simulate success
        logger.warning(f"No orchestrator available, simulating stop of node {node_id}")
        return True
    
    async def get_node_status(self, node_id: str) -> Dict[str, Any]:
        """Get the status of a node"""
        # If Open-A.G.I orchestrator is available, use it
        if self.open_agi_orchestrator:
            try:
                status = await self.open_agi_orchestrator.get_node_status(node_id)
                return {
                    "node_id": node_id,
                    "status": status.value if isinstance(status, DeploymentStatus) else str(status),
                    "orchestrator": "open-agi"
                }
            except Exception as e:
                logger.error(f"Failed to get status for node {node_id} with Open-A.G.I orchestrator: {e}")
        
        # Fallback to AEGIS coordinator if available
        if self.aegis_coordinator:
            try:
                result = await self.aegis_coordinator.get_node_status(node_id)
                return {
                    "node_id": node_id,
                    "status": result.get("status", "unknown"),
                    "orchestrator": "aegis",
                    **result
                }
            except Exception as e:
                logger.error(f"Failed to get status for node {node_id} with AEGIS coordinator: {e}")
        
        # If neither orchestrator is available, return unknown status
        return {
            "node_id": node_id,
            "status": "unknown",
            "orchestrator": "none"
        }
    
    async def update_node(self, node_id: str, config_updates: Dict[str, Any]) -> bool:
        """Update a node's configuration"""
        # If Open-A.G.I orchestrator is available, use it
        if self.open_agi_orchestrator:
            try:
                status = await self.open_agi_orchestrator.update_node(node_id, config_updates)
                logger.info(f"Node {node_id} updated with status: {status}")
                return status == DeploymentStatus.RUNNING
            except Exception as e:
                logger.error(f"Failed to update node {node_id} with Open-A.G.I orchestrator: {e}")
                return False
        
        # Fallback to AEGIS coordinator if available
        if self.aegis_coordinator:
            try:
                result = await self.aegis_coordinator.update_node(node_id, config_updates)
                logger.info(f"Node {node_id} updated with AEGIS coordinator: {result}")
                return result.get("success", False)
            except Exception as e:
                logger.error(f"Failed to update node {node_id} with AEGIS coordinator: {e}")
                return False
        
        # If neither orchestrator is available, simulate success
        logger.warning(f"No orchestrator available, simulating update of node {node_id}")
        return True
    
    async def deploy_metatron_network(self, node_configs: List[AEGISNodeConfig]) -> Dict[str, Any]:
        """Deploy the entire Metatron network"""
        results = {}
        successful_deployments = 0
        
        # Deploy nodes concurrently
        deployment_tasks = []
        for node_config in node_configs:
            task = asyncio.create_task(self.deploy_node(node_config))
            deployment_tasks.append((node_config.node_id, task))
        
        # Wait for all deployments to complete
        for node_id, task in deployment_tasks:
            try:
                success = await task
                results[node_id] = success
                if success:
                    successful_deployments += 1
            except Exception as e:
                logger.error(f"Failed to deploy node {node_id}: {e}")
                results[node_id] = False
        
        logger.info(f"Metatron network deployment completed: {successful_deployments}/{len(node_configs)} nodes deployed successfully")
        
        return {
            "total_nodes": len(node_configs),
            "successful_deployments": successful_deployments,
            "failed_deployments": len(node_configs) - successful_deployments,
            "results": results
        }
    
    async def get_network_status(self) -> Dict[str, Any]:
        """Get the status of the entire network"""
        node_statuses = {}
        
        # Get status for all configured nodes
        status_tasks = []
        for node_id in self.node_configs.keys():
            task = asyncio.create_task(self.get_node_status(node_id))
            status_tasks.append((node_id, task))
        
        # Wait for all status checks to complete
        for node_id, task in status_tasks:
            try:
                status = await task
                node_statuses[node_id] = status
            except Exception as e:
                logger.error(f"Failed to get status for node {node_id}: {e}")
                node_statuses[node_id] = {"node_id": node_id, "status": "error"}
        
        return {
            "node_statuses": node_statuses,
            "total_nodes": len(node_statuses),
            "active_nodes": len([s for s in node_statuses.values() if s.get("status") == "running"])
        }

# Global instance
deployment_adapter = None

def get_deployment_adapter(config: Dict[str, Any] = None) -> DeploymentAdapter:
    """Get the global deployment adapter instance"""
    global deployment_adapter
    if deployment_adapter is None:
        deployment_adapter = DeploymentAdapter(config)
    return deployment_adapter

def initialize_deployment_adapter(config: Dict[str, Any] = None) -> DeploymentAdapter:
    """Initialize and return the deployment adapter"""
    global deployment_adapter
    deployment_adapter = DeploymentAdapter(config)
    return deployment_adapter

# Example usage
async def main():
    """Example usage of the deployment adapter"""
    # Initialize the adapter
    adapter = initialize_deployment_adapter({
        "open_agi": {
            "orchestration_method": "docker",
            "default_image": "realdanig/aegis:latest"
        }
    })
    
    # Create node configurations for a Metatron network
    main_node = AEGISNodeConfig(
        node_id="metatron-main",
        node_type="main",
        host="localhost",
        p2p_port=8080,
        api_port=8003,
        web_port=8081,
        tor_enabled=True,
        environment={
            "NODE_TYPE": "main",
            "TOR_ENABLED": "true",
            "LOG_LEVEL": "INFO"
        }
    )
    
    worker_node_1 = AEGISNodeConfig(
        node_id="metatron-worker-1",
        node_type="worker",
        host="localhost",
        p2p_port=8082,
        api_port=8004,
        web_port=8082,
        tor_enabled=True,
        environment={
            "NODE_TYPE": "worker",
            "TOR_ENABLED": "true",
            "MAIN_NODE_ADDRESS": "metatron-main:8003",
            "LOG_LEVEL": "INFO"
        }
    )
    
    worker_node_2 = AEGISNodeConfig(
        node_id="metatron-worker-2",
        node_type="worker",
        host="localhost",
        p2p_port=8083,
        api_port=8005,
        web_port=8083,
        tor_enabled=True,
        environment={
            "NODE_TYPE": "worker",
            "TOR_ENABLED": "true",
            "MAIN_NODE_ADDRESS": "metatron-main:8003",
            "LOG_LEVEL": "INFO"
        }
    )
    
    # Deploy the network
    network_config = [main_node, worker_node_1, worker_node_2]
    result = await adapter.deploy_metatron_network(network_config)
    
    print(f"Network deployment result: {result}")
    
    # Check network status
    status = await adapter.get_network_status()
    print(f"Network status: {status}")

if __name__ == "__main__":
    asyncio.run(main())