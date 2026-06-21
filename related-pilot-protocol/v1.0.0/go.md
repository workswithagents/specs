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
