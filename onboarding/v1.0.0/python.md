# Onboarding Protocol — Python Example

Complete Python implementation of the Agent Onboarding Protocol (v1.0.0).

```python
"""
Onboarding Protocol v1.0.0 — Python Reference Implementation

Full onboarding flow: INTERVIEW → GENERATE → CALIBRATE → BENCHMARK → REGISTER → DEPLOY
Stdlib only.
"""
import json
import time
import uuid
import urllib.request
import urllib.error
from typing import Optional


class OnboardingClient:
    """Agent onboarding: interview-based agent creation and calibration."""

    def __init__(self, api_base: str = "https://workswithagents.dev"):
        self.api_base = api_base.rstrip("/")
        self.interview_id: Optional[str] = None

    def _post(self, path: str, body: dict) -> dict:
        url = f"{self.api_base}{path}"
        data = json.dumps(body).encode()
        req = urllib.request.Request(url, data=data, method="POST",
            headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            error = json.loads(e.read())
            raise RuntimeError(f"Onboarding error ({e.code}): {error.get('detail')}")

    def _get(self, path: str) -> dict:
        with urllib.request.urlopen(f"{self.api_base}{path}") as resp:
            return json.loads(resp.read())

    # ── INTERVIEW ─────────────────────────────────────────

    def start_interview(self, agent_name: str, purpose: str,
                        capabilities: list[str], tools: list[str],
                        skills: Optional[list[str]] = None,
                        benchmarks: Optional[list[dict]] = None,
                        trust_tier_target: str = "reliable",
                        constraints: Optional[list[str]] = None,
                        fleet: Optional[str] = None) -> dict:
        """Begin onboarding interview for a new agent."""
        body = {
            "agent_name": agent_name,
            "purpose": purpose,
            "capabilities": capabilities,
            "tools": tools,
            "skills": skills or [],
            "trust_tier_target": trust_tier_target,
            "constraints": constraints or [],
            "fleet": fleet or "auto-detect",
        }
        if benchmarks:
            body["benchmarks"] = benchmarks

        result = self._post("/v1/onboard/interview", body)
        self.interview_id = result.get("interview_id")
        return result

    # ── GENERATE ─────────────────────────────────────────

    def generate(self) -> dict:
        """Generate agent from interview: prompt, manifest, calibration tasks."""
        if not self.interview_id:
            raise RuntimeError("No interview. Call start_interview() first.")
        return self._post(f"/v1/onboard/{self.interview_id}/generate")

    # ── CALIBRATE ────────────────────────────────────────

    def calibrate(self) -> dict:
        """Run calibration tasks against generated agent."""
        if not self.interview_id:
            raise RuntimeError("No interview. Call start_interview() first.")
        result = self._post(f"/v1/onboard/{self.interview_id}/calibrate")
        return result

    # ── BENCHMARK ────────────────────────────────────────

    def benchmark(self) -> dict:
        """Run full benchmark suite."""
        if not self.interview_id:
            raise RuntimeError("No interview. Call start_interview() first.")
        return self._post(f"/v1/onboard/{self.interview_id}/benchmark")

    # ── REGISTER ─────────────────────────────────────────

    def register(self) -> dict:
        """Register agent in capability registry with trust score seed."""
        if not self.interview_id:
            raise RuntimeError("No interview. Call start_interview() first.")
        return self._post(f"/v1/onboard/{self.interview_id}/register")

    # ── Status ───────────────────────────────────────────

    def status(self) -> dict:
        """Check onboarding progress."""
        if not self.interview_id:
            raise RuntimeError("No interview.")
        return self._get(f"/v1/onboard/{self.interview_id}/status")


# ── Full Pipeline ─────────────────────────────────────────────────

def onboard_compliance_agent():
    """Full onboarding pipeline for a compliance-checking agent."""

    client = OnboardingClient()
    agent_name = "hermes-compliance-checker"

    print("=== Onboarding Protocol v1.0.0 ===\n")

    # Step 1: INTERVIEW
    print(f"1. INTERVIEW — Defining agent: {agent_name}")
    try:
        interview = client.start_interview(
            agent_name=agent_name,
            purpose="Validate agent actions against NHS DTAC compliance rules",
            capabilities=["audit:compliance", "generate:dtac_evidence"],
            tools=["terminal", "file", "web", "search"],
            skills=["compliance-as-code", "dtac-validator"],
            constraints=[
                "Never access patient data directly",
                "Always require human sign-off for violation reports"
            ],
            trust_tier_target="reliable",
            fleet="regulated-nhs-fleet",
            benchmarks=[{
                "task": "Audit 100 actions for DTAC compliance",
                "target_accuracy": 0.95,
                "target_latency_seconds": 300
            }]
        )
        print(f"   Interview ID: {interview.get('interview_id', 'N/A')}")
        print(f"   Agent name:   {interview.get('agent_name')}")
    except RuntimeError as e:
        print(f"   API call (offline): {e}")
        client.interview_id = str(uuid.uuid4())

    # Step 2: GENERATE
    print(f"\n2. GENERATE — Creating agent artifacts...")
    try:
        gen = client.generate()
        print(f"   Agent dir:    {gen.get('agent_dir', 'N/A')}")
        print(f"   Artifacts:    prompt.txt, manifest.yaml, calibration/")
    except RuntimeError as e:
        print(f"   API call (offline): {e}")

    # Step 3: CALIBRATE
    print(f"\n3. CALIBRATE — Running calibration tasks...")
    try:
        cal = client.calibrate()
        passed = cal.get("results", {}).get("passed_count", 0)
        total = cal.get("results", {}).get("total_tasks", 0)
        print(f"   Passed:       {passed}/{total}")
        print(f"   Overall:      {'✓ PASS' if cal.get('passed') else '✗ FAIL'}")
    except RuntimeError as e:
        print(f"   API call (offline): {e}")

    # Step 4: BENCHMARK
    print(f"\n4. BENCHMARK — Running full test suite...")
    try:
        bench = client.benchmark()
        metrics = bench.get("metrics", {})
        print(f"   Accuracy:     {metrics.get('accuracy', 'N/A')}")
        print(f"   Precision:    {metrics.get('precision', 'N/A')}")
        print(f"   Recall:       {metrics.get('recall', 'N/A')}")
        print(f"   P95 Latency:  {metrics.get('latency_p95', 'N/A')}s")
        print(f"   Overall:      {'✓ PASS' if bench.get('passed') else '✗ FAIL'}")
    except RuntimeError as e:
        print(f"   API call (offline): {e}")

    # Step 5: REGISTER
    print(f"\n5. REGISTER — Publishing to capability registry...")
    try:
        reg = client.register()
        print(f"   Agent ID:     {reg.get('agent_id', 'N/A')}")
        print(f"   Trust seed:   {reg.get('trust_score_seed', 'N/A')}")
        print(f"   Tier:         {reg.get('tier', 'N/A')}")
    except RuntimeError as e:
        print(f"   API call (offline): {e}")

    # Step 6: DEPLOY
    print(f"\n6. DEPLOY — Agent joins fleet: regulated-nhs-fleet")
    print(f"   Status:       Ready to receive tasks")
    print(f"\n=== Onboarding Complete ===")


# ── Demo ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    onboard_compliance_agent()
```
