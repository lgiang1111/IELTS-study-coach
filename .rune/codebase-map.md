# Codebase Map

Generated: 2026-06-30T17:22:00+07:00

## Module Boundaries

| Module | Directory | Public API | Dependencies | Domain |
| :--- | :--- | :--- | :--- | :--- |
| **Agent Rules** | `.agent/rules/` | Quy tắc Rune cho Agent (onboard, cook, scout...) | none | Quy ước & hướng dẫn hoạt động của AI Agent |
| **Documentation** | `docs/` | agno_agent_lessons, cookbook, os_architecture | none | Hướng dẫn Framework & các kiến trúc mẫu |
| **System Designs** | (Root) | system_design_v3.md, system_design_multi_agent.md | Specs | Phân tích kiến trúc hệ thống và luồng dữ liệu |
| **Specifications** | (Root) | Specs-5565918f-f1cf-5191-bbb5-e43fc8cbf30d.md | none | Đặc tả các mô hình toán học (GA, fatigue, learning curve) |

## Dependency Graph (Mermaid)

```mermaid
graph TD
    UI[👤 User / Streamlit UI] --> Router{App Router: Regex Code}
    
    subgraph Multi-Agent Layer
        Router -- Chat thường --> Coach[🤖 IELTS Coach Agent]
        Router -- Lập lịch --> Planner[🤖 Planner Agent]
        Planner --> Reviewer[🔍 Reviewer Agent]
    end
    
    subgraph Tool / Engine Layer
        Planner -->|MCP Client| MCP[🔌 Local MCP Server]
        MCP --> GA[🔧 Genetic Algorithm Engine]
        MCP --> LC[🔧 Learning Curve Engine]
    end
    
    classDef agent fill:#f9f,stroke:#333,stroke-width:2px;
    classDef tool fill:#bbf,stroke:#333,stroke-width:1px;
    class Coach,Planner,Reviewer agent;
    class GA,LC tool;
```

## Domain Ownership

| Domain | Modules | Key Files |
| :--- | :--- | :--- |
| **Agent Orchestration** | Agno Agents | `system_design_v3.md`, `system_design_multi_agent.md` |
| **Optimization Engine** | Math/GA Engines | `Specs-5565918f-f1cf-5191-bbb5-e43fc8cbf30d.md` |
| **System Evaluation** | Research/Paper | `project_evaluation.md`, `Capstone Project.docx.md` |
| **Agent Standard Rules** | Rune Kit | `.agent/rules/rune-onboard.md`, `CLAUDE.md` |
