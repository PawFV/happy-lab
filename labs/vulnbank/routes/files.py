from flask import Blueprint, request, redirect, session, send_file
import os

from db import get_db_connection
from templates import render

bp = Blueprint("files", __name__)


# VULN: Unvalidated File Upload
@bp.route("/upload", methods=["GET", "POST"])
def upload():
    msg = ""
    if request.method == "POST":
        if "user_id" not in session:
            return redirect("/login")

        file = request.files.get("file")
        if file:
            # VULNERABLE: does not validate extension or content
            upload_dir = "uploads"
            os.makedirs(upload_dir, exist_ok=True)
            filepath = os.path.join(upload_dir, file.filename)
            file.save(filepath)

            db = get_db_connection()
            db.execute(
                "INSERT INTO files (user_id, filename, filepath) VALUES (%s, %s, %s)",
                (session["user_id"], file.filename, filepath),
            )
            db.commit()
            msg = f"<p class='success'>Document uploaded: {file.filename}</p>"

    return render(
        "Document Upload",
        f"""
        <p>Please upload your identification documents here.</p>
        {msg}
        <form method='POST' enctype='multipart/form-data'>
            <input type='file' name='file'>
            <button type='submit'>Upload</button>
        </form>
        """,
    )


# VULN: Path Traversal on download
@bp.route("/download")
def download():
    filename = request.args.get("file", "")
    if filename:
        # VULNERABLE: path traversal, no sanitization of input
        filepath = os.path.join("uploads", filename)
        try:
            return send_file(filepath)
        except Exception as e:
            return f"Error: {e}", 404

    return render(
        "Download Document",
        """
        <p>Enter document ID to download:</p>
        <form method='GET'>
            <input name='file' placeholder='Document name...'>
            <button type='submit'>Download</button>
        </form>
        """,
    )
