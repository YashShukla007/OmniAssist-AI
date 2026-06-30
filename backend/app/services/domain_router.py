from backend.app.models.llm_manager import llm_manager


class DomainRouter:

    async def route(
        self,
        prompt: str,
        domain: str,
    ) -> dict:

        if domain == "IT Helpdesk":
            return await llm_manager.generate(
                prompt=f"[IT] {prompt}",
                domain=domain,
            )

        elif domain == "HR":
            return await llm_manager.generate(
                prompt=f"[HR] {prompt}",
                domain=domain,
            )

        elif domain == "Legal":
            return await llm_manager.generate(
                prompt=f"[Legal] {prompt}",
                domain=domain,
            )

        elif domain == "Finance":
            return await llm_manager.generate(
                prompt=f"[Finance] {prompt}",
                domain=domain,
            )

        else:
            return await llm_manager.generate(
                prompt=prompt,
                domain=domain,
            )


domain_router = DomainRouter()