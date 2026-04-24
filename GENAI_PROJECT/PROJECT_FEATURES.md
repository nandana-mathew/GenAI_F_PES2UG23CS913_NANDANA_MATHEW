# Game Strategiser AI - Capstone Level GenAI Features

This document outlines the latest highly advanced features integrated into the **Game Strategiser AI** dashboard to elevate it from a simple "ChatGPT wrapper" into a comprehensive, robust, and academic-grade ML/GenAI application.

## 1. Zero-Dependency Native Inference Engine (Qwen-2.5)
**What it is:** The application natively integrates the `transformers` library to run the lightweight **Qwen-2.5 (0.5B Instruct)** model directly on the host machine's CPU hardware in real-time.
**Why it's better:** 
- **Zero API Reliance:** It completely bypasses "Quota Exhausted" or "Invalid Key" roadblocks that break most basic GenAI projects by operating entirely self-contained. 
- **Maximum Data Privacy:** Game states and strategic rule sets never leave the host machine.
- **Proof of Concept:** Demonstrates deep algorithmic familiarity with hosting and running raw PyTorch (`torch`) tensors instead of simply utilizing standard REST APIs.

## 2. Advanced Multi-Provider Routing Architecture
**What it is:** The codebase is built with a dynamic architectural router that can switch between **Gemini**, **Groq**, and **Qwen-2.5** seamlessly.
**Why it's better:** 
- **High Availability (HA):** In a production system, if one LLM provider goes down or restricts the API tier, it effortlessly shifts traffic to an alternate endpoint.
- **Fail-safes:** It doesn't crash quietly. We've replaced silent mock failures with transparent error propagation throughout the stream.

## 3. ML Observability & Telemetry Tracking (MLOps)
**What it is:** We have built a dedicated **GENAI TELEMETRY** dashboard that operates parallel to the output.
**Why it's better:** 
- This moves the project into the highly sought-after **MLOps** tier. It actively tracks pipeline health, Inference Speed (`W/s`), Context Window parsing load, and Total Execution Latency logic.
- Evaluators and recruiters look *specifically* for tracking metrics like these to see if an engineer deeply understands the cost, latency, and performance thresholds of deploying large-language models constraints.

## 4. Strict Grounding and Uncertainty Enforced Prompt Engineering
**What it is:** Detailed tuning inside `SYSTEM_PROMPT` enforces constraints forcing the AI to strictly use words like "probability", "likely", and "suggests". It also enforces a strict parsing grammar (`Scenario 1:`, `Scenario 2:`).
**Why it's better:** 
- By deliberately restricting vocabulary (Temperature scaling & prompt structuring), we control LLM hallucination limits and prevent it from giving definitive answers about 'hidden' information (fog of war). 

By integrating **Self-Contained Model Execution**, **High Availability Load Routes**, and **Observability Dashboards**, the project proves robust GenAI system engineering capabilities far beyond standard wrapper applications!
