import pandas as pd
import numpy as np
from typing import Dict, Any, List
from google.adk.agents import Agent
# from google.adk.tools import Tool # Correct import for Tool
# from google.adk.tools.agent_tool import AgentTool
# from google.adk.tools.agent_tool import Tool
from google.adk.tools.agent_tool import AgentTool as Tool
# --- 1. Define the Corrected Tool Function ---

def analyse_triangle(csv_path: str, metric: str = "paid") -> Dict[str, Any]:
    """
    Analyzes a long-format claims triangle CSV to compute link ratios, 
    volume-weighted averages, and identify outliers.

    Args:
        csv_path (str): File path to the claims triangle data (CSV format).
        metric (str): The column name representing the claim metric 
                      (e.g., 'paid', 'incurred', 'count'). Defaults to 'paid'.

    Returns:
        Dict[str, Any]: A structured dictionary containing summary statistics 
                        (Volume-Weighted Link Ratios, Std Dev) and a list of outliers.
    """
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        return {"error": f"File not found at path: {csv_path}"}
    
    # --- Input Validation (Improved) ---
    required_cols = {"accident_period", "dev_month"}
    
    # Ensure all required columns exist and the metric column is present
    if not required_cols.issubset(df.columns) or metric not in df.columns:
        missing = required_cols.union({metric}) - set(df.columns)
        return {"error": f"Missing required columns: {missing}. Available: {list(df.columns)}"}

    # Ensure accident_period is treated as a string for grouping and dev_month is integer
    df["dev_month"] = pd.to_numeric(df["dev_month"], errors='coerce').astype('Int64')
    df = df.dropna(subset=["dev_month"])
    
    df = df.sort_values(["accident_period", "dev_month"])
    
    # --- Link Ratio and Next Value Calculation ---
    df["next_val"] = df.groupby("accident_period")[metric].shift(-1)
    
    # Use .replace(0, np.nan) to prevent division by zero, which is critical for link ratios
    df["link_ratio"] = df["next_val"] / df[metric].replace(0, np.nan) 

    ratios = df.dropna(subset=["link_ratio"]).copy()

    summary: Dict[int, Any] = {}
    outliers: List[Dict[str, Any]] = []

    # --- Link Ratio Aggregation and Outlier Detection ---
    for dev, part in ratios.groupby("dev_month"):
        
        # 1. Volume Weighted Average (Professional Standard)
        # Sum of numerators divided by sum of denominators
        numerator_sum = part["next_val"].sum()
        denominator_sum = part[metric].sum()
        
        # Calculate the Volume Weighted Average Link Ratio (VWADF)
        vwadf = numerator_sum / denominator_sum if denominator_sum != 0 else np.nan
        
        # Calculate standard deviation on individual link ratios (for outlier detection)
        # Note: The outlier detection logic remains based on individual link ratios
        mu_outlier_calc = part["link_ratio"].mean()
        sigma = part["link_ratio"].std(ddof=0) or 1e-9

        # Z-score calculation for outlier flagging
        part["z"] = (part["link_ratio"] - mu_outlier_calc) / sigma
        
        # Outlier threshold remains > 2.5 std devs
        part["is_outlier"] = part["z"].abs() > 2.5 

        # --- Populate Summary ---
        summary[int(dev)] = {
            "volume_weighted_link_ratio": round(float(vwadf), 4) if not np.isnan(vwadf) else None,
            "std_dev_of_ratios": round(float(sigma), 4),
            "count": int(len(part)),
            "outliers_found": int(part["is_outlier"].sum()),
        }

        # --- Populate Outliers List ---
        for _, row in part[part["is_outlier"]].iterrows():
            outliers.append({
                "accident_period": str(row["accident_period"]),
                "dev_month_start": int(row["dev_month"]),
                "link_ratio": round(float(row["link_ratio"]), 4),
                "current_value": round(float(row[metric]), 2),
                "next_value": round(float(row["next_val"]), 2),
                "z_score": round(float(row["z"]), 2),
            })

    return {
        "metric": metric,
        "summary_by_dev_month": summary,
        "outliers": outliers,
    }


# --- 2. Tool Registration ---
# analyse_triangle_tool = Tool(
#     name="analyse_triangle",
#     description="Analyzes long-format triangle CSV (accident_period, dev_month, metric) to compute volume-weighted link ratios and identify outliers (Z > 2.5). Requires csv_path and metric (e.g., 'paid').",
#     func=analyse_triangle,
# )

# analyse_triangle_tool = Tool(
#     description="Analyzes long-format triangle CSV (accident_period, dev_month, metric) to compute volume-weighted link ratios and identify outliers (Z > 2.5). Requires csv_path and metric (e.g., 'paid').",
#     func=analyse_triangle,
#     # The name will now be automatically derived from the function name 'analyse_triangle'
# )


# --- 3. Agent Definition (No changes needed, but placed here for context) ---
root_agent = Agent(
    name="greeting_agent",
    # https://ai.google.dev/gemini-api/docs/models
    model="gemini-2.0-flash",
    description=(
        "An actuarial reserving assistant specialising in paid/incurred "
        "triangles, development factors, outlier detection and trend analysis."
    ),
    instruction=(
        "You are an expert non-life insurance reserving actuary.\n\n"
        "Context:\n"
        "- Input data is claims triangles by accident period (rows) and development month (columns).\n"
        "- Diagonals correspond to calendar months.\n"
        "- Metrics include paid, incurred, claim counts and derived link ratios.\n\n"
        "What to do:\n"
        "- Ask the user for a CSV path or description if not provided.\n"
        "- Use the analyse_triangle tool to compute development factors and outliers.\n"
        "- Explain key trends by accident period, development step and calendar period.\n"
        "- Highlight material outliers and plausible external drivers (inflation, regulation, COVID, "
        " operational changes) but be explicit about uncertainty.\n"
        "- Produce concise, business-ready summaries suitable for reserving decks and management reports."
    ),
    tools=[analyse_triangle],
)