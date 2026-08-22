# UML diagrams

## Create diagrams

- Store in docs/diagrams/sources
- Give `.md` file extension

```markdown
    # Mandatory 1st level header

    ```mermaid
        diagram code
        %% comments
    ```
```

## Open preview

[macOS]
Press  
**Cmd + Shift + V** → Markdown Preview  
or  
**Cmd + K, V** → Side-by-side preview  

[Windows, linux]
Press  
**Ctrl + Shift + V** → Markdown Preview  
or  
**Ctrl + K, V** → Side-by-side preview  

Or click:  
**“Open Preview to the Side”** button in top-right corner.

## Render diagrams

```sh
make diagrams
```
