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
