# Coltex

**The AI Knowledge Platform for Modern Organizations**

Turn scattered business knowledge into AI-ready intelligence — runs locally in your browser.

## Install & run (localhost)

```cmd
cd Coltex-Knowledge-Platform
python -m venv .venv
.venv\Scripts\activate.bat
pip install -e .
coltex serve
```

Opens **http://127.0.0.1:8787** automatically.

Or just:

```cmd
coltex
```

(`coltex` with no arguments starts the localhost server.)

---

## What you get

| Page | Purpose |
|------|---------|
| **Dashboard** | Documents, embeddings, health, build workspace |
| **Workspace** | Create or open a `.ctex` workspace |
| **Knowledge** | Browse knowledge objects |
| **Sources** | Upload PDF, DOCX, MD, TXT, HTML, JSON |
| **Search** | Universal search |
| **Ask Knowledge** | Q&A with sources |
| **Settings** | Embedding model, chunk size, etc. |

No cloud. Everything runs on **127.0.0.1** on your machine.

---

## Workspace (.ctex)

From the **Workspace** page, click **Create** to make a new workspace, or **Open** with the path to your `.ctex` file:

```
C:\Users\you\Coltex-Knowledge-Platform\workspaces\MyWorkspace\MyWorkspace.ctex
```

Then use **Build Workspace** on the Dashboard to process documents and generate embeddings.

---

## Windows cmd quick start

```cmd
cd C:\Users\elija\Coltex-Knowledge-Platform
git pull origin main
.venv\Scripts\activate.bat
pip install -e .
coltex serve
```

---

## License

MIT — see [LICENSE](LICENSE).
