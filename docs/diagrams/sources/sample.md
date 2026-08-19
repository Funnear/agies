# Sample diagram

Reference template for this repo's Mermaid setup. It doubles as a smoke test:
[tools/shell_scripts/gen_diagrams.sh](../../../tools/shell_scripts/gen_diagrams.sh) pulls the first
fenced Mermaid code block out of every file under `docs/diagrams/sources/` and renders it to
`docs/diagrams/images/<same path>.png` using [theme.json](../theme.json). The extraction is
line-based and gets confused by a second fenced Mermaid block (or even the literal fence text
appearing elsewhere in the file), so keep exactly one such block per source file — copy this file
as a starting point for a new diagram rather than appending to this one.

The flowchart below is a mock data/ML pipeline ("Customer Churn Predictor") built to exercise the
Mermaid flowchart elements you'll reach for most often in this kind of project:

- **Node shapes** — process `[ ]`, terminal/stadium `( )`, decision `{ }`, database `[( )]`,
  subroutine `[[ ]]`, external system `{{ }}`, input `>]`, circle `(( ))`, parallelogram `[/ /]`
- **Edge styles** — solid `-->`, thick `==>`, dotted `-.->`, and both inline (`-- label -->`) and
  piped (`-->|label|`) edge labels
- **Structure** — subgraph grouping with per-subgraph direction, cross-subgraph edges, and a
  feedback loop back to an earlier stage
- **Styling** — `classDef` / `class` to color nodes by role, plus `%%` comments

```mermaid
%% Mock project: "Customer Churn Predictor" — end-to-end ML pipeline.
%% This is the block gen_diagrams.sh renders into docs/diagrams/images/sample.png
flowchart TD
    subgraph SRC["Data Sources"]
        direction LR
        crm[(CRM Database)]
        billing{{Billing API}}
        exports>Raw CSV Exports]
    end

    subgraph ENG["Data Engineering"]
        direction TB
        ingest[Ingest Raw Data]
        validate{Schema valid?}
        badschema[Alert: Bad Schema]
        clean[Clean & Normalize]
        features[[Build Features]]
        featurestore[(Feature Store)]
    end

    subgraph DEV["Model Development"]
        direction TB
        split((Train / Test Split))
        train[Train Candidate Model]
        evaluate{Metrics ≥ threshold?}
        tune[Hyperparameter Tuning]
    end

    subgraph DEPLOY["Deployment"]
        direction TB
        package[Package Model Artifact]
        stage([Staging Rollout])
        prod([Production Rollout])
        rollback[/Rollback/]
    end

    subgraph MON["Monitoring & Feedback"]
        direction TB
        drift{Data drift detected?}
        healthy[Model Healthy]
        retrain[Trigger Retraining]
    end

    %% -- happy path (thick) --
    crm ==> ingest
    exports --> ingest
    billing -.->|nightly sync| ingest
    ingest --> validate
    validate -- yes --> clean
    validate -- no --> badschema
    clean --> features
    features --> featurestore
    featurestore ==> split
    split ==> train
    train --> evaluate
    evaluate -- no --> tune
    tune --> train
    evaluate -- yes --> package
    package --> stage
    stage --> prod

    %% -- monitoring + feedback loop --
    prod -.-> drift
    drift -- no --> healthy
    drift -- yes --> retrain
    retrain -.->|retrain trigger| ingest
    prod --> rollback
    rollback --> stage

    %% -- styling --
    classDef store fill:#1b3442,stroke:#40e0d0,color:#e9eef2;
    classDef decision fill:#253f4f,stroke:#40e0d0,color:#e9eef2,stroke-width:2px;
    classDef terminal fill:#10212b,stroke:#40e0d0,color:#e9eef2,stroke-width:2px;
    classDef alertNode fill:#5a1f1f,stroke:#ff6b6b,color:#ffe9e9;

    class crm,featurestore store
    class validate,evaluate,drift decision
    class stage,prod,healthy terminal
    class badschema alertNode
```

## Rendering this file

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
"$REPO_ROOT/tools/shell_scripts/gen_diagrams.sh"
```

Output lands at `docs/diagrams/images/sample.png`, rendered with the repo's dark theme
(transparent background, teal accents from [theme.json](../theme.json)). Mindmap sources are the
one exception — the script auto-detects the mindmap keyword and renders those on a solid white
background instead, since mindmap's default styling doesn't hold up on the dark theme.

## Starting a new diagram type

This file only demonstrates the flowchart, since that's what the pipeline safely renders today.
For other diagram types (sequence, class, ER, state, gantt, mindmap, …), create a new file under
`docs/diagrams/sources/` with a single fenced Mermaid block, e.g.:

```text
docs/diagrams/sources/
├── sample.md               # this file — flowchart reference
├── api_sequence.md         # sequenceDiagram example
└── model_lifecycle.md      # stateDiagram-v2 example
```

Each file gets its own PNG under `docs/diagrams/images/`, mirroring the source path.
