from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = "scoreboard_secret_key"

DATA_FILE = os.environ.get("DATA_FILE", "data/scores.json")

# In a real app this would be in a DB. For a simple lab scoreboard, a JSON file suffices.
# Format: {"team_name": {"score": 0, "flags": []}}

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Valid flags across the lab (hardcoded baseline, AI generator could update this later if it mutates flags, 
# but for now we'll accept any flag format or we can check against a list. Let's just accept any string starting with FLAG{ and assign 100 pts)
def is_valid_flag(flag):
    return flag.startswith("FLAG{") and flag.endswith("}")

@app.route("/", methods=["GET"])
def index():
    data = load_data()
    # Sort by score descending
    leaderboard = sorted([{"team": k, **v} for k, v in data.items()], key=lambda x: x["score"], reverse=True)
    return render_template("index.html", leaderboard=leaderboard)

@app.route("/admin", methods=["GET"])
def admin():
    return render_template("admin.html")

@app.route("/admin/generate", methods=["POST"])
def generate():
    provider = request.form.get("provider")
    api_key = request.form.get("api_key")
    if not api_key:
        flash("API Key is required.", "danger")
        return redirect(url_for("admin"))

    # Pass the key to the generator script
    import subprocess
    env = os.environ.copy()
    if provider == "anthropic":
        env["ANTHROPIC_API_KEY"] = api_key
    else:
        env["OPENAI_API_KEY"] = api_key

    script_path = "/project/infra/scripts/ai_vuln_generator.py"
    target_files = [
        "/project/labs/vulnbank/routes/main.py",
        "/project/labs/vulnbank/routes/auth.py",
        "/project/labs/vulnshop/routes/api.js"
    ]
    
    success = True
    for target in target_files:
        try:
            result = subprocess.run(
                ["python3", script_path, target],
                env=env,
                capture_output=True,
                text=True,
                timeout=120
            )
            if result.returncode != 0:
                success = False
                print(f"Error mutating {target}: {result.stderr}")
        except Exception as e:
            success = False
            print(f"Exception mutating {target}: {str(e)}")

    if success:
        # Restart the vulnerable containers
        try:
            import docker
            client = docker.from_env()
            for container_name in ["vulnbank", "vulnshop"]:
                try:
                    c = client.containers.get(container_name)
                    c.restart()
                except docker.errors.NotFound:
                    print(f"Container {container_name} not found.")
            flash("Successfully generated dynamic vulnerabilities and restarted apps!", "success")
        except Exception as e:
            flash(f"Generated vulnerabilities, but failed to restart containers: {str(e)}", "warning")
    else:
        flash("Failed to generate some vulnerabilities. Check server logs.", "danger")

    return redirect(url_for("admin"))

@app.route("/submit", methods=["POST"])
def submit():
    team = request.form.get("team", "").strip()
    flag = request.form.get("flag", "").strip()

    if not team or not flag:
        flash("Team name and flag are required.", "danger")
        return redirect(url_for("index"))

    if not is_valid_flag(flag):
        flash("Invalid flag format. Flags must start with FLAG{ and end with }.", "danger")
        return redirect(url_for("index"))

    data = load_data()
    
    if team not in data:
        data[team] = {"score": 0, "flags": []}
        
    if flag in data[team]["flags"]:
        flash("Flag already submitted by your team!", "warning")
        return redirect(url_for("index"))

    data[team]["flags"].append(flag)
    data[team]["score"] += 100
    save_data(data)

    flash(f"Flag accepted! 100 points awarded to {team}.", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)