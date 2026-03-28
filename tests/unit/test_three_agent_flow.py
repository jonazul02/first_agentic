from first_agentic.agents.orchestrator import OrchestratorAgent
from first_agentic.core.demo_tasks import build_demo_tasks
from first_agentic.domain.enums import TaskStatus


def test_demo_flow_reaches_awaiting_user() -> None:
    orchestrator = OrchestratorAgent(max_review_rounds=3)
    tasks = build_demo_tasks()

    results = [orchestrator.run_task(task) for task in tasks]

    assert len(results) == 3
    assert all(result.final_status == TaskStatus.AWAITING_USER for result in results)


def test_review_rounds_do_not_exceed_limit() -> None:
    orchestrator = OrchestratorAgent(max_review_rounds=3)
    tasks = build_demo_tasks()

    for task in tasks:
        orchestrator.run_task(task)
        assert task.review_round <= 3
