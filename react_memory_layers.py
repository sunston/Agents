import numpy as np

class MockVectorDB:
    """Simulates a vector database storing enterprise knowledge."""
    def __init__(self):
        self.kb_text = [
            "Contract #1042 with Global Logistics guarantees a 5% discount on orders exceeding $50,000.",
            "Standard corporate policy mandates net-30 payment terms for all manufacturing vendors.",
            "Support log: Global Logistics experienced a 3-day hub delay in Sacramento during May 2026."
        ]
        self.embeddings = np.array([
            [0.15, 0.88, 0.34],  
            [0.02, 0.41, 0.91],  
            [0.89, 0.12, 0.22]   
        ])

    def query(self, query_text: str, top_k: int = 1) -> str:
        query_vector = np.array([0.18, 0.85, 0.30]) 
        
        dot_products = np.dot(self.embeddings, query_vector)
        norms_db = np.linalg.norm(self.embeddings, axis=1)
        norm_query = np.linalg.norm(query_vector)
        similarities = dot_products / (norms_db * norm_query)
        
        best_idx = np.argmax(similarities)
        return self.kb_text[best_idx]


class B2BAgentSession:
    """Manages short-term conversation history and internal scratchpad memory."""
    def __init__(self, session_id: str, client_company: str):
        self.session_id = session_id
        self.client_company = client_company
        self.conversation_history = [
            {"role": "system", "content": f"You are an enterprise procurement agent handling {client_company}."}
        ]
        self.scratchpad = []

    def add_to_history(self, role: str, content: str):
        self.conversation_history.append({"role": role, "content": content})

    def log_scratchpad(self, thought_or_action: str):
        self.scratchpad.append(thought_or_action)

    def clear_scratchpad(self):
        self.scratchpad.clear()


if __name__ == "__main__":
    vector_db = MockVectorDB()
    session = B2BAgentSession(session_id="sess_9948", client_company="Acme Corp")

    user_query = "We just placed a $60,000 order with Global Logistics. Are we getting our negotiated contract rate?"
    session.add_to_history(role="user", content=user_query)

    print(f"--- [User Input Received via Session {session.session_id}] ---")
    print(f"User: {user_query}\n")

    session.log_scratchpad("THOUGHT: User is asking about a specific vendor contract rate for a $60k order.")
    session.log_scratchpad("ACTION: Need to query Long-Term Memory (Vector DB) for Global Logistics contract terms.")

    retrieved_context = vector_db.query("Global Logistics contract discount terms")
    session.log_scratchpad(f"OBSERVATION: Vector DB returned: '{retrieved_context}'")
    session.log_scratchpad("THOUGHT: The retrieved contract confirms a 5% discount for orders over $50,000. The user's order is $60,000, so the discount applies.")

    payload_to_llm = {
        "model_context": session.conversation_history.copy(), 
        "agent_working_memory": session.scratchpad.copy(),     
        "injected_knowledge": retrieved_context         
    }

    agent_response = (
        f"Yes, Acme Corp qualifies for the contract rate. According to Contract #1042, "
        f"Global Logistics applies a 5% discount for orders over $50,000. Because your current "
        f"order is $60,000, the discount will automatically apply at invoicing."
    )

    session.add_to_history(role="assistant", content=agent_response)

    print("--- [Agent Internal Execution Log (Scratchpad)] ---")
    for log in payload_to_llm["agent_working_memory"]:
        print(f"  > {log}")
        
    print("\n--- [Final Short-Term Conversation State] ---")
    for turn in session.conversation_history:
        print(f"{turn['role'].upper()}: {turn['content']}")

    session.clear_scratchpad()
