# Onboarding Protocol — cURL Examples

cURL command examples for the Agent Onboarding Protocol (v1.0.0).

## 1. Start Interview

```bash
curl -X POST https://workswithagents.dev/v1/onboard/interview \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "hermes-compliance-checker",
    "purpose": "Validate agent actions against NHS DTAC compliance rules",
    "capabilities": ["audit:compliance", "generate:dtac_evidence"],
    "tools": ["terminal", "file", "web", "search"],
    "skills": ["compliance-as-code", "dtac-validator"],
    "trust_tier_target": "reliable",
    "constraints": [
      "Never access patient data directly",
      "Always require human sign-off for violation reports"
    ],
    "fleet": "regulated-nhs-fleet",
    "benchmarks": [{
      "task": "Audit 100 actions for DTAC compliance",
      "target_accuracy": 0.95,
      "target_latency_seconds": 300
    }]
  }'
```

**Expected response (201 Created):**
```json
{
  "interview_id": "019acb7b-8a9b-7c6d-5e4f-3a2b1c0d9e8f",
  "agent_name": "hermes-compliance-checker",
  "phase": "interview",
  "created_at": "2026-06-20T12:00:00Z"
}
```

Store the interview ID:
```bash
INTERVIEW_ID="019acb7b-8a9b-7c6d-5e4f-3a2b1c0d9e8f"
```

## 2. Generate Agent

```bash
curl -X POST "https://workswithagents.dev/v1/onboard/$INTERVIEW_ID/generate" \
  -H "Content-Type: application/json"
```

**Expected response (200 OK):**
```json
{
  "agent_dir": "agent_hermes-compliance-checker/",
  "artifacts": [
    "AGENTS.md",
    "manifest.yaml",
    "prompt.txt",
    "skills.txt",
    "calibration/task-1.yaml",
    "calibration/task-2.yaml",
    "config.yaml"
  ],
  "phase": "generate"
}
```

## 3. Run Calibration

```bash
curl -X POST "https://workswithagents.dev/v1/onboard/$INTERVIEW_ID/calibrate" \
  -H "Content-Type: application/json"
```

**Expected response (200 OK):**
```json
{
  "interview_id": "019acb7b-8a9b-7c6d-5e4f-3a2b1c0d9e8f",
  "passed": true,
  "phase": "calibrate",
  "results": {
    "passed_count": 5,
    "total_tasks": 5,
    "tasks": [
      {"task_id": "calib-1", "passed": true, "score": 0.92},
      {"task_id": "calib-2", "passed": true, "score": 0.88}
    ]
  }
}
```

## 4. Run Benchmark

```bash
curl -X POST "https://workswithagents.dev/v1/onboard/$INTERVIEW_ID/benchmark" \
  -H "Content-Type: application/json"
```

**Expected response (200 OK):**
```json
{
  "interview_id": "019acb7b-8a9b-7c6d-5e4f-3a2b1c0d9e8f",
  "passed": true,
  "phase": "benchmark",
  "metrics": {
    "accuracy": 0.93,
    "precision": 0.91,
    "recall": 0.89,
    "latency_p95": 245,
    "token_efficiency": 1200
  }
}
```

## 5. Register in Fleet

```bash
curl -X POST "https://workswithagents.dev/v1/onboard/$INTERVIEW_ID/register" \
  -H "Content-Type: application/json"
```

**Expected response (200 OK):**
```json
{
  "agent_id": "hermes-compliance-checker",
  "trust_score_seed": 0.60,
  "tier": "reliable",
  "fleet": "regulated-nhs-fleet",
  "registered_at": "2026-06-20T12:15:00Z"
}
```

## 6. Check Status

```bash
curl "https://workswithagents.dev/v1/onboard/$INTERVIEW_ID/status" \
  -H "Accept: application/json"
```

**Expected response (200 OK):**
```json
{
  "interview_id": "019acb7b-8a9b-7c6d-5e4f-3a2b1c0d9e8f",
  "agent_name": "hermes-compliance-checker",
  "phase": "complete",
  "completed": true,
  "agent_id": "hermes-compliance-checker"
}
```

## Full Pipeline (One-Liner Script)

```bash
#!/bin/bash
# Full onboarding pipeline

NAME="my-new-agent"
PURPOSE="Audit agent actions for compliance"

# 1. Interview
INTERVIEW=$(curl -s -X POST https://workswithagents.dev/v1/onboard/interview \
  -H "Content-Type: application/json" \
  -d "{\"agent_name\":\"$NAME\",\"purpose\":\"$PURPOSE\",\"capabilities\":[\"audit\"],\"tools\":[\"terminal\"]}")
ID=$(echo "$INTERVIEW" | jq -r '.interview_id')
echo "Interview: $ID"

# 2. Generate
echo "Generating..."
curl -s -X POST "https://workswithagents.dev/v1/onboard/$ID/generate"

# 3. Calibrate
echo "Calibrating..."
CAL=$(curl -s -X POST "https://workswithagents.dev/v1/onboard/$ID/calibrate")
echo "$CAL" | jq '.passed'

# 4. Benchmark
echo "Benchmarking..."
BENCH=$(curl -s -X POST "https://workswithagents.dev/v1/onboard/$ID/benchmark")
echo "$BENCH" | jq '.metrics'

# 5. Register
echo "Registering..."
curl -s -X POST "https://workswithagents.dev/v1/onboard/$ID/register" | jq '.agent_id'
```

## API Summary

| Method | Path | Phase |
|--------|------|-------|
| POST | `/v1/onboard/interview` | 1. Interview |
| POST | `/v1/onboard/{id}/generate` | 2. Generate |
| POST | `/v1/onboard/{id}/calibrate` | 3. Calibrate |
| POST | `/v1/onboard/{id}/benchmark` | 4. Benchmark |
| POST | `/v1/onboard/{id}/register` | 5. Register |
| GET | `/v1/onboard/{id}/status` | Status check |
