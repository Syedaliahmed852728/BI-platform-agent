# DeepAgent BI Platform

> A production-ready, self-improving, multi-tenant Agentic Business Intelligence platform that learns from every successful interaction.

DeepAgent BI Platform is an enterprise-grade AI system that enables natural language analytics over multiple client databases. Instead of relying solely on prompting, the platform continuously improves itself by learning reusable SQL reasoning patterns, business rules, and successful query executions.

The result is an AI system that becomes faster, smarter, and more accurate over time without retraining the language model.

---

# Features

- Multi-tenant architecture
- Self-improving AI agent
- Runtime semantic orchestration
- Redis Vector Search memory
- Automatic SQL generation
- Business domain routing
- Entity resolution engine
- Background memory consolidation
- Production-ready FastAPI services
- LangGraph / DeepAgent orchestration
- SQL validation before execution
- Client-isolated semantic memory
- Extensible business domains

---

# High-Level Architecture

```
                   User
                     │
                     ▼
        Runtime Orchestration Middleware
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
 Semantic Memory Hit        DeepAgent Pipeline
        │                         │
        ▼                         ▼
 Return Answer        Entity Resolution
                               │
                               ▼
                       Domain Detection
                               │
                               ▼
                     Retrieve Similar Examples
                               │
                               ▼
                        SQL Generation
                               │
                               ▼
                         SQL Validation
                               │
                               ▼
                         Execute Query
                               │
                               ▼
                        Generate Response
                               │
                               ▼
                     Learning Queue (Redis)
                               │
                               ▼
                     Consolidation Worker
                               │
                               ▼
                 Redis Vector Memory Update
```

---

# Core Components

## Runtime Orchestration Middleware

Every user request first passes through the orchestration middleware.

Instead of invoking the LLM immediately, the middleware searches the semantic memory for previously solved examples.

If a highly similar execution exists, the middleware can:

- return the answer immediately
- reuse previous SQL
- inject previous reasoning into the prompt
- completely skip expensive SQL generation

This dramatically reduces:

- latency
- token usage
- LLM cost

---

## Self-Improving Memory

Unlike traditional RAG systems that only retrieve documents, DeepAgent learns from successful executions.

Each successful interaction is transformed into reusable knowledge.

Examples include:

- SQL patterns
- business reasoning
- entity mappings
- reusable prompts
- successful query structures

Over time the agent naturally becomes more capable.

No model fine-tuning is required.

---

## Redis Semantic Memory

The platform stores reusable knowledge inside Redis Vector Search.

Each memory contains:

- Question
- Embedding
- Business domain
- Generated SQL
- Reasoning
- Final answer
- Metadata
- Client identifier

Semantic search retrieves the most relevant examples during future requests.

---

## Entity Resolution

The entity resolution service keeps Redis synchronized with every client database.

Features include:

- fuzzy matching
- normalization
- aliases
- typo correction
- scheduled refreshes
- client isolation

This eliminates unnecessary SQL lookups during entity discovery.

---

## Background Learning Pipeline

Successful interactions are not immediately stored.

Instead they are queued.

```
Question
      ↓
Redis Stream
      ↓
Worker
      ↓
Batch Consolidation
      ↓
LLM Compression
      ↓
High Quality Example
      ↓
Redis Vector Store
```

This produces significantly higher quality memories while avoiding duplicate examples.

---

## Multi-Tenant Architecture

Every client is completely isolated.

```
Client A
    ├── SQL Database
    ├── Entity Cache
    ├── Vector Memory
    └── Examples

Client B
    ├── SQL Database
    ├── Entity Cache
    ├── Vector Memory
    └── Examples
```

No information leaks across clients.

---

# Supported Business Domains

The platform is designed to support independent business skills.

Current domains include:

- Sales
- Inventory
- Purchase Orders
- Customer Finance
- Delivery
- General Ledger

Adding new domains requires only a new business skill and schema definition.

---

# Technology Stack

## AI

- OpenAI GPT
- LangGraph
- DeepAgents
- LangChain

## Backend

- FastAPI
- Python

## Database

- SQL Server
- Redis
- Redis Vector Search

## AI Infrastructure

- Embeddings
- Semantic Search
- Runtime Memory
- Background Workers

---

# Learning Workflow

```
User Question
      │
      ▼
DeepAgent
      │
      ▼
Generate SQL
      │
      ▼
Execute SQL
      │
      ▼
Successful Result
      │
      ▼
Redis Queue
      │
      ▼
Consolidation Worker
      │
      ▼
Reusable Semantic Memory
      │
      ▼
Future Requests Become Faster
```

---

# Why This Project?

Traditional AI SQL assistants solve each question independently.

DeepAgent continuously learns from successful executions.

Instead of repeatedly solving the same problems, it remembers them.

The more it is used, the better it performs.

This creates an enterprise AI platform that continuously improves while maintaining strict tenant isolation and production-grade reliability.

---

# Future Roadmap

- Memory quality scoring
- Automatic memory pruning
- SQL regression testing
- Human feedback learning
- Reasoning memory
- Business rule memory
- Failure memory
- Cross-agent collaboration
- Distributed workers
- Hybrid retrieval
- Observability dashboard
- Agent evaluation framework

---

# License

MIT License