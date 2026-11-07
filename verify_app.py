# Flask for QR verification

from flask import Flask

verify_app = Flask(__name__)


@verify_app.get("/")
def home():
    return """
    <h1>Bouncer Verifier</h1>
    <p>Ready to scan your mom. /j</p>
    <button onclick="startScan()">Scan QR</button>

    <script src="https://unpkg.com/html5-qrcode"></script>
    <div id="reader"></div>

    <script>
    function startScan() {
    const scanner = new Html5Qrcode("reader");

    scanner.start(
        { facingMode: "environment" },
        { fps: 10, qrbox: 250 },
        decodedText => {
            alert("Scanned data: " + decodedText);
            scanner.stop();
        },
        errorMessage => {
            // Keep scanning
        }
        );
    }
    </script>
"""



if __name__ == "__main__":
    verify_app.run(
        host="0.0.0.0", 
        port=5000, 
        debug=True, 
        ssl_context="adhoc"
    )