"""Point d'entree du worker Mistral Workflows — Les Editions du Discernement."""

import asyncio

from mistralai.workflows import discover_all_workflows_in_package, run_worker


async def main() -> None:
    discovered = discover_all_workflows_in_package("workflows")
    await run_worker(discovered)


if __name__ == "__main__":
    asyncio.run(main())
