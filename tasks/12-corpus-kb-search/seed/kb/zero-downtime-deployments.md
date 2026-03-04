# Zero-Downtime Deployment Strategies

## Overview
Zero-downtime deployments ensure users experience no interruption during releases.

## Blue-Green Deployment
The recommended strategy for zero-downtime deployments is blue-green deployment. Maintain two identical production environments. Route traffic to "blue" while deploying to "green". Switch the load balancer when green is verified.

### Steps
1. Deploy new version to inactive environment (green)
2. Run smoke tests against green
3. Switch load balancer from blue to green
4. Monitor for issues
5. Keep blue as instant rollback

## Database Migration Strategy
For database changes in zero-downtime deployments, use expand-and-contract migrations:
1. **Expand**: Add new columns/tables (backward compatible)
2. **Migrate**: Backfill data in the background
3. **Contract**: Remove old columns after all code uses new schema

## Rolling Updates
Alternative to blue-green: update instances one at a time. Works well with Kubernetes but requires backward-compatible changes.

## Canary Releases
Route a small percentage of traffic to the new version. Gradually increase if metrics look healthy.

## Feature Flags
Decouple deployment from release. Deploy code with features disabled, then enable for specific users or percentages.
