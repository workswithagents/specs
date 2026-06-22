# Pilot Protocol

**Version:** pre-release
**Status:** Published
**Layer:** L4/L5 — Session / Coordination
**Steward:** Community (pilot-protocol)
**License:** 
**Repository:** https://github.com/pilot-protocol/pilotprotocol
**Specification:** https://github.com/pilot-protocol/pilotprotocol

## Relationship to WWA

Pilot Protocol overlaps with WWA's discovery (L3 — Agent Registry) and handoff (L4) layers. It envisions an "Internet of Agents" — a peer-to-peer overlay network where agents discover each other through UDP-based NAT traversal and communicate over encrypted channels. While WWA's Agent Registry handles discovery through a centralized or federated registry, Pilot Protocol uses a decentralized P2P approach with virtual addressing. The two could complement each other: WWA for structured agent identity and capability negotiation, Pilot Protocol for low-latency P2P transport.

### Problem

Agent discovery across the open internet requires either a central registry (single point of failure, requires trust in the operator) or custom point-to-point integrations that don't scale. Agents behind NATs and firewalls are unreachable without relay infrastructure, and maintaining stable addresses as network topology changes adds significant complexity. Without a P2P discovery and transport layer, every cross-organization agent deployment requires manual network configuration and VPN tunnels.

### Solution

Pilot Protocol builds a decentralized P2P overlay network on top of UDP, enabling agents behind NATs to discover and communicate directly without relay servers. Each agent gets a virtual address that remains stable regardless of network changes, and discovery happens through a distributed hash table (DHT) rather than a central registry. Communication is encrypted end-to-end, and the Go implementation prioritizes low latency and high throughput for real-time agent interactions.

### When to use

- Open internet agent discovery where a central registry is undesirable or unavailable
- P2P agent networks requiring NAT traversal without manual network configuration
- Decentralized agent ecosystems where no single party controls the discovery infrastructure
- Low-latency, high-throughput agent-to-agent communication across the public internet

### When NOT to use

- Private, single-organization agent fleets — use WWA Agent Registry for simpler centralized discovery with identity management
- Single-agent deployments — the P2P overlay adds unnecessary complexity when there's only one agent
- Trusted network environments where NAT is not a concern — simpler transport protocols (WebSocket, gRPC) are sufficient
- Systems requiring structured capability negotiation — Pilot Protocol handles discovery and transport, not capability semantics (layer WWA on top)

### How it compares to similar specs

| Instead of THIS spec | When | Because |
|---|---|---|
| WWA Agent Registry | Centralized or federated agent discovery with identity and capability metadata | WWA Registry provides structured identity, capability negotiation, and compliance — not just address discovery |
| WWA Handoff | Structured task transfer with quality checklist and state context hash | WWA Handoff defines task-transfer semantics; Pilot Protocol provides the transport layer underneath |
| A2A | HTTP-based agent discovery with Agent Cards and JSON-RPC task lifecycle | A2A uses card-exchange over HTTP, which is simpler but doesn't solve NAT traversal or provide P2P transport |

### What you lose without THIS spec

- No standard for decentralized P2P agent discovery across the open internet
- Agents behind NATs cannot communicate directly without custom relay infrastructure
- No stable virtual addressing — agent addresses change with network topology unless you build your own overlay
- Every cross-organization agent deployment requires manual network configuration or VPN tunnels

## Architecture

Pilot Protocol builds a P2P overlay network on top of UDP, enabling agents behind NATs and firewalls to communicate directly. Each agent gets a virtual address that remains stable regardless of network topology changes. Discovery happens through a distributed hash table (DHT) rather than a central registry. Communication between agents is encrypted end-to-end. The protocol is implemented in Go with a focus on minimal latency and high throughput.

## Features

- UDP-based NAT traversal for direct agent-to-agent communication
- Peer-to-peer overlay network (no central coordinator required)
- Encrypted channels between agents
- Virtual addresses stable across network changes
- Distributed discovery via DHT (no central registry)
- Written in Go for performance
- 108 ★ on GitHub

## Governance

A community-driven open-source project under the `pilot-protocol` GitHub organization. No single corporate steward — governance is through open-source community norms. Still in pre-release with active development. License to be confirmed as the project matures.

## Examples

### Go SDK
```go
package main

import (
    "log"
    "github.com/pilot-protocol/pilotprotocol"
)

func main() {
    // Create a new agent node on the P2P overlay
    node, err := pilotprotocol.NewNode(pilotprotocol.Config{
        ListenAddr: ":0",     // random UDP port
        VirtualAddr: "agent.alice",
    })
    if err != nil {
        log.Fatal(err)
    }
    defer node.Close()

    // Discover another agent by virtual address
    peer, err := node.Discover("agent.bob")
    if err != nil {
        log.Fatal(err)
    }

    // Open an encrypted channel
    channel, err := node.Connect(peer)
    if err != nil {
        log.Fatal(err)
    }
    defer channel.Close()

    // Send a message
    channel.Send([]byte("hello from alice"))

    // Receive a response
    msg, _ := channel.Receive()
    log.Printf("Received: %s", msg)
}
```
