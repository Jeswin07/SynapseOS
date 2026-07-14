from src.agents.models import AgentOutput, AgentMetadata


class BusinessFallback:

    @staticmethod
    def greeting() -> AgentOutput:
        return AgentOutput(
            answer=(
                "Hello! I'm SynapseOS Enterprise Intelligence Assistant.\n\n"
                "I can help you with:\n"
                "• Enterprise knowledge and documents\n"
                "• Business analytics and KPIs\n"
                "• Forecasting and predictions\n"
                "• Risk analysis\n"
                "• What-if scenario planning\n"
                "• Executive decision support\n\n"
                "How can I help you today?"
            ),
            metadata=AgentMetadata(
                agent_name="Business Agent",
                agent_type="business",
                success=True,
            ),
        )

    @staticmethod
    def invalid() -> AgentOutput:
        return AgentOutput(
            answer=(
                "I couldn't identify a business request.\n\n"
                "Try asking something like:\n"
                "• Summarize our sales performance\n"
                "• Forecast next month's revenue\n"
                "• Analyze customer churn\n"
                "• What happens if delivery improves by 20%?\n"
                "• What does our return policy say?"
            ),
            metadata=AgentMetadata(
                agent_name="Business Agent",
                agent_type="business",
                success=True,
            ),
        )