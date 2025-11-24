#
#& 1. CRITICAL PREREQUISITES: Python Versions
#? dbt and some dependencies (like maturin/Rust builds) are not fully stable on Python 3.12. Python 3.11 is the recommended version.

#* Step 1: Install Python 3.11
   - Download from python.org or use WinGet.
   - On Windows, check "Add to PATH" during installation.
   - If using WinGet, enable "App execution aliases" in Windows Settings if prompted.

#* Step 2: Avoid Conflicts
   - You can keep Python 3.12 and 3.11 side‑by‑side.
   - Use the `py` launcher to target 3.11 explicitly.
   - Commands: `py --list` (shows installed versions), `py --version` (shows default).

#& 2. SETTING UP THE VIRTUAL ENVIRONMENT (VENV)
#? venv creates an isolated folder for dependencies, avoiding conflicts with system Python.

#* Step 1: Create the Project Folder
   mkdir dbt_project
   cd dbt_project

#* Step 2: Create the venv using Python 3.11
   py -3.11 -m venv venv
   
   #! to remove the env
   rm -rf venv

#& 3. ACTIVATING THE ENVIRONMENT (Scripts vs bin)
#? Windows venv → `Scripts` folder.  
#? Linux/macOS venv → `bin` folder.  
#? Git Bash on Windows still uses the Windows folder name (`Scripts`), but paths must use forward slashes.

#* Option A: PowerShell (Recommended in VS Code)
   venv\Scripts\Activate.ps1

#* Option B: Git Bash (on Windows)
   source venv/Scripts/activate
   # Note: "Scripts" must be capitalized.

#* Option C: Linux/macOS
   source venv/bin/activate

#* Verify Activation
   - Prompt shows `(venv)` prefix.
   - Run `python --version` → should show Python 3.11.x.
   
#& Deactivation:
   deactivate
#* only works after activation

#& 4. INSTALLING DBT
#? Upgrade pip/setuptools/wheel first to avoid build errors.

#* Step 1: Upgrade core tools
   pip install --upgrade pip setuptools wheel

#* Step 2: Install dbt with Postgres Adapter
   pip install dbt-postgres

#* Step 3: Verify Installation
   dbt --version
   # Shows dbt Core + Postgres adapter.

#& 5. TROUBLESHOOTING: "Command not found" in Git Bash
#? Git Bash doesn’t automatically see Windows `.exe` files in `Scripts`.

#* Solution A: Run directly via path
   ./venv/Scripts/dbt.exe --version

#* Solution B: Export PATH (temporary)
   export PATH=$PATH:./venv/Scripts/

#* Solution C: Use PowerShell
   PowerShell handles PATH correctly after activation.

#& 6. INITIALIZING THE PROJECT
#* Run:
   dbt init my_dbt_project
   # Choose adapter (e.g., [1] for postgres).

#& 7. CONFIGURING DATABASE CONNECTION (profiles.yml)
#? File is created in `~/.dbt/profiles.yml` (Windows: `C:\Users\<User>\.dbt\profiles.yml`).

#* Common Prompts:
   - host: localhost
   - port: 5432
   - user: postgres
   - password: <your_password>
   - dbname: <your_database>
   - schema: public

#* Fix Host Error:
   1. Open `~/.dbt/profiles.yml`.
   2. Change `host: ibrahim` → `host: localhost`.
   3. Run `dbt debug`.

#& 8. CLEANUP & RESETTING
#? Safe to delete and recreate if misconfigured.

#* Reset Project:
   deactivate
   rm -rf custom_postgres   # or Remove-Item in PowerShell
   source venv/Scripts/activate
   dbt init new_project_name

#* Reset venv:
   deactivate
   rm -rf venv
   py -3.11 -m venv venv


custom_postgres:
  outputs:
    dev:
      dbname: destination_db
      host: host.docker.internal
      pass: secret
      port: 5434
      schema: public
      threads: 1
      type: postgres
      user: postgres
  target: dev