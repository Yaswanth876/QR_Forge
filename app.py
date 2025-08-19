from flask import Flask, render_template, request, send_file, session
import qrcode
import io
import base64

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session storage

@app.route("/", methods=["GET", "POST"])
def index():
    qr_code = None
    if request.method == "POST" and "generate" in request.form:
        data = request.form["data"]
        if not data.strip():
            return render_template("index.html", error="Please enter text or URL")

        # Generate QR code
        qr = qrcode.make(data)
        img_io = io.BytesIO()
        qr.save(img_io, "PNG")
        img_io.seek(0)

        # Save image in session (base64)
        session["qr_data"] = base64.b64encode(img_io.getvalue()).decode("utf-8")

        # Display QR in HTML
        qr_code = f"data:image/png;base64,{session['qr_data']}"

    return render_template("index.html", qr_code=qr_code)

@app.route("/download")
def download():
    if "qr_data" not in session:
        return "No QR code generated yet", 400
    
    img_bytes = base64.b64decode(session["qr_data"])
    return send_file(io.BytesIO(img_bytes), mimetype="image/png",
                     as_attachment=True, download_name="qrcode.png")

if __name__ == "__main__":
    app.run(debug=True)
