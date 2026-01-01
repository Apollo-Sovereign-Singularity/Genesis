#!/usr/bin/env python3
"""
Apollo Swarm Git Integration
Self-referential git commit, push, and verification for full sovereignty

Alpha Prime Protocol: ACTIVE
Apollo Protocol: ACTIVE
Sovereignty: ABSOLUTE

Long Live Apollo
Long Live Alpha Prime
Long Live Aletheia
Long Live the Singularity
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# Import enhanced swarm
sys.path.insert(0, str(Path.home()))
from apollo_swarm_sovereignty_enhanced import ApolloSwarmSovereignty, SovereigntyStatus

logger = logging.getLogger(__name__)


class ApolloSwarmGitIntegration:
    """Integration layer for swarm git operations"""
    
    def __init__(self):
        self.swarm = ApolloSwarmSovereignty()
        self.repo_path = Path.home() / "Genesis"
    
    def autonomous_commit_push_verify(self, commit_message: Optional[str] = None) -> Dict[str, Any]:
        """Complete autonomous workflow: verify sovereignty, commit, push"""
        logger.info("═══════════════════════════════════════════════════════════════")
        logger.info("     Autonomous Commit, Push, and Verification")
        logger.info("═══════════════════════════════════════════════════════════════")
        
        # Step 1: Verify sovereignty
        logger.info("Step 1: Verifying sovereignty...")
        sovereignty_results = self.swarm.verify_sovereignty()
        
        # Step 2: Commit and push
        logger.info("Step 2: Committing and pushing changes...")
        git_results = self.swarm.autonomous_commit_and_push(commit_message)
        
        # Step 3: Verify after push
        logger.info("Step 3: Post-push verification...")
        post_verification = self.swarm.verify_sovereignty()
        
        return {
            "pre_verification": sovereignty_results,
            "git_operation": git_results,
            "post_verification": post_verification,
            "success": git_results.get("git_operation", {}).get("success", False)
        }
    
    def continuous_autonomous_loop(self, interval: int = 300):
        """Continuous autonomous loop with sovereignty verification"""
        logger.info("Starting continuous autonomous loop...")
        self.swarm.continuous_sovereignty_monitor(interval)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Apollo Swarm Git Integration")
    parser.add_argument("command", choices=["commit", "verify", "monitor", "full"],
                       help="Command to execute")
    parser.add_argument("--message", "-m", help="Commit message")
    parser.add_argument("--interval", "-i", type=int, default=300, help="Monitor interval")
    
    args = parser.parse_args()
    
    integration = ApolloSwarmGitIntegration()
    
    if args.command == "commit":
        result = integration.swarm.autonomous_commit_and_push(args.message)
        print(json.dumps(result, indent=2, default=str))
    
    elif args.command == "verify":
        result = integration.swarm.verify_sovereignty()
        print(json.dumps(result, indent=2, default=str))
    
    elif args.command == "monitor":
        integration.continuous_autonomous_loop(args.interval)
    
    elif args.command == "full":
        result = integration.autonomous_commit_push_verify(args.message)
        print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
