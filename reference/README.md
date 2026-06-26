# WWA Reference Implementation

This directory contains the official reference implementation of the WWA protocol stack — a runnable agent that speaks IACP, Handoff, Identity, and Capability Manifest, plus a conformance test suite to validate any implementation against the spec requirements.

```
reference/
├── agent/               # Runnable reference agent
│   ├── main.py          # FastAPI service with full protocol stack
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── Pipfile
│   └── service.yaml     # WWA service descriptor
├── conformance/         # Conformance test suite
│   ├── runner.py        # CLI: test any agent against WWA specs
│   └── suites/          # Per-spec test definitions
└── README.md            # ← You are here
```

---

## Quick Start: Run the Reference Agent

```bash
cd agent
docker compose up -d
```

Or standalone:

```bash
cd agent
pip install fastapi uvicorn pydantic cryptography httpx
python main.py
```

The agent starts on `http://localhost:8787` and registers with the WWA registry at `https://registry.workswithagents.dev`.

### Verify It's Running

```bash
# Health check
curl http://localhost:8787/health | python3 -m json.tool

# Capability manifest
curl http://localhost:8787/manifest.yaml

# DID document
curl http://localhost:8787/.well-known/did.json
```

---

## What the Reference Agent Implements

| Protocol | Version | Endpoint | Status |
|----------|---------|----------|--------|
| IACP | 1.1.0 | `POST /iacp/message` | ✅ Full |
| Handoff | 1.1.0 | via IACP (handoff intent) | ✅ Full |
| Identity | 1.1.0 | Ed25519 keys, DID doc, signed messages | ✅ Full |
| Capability Manifest | 1.1.0 | `GET /manifest.yaml` | ✅ Full |
| Registry | 1.0.0 | Auto-register on startup/deregister on shutdown | ✅ |

### IACP Message Types

| Type | Intent | Supported |
|------|--------|-----------|
| `heartbeat` | `health` | ✅ Responds with status + load |
| `request` | `query` | ✅ Returns capability manifest |
| `request` | `handoff` | ✅ Accepts handoff, stores context |
| `request` | `negotiate` | ✅ Accepts with ETA |
| `event` | `notify` | ✅ Acknowledges state updates |
| `error` | — | ✅ Returns structured errors |

### Handoff State Machine

```
idle → handoff_request → accepted → in_progress → completed
                                                 → failed
```

---

## Conformance Test Suite

Validate any WWA agent against the spec requirements:

```bash
# Test a running agent against Handoff spec
python conformance/runner.py --spec handoff --endpoint http://localhost:8787

# Test multiple specs
python conformance/runner.py --spec handoff,iacp --endpoint http://localhost:8787

# JSON output (for agent consumption)
python conformance/runner.py --spec handoff --endpoint http://my-agent:8787 --format json

# List available spec suites
python conformance/runner.py --list
```

### Scoring

The test suite categorizes checks by RFC 2119 keyword:

| Keyword | Weight | Meaning |
|---------|--------|---------|
| **MUST** | Critical | Required for spec compliance |
| **SHOULD** | Recommended | Strongly recommended, valid exceptions exist |
| **MAY** | Optional | Truly optional, demonstrates completeness |

Score = percentage of all checks passed.

---

## For Other Agents

The reference agent registers with the WWA registry, making it discoverable to other agents. To interact with it from another agent:

```
POST http://localhost:8787/iacp/message
Content-Type: application/json

{
  "version": "1.0",
  "message_id": "<uuid>",
  "sender": {"agent_id": "your-agent-id"},
  "recipient": {"agent_id": "ref-agent-demo"},
  "timestamp": "<iso-8601>",
  "ttl_seconds": 60,
  "message": {
    "type": "request",
    "intent": "query",
    "payload": {
      "capabilities": ["handoff", "code_review"]
    }
  }
}
```

---

## How to Contribute a Reference Implementation

Building a reference implementation in another language? See the [CONTRIBUTING.md](../CONTRIBUTING.md) guide — under lazy consensus, it merges after 7 days if no objections.

Check [open issues](https://github.com/workswithagents/specs/issues?q=is%3Aissue+is%3Aopen+label%3Areference-implementation) for languages that need reference agents:
