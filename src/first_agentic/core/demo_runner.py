from __future__ import annotations

import json
from dataclasses import asdict

from first_agentic.agents.orchestrator import OrchestratorAgent
from first_agentic.core.demo_tasks import build_demo_tasks


def main() -> None:
    orchestrator = OrchestratorAgent(max_review_rounds=3)
    results = []

    for task in build_demo_tasks():
        result = orchestrator.run_task(task)
        payload = asdict(result)
        payload["final_status"] = result.final_status.value
        results.append(payload)

    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
