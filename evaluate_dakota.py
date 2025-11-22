
import os
import dotenv
import asyncio

# Disable LangSmith tracing to prevent noise in output
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_API_KEY"] = ""

from deep_agent import DeepAgentE2B

# Load environment variables
dotenv.load_dotenv()

async def main():
    # Define the task based on the user's request
    task = r"""
    I want you to evaluate the significance of the following mathematical framework in the context of generalized learning and the repository 'HarleyCoops/Dakota1890'.

    The framework is described as follows:

    ### 1. The Transformation Function (Book to Environment)
    Let $\mathcal{T}$ be the historical textbook source. We define an extraction function $\mathcal{E}$ (the VLM) that maps the raw text into a structured grammar space $\mathcal{G}$:
    $$ \mathcal{G} = \{g_1, g_2, \dots, g_N\} = \mathcal{E}(\mathcal{T}) $$
    Where each grammar rule $g_k$ acts as a constraint function on the generated token sequence $y$:
    $$ g_k: \Sigma^* \rightarrow \{0, 1\} $$

    ### 2. The Compositional Reward Function
    Standard RLHF or GRPO typically uses a singular reward model $R(y)$. Your approach decomposes $R$ into a weighted sum of linguistic primitives.
    Let $y_i$ be the $i$-th generation in a group of size $G$. The reward $r_i$ for generation $y_i$ given prompt $x$ is:
    $$ r(y_i, x) = \lambda_{diff}(x) \cdot \left[ \alpha \cdot R_{char}(y_i, x) + \beta \cdot R_{morph}(y_i, \mathcal{G}) + \gamma \cdot R_{sem}(y_i, y^*) \right] $$
    Where:
    *   **$R_{char}$ (Orthography)**: The Intersection-over-Union (or Recall) of required special unicode characters $\mathcal{C}_{spec}$.
        $$ R_{char} = \frac{|chars(y_i) \cap chars(x)|}{|chars(x) \cap \mathcal{C}_{spec}|} $$
    *   **$R_{morph}$ (Syntax)**: A binary or scalar check against specific grammar rules $g_k \in \mathcal{G}$.
        $$ R_{morph} = \frac{1}{|A|}\sum_{a \in A} \mathbb{I}(a \subset y_i) \quad \text{where } A \text{ are required affixes} $$
    *   **$R_{sem}$ (Semantics)**: Semantic similarity to ground truth (or Dictionary lookup).
    *   **Weights**: $(\alpha, \beta, \gamma) = (0.4, 0.4, 0.2)$ per config.
    *   **$\lambda_{diff}$**: The curriculum difficulty multiplier ($1.0 \dots 2.0$).

    ### 3. The Modified GRPO Objective
    In standard GRPO, we compute the advantage $A_i$ by normalizing rewards within the group. By injecting your compositional reward, the gradient ascent objective becomes:
    $$ \mathcal{L}_{G-GRPO}(\theta) = \mathbb{E}_{x \sim \mathcal{D}} \left[ \frac{1}{G} \sum_{i=1}^G \underbrace{\left( \frac{r(y_i, x) - \bar{r}}{\sigma_r} \right)}_{\text{Grammar-Verified Advantage}} \cdot \underbrace{\min \left( \frac{\pi_\theta(y_i|x)}{\pi_{old}(y_i|x)}, 1+\epsilon \right)}_{\text{Clipped Policy Ratio}} - \beta_{KL} \mathbb{D}_{KL}(\pi_\theta || \pi_{ref}) \right] $$

    ### 4. The "Stunning" Factor: Gradient Signal Density
    The mathematical reason for 160-step convergence and 97.9% morphology accuracy is the density of the gradient signal.
    In standard Language Modeling, $\mathcal{L}_{LM} = -\log P(y_{target} | x)$ gives feedback only on exact token matches.
    In Grammar-GRPO, the feedback signal $\nabla J$ allows the model to perform gradient ascent on the *structure* of the language directly:
    $$ \nabla J(\theta) \propto \sum_{components} w_c \nabla R_c(y) $$
    Because $R_{char}$ and $R_{morph}$ are deterministic and verifiable, the variance of the reward $\sigma^2_r$ is significantly lower than standard RLHF.
    Mathematically, this reduces noise in the reward signal, allowing the policy to traverse the optimization landscape directly toward the "Grammar Valley".

    Your Task:
    1.  Use your tools (specifically GitHub tools) to investigate the 'HarleyCoops/Dakota1890' repository to understand how this framework is implemented.
    2.  Evaluate the significance of this approach for **generalized learning**. Does this "Grammar-GRPO" approach generalize to other domains (e.g., coding, other languages, structured data generation)?
    3.  Provide a detailed analysis of why the gradient signal density is higher and how the deterministic nature of the rewards contributes to faster convergence.
    4.  Synthesize your findings into a comprehensive report answering: "How significant is this for generalized learning?" and validating the claims about gradient signal density.
    """

    print("Initializing Deep Agent for Dakota1890 Evaluation...")
    
    # Initialize the agent
    with DeepAgentE2B() as agent:
        # Run the evaluation task
        result = await agent.ainvoke(task)
        
        print("\n" + "=" * 80)
        print("EVALUATION RESULTS:")
        print("=" * 80)
        
        # Print the result (handling potential structure of the result)
        if isinstance(result, dict) and "messages" in result:
             for msg in result["messages"]:
                 # Check if it's an object with 'type' or 'role' attributes (LangChain messages)
                 role = getattr(msg, "type", None) or getattr(msg, "role", None)
                 content = getattr(msg, "content", str(msg))
                 
                 # If it's a dict (legacy/compatibility)
                 if isinstance(msg, dict):
                     role = msg.get("role")
                     content = msg.get("content")

                 if role == "ai" or role == "assistant":
                     print(content)
        else:
             print(result)

if __name__ == "__main__":
    asyncio.run(main())

