# Camera Test App

A small, standalone Flask app for testing browser camera capture. It is
separate from the main ChatBerry chatbot and has its own dependencies.

It serves a mobile-friendly page that opens your device's camera (front or
rear), lets you snap a photo, and uploads it to the Flask backend, which
saves it under `static/captures/` and lists it in a `/gallery` view.

## Why a web app

Native Python doesn't run directly on mobile. The practical way to get a
"simple Python app with camera use that runs on mobile" is a Python (Flask)
backend paired with the browser's built-in camera API (`getUserMedia`),
since every modern mobile browser (Safari on iOS, Chrome on Android)
supports it. Open the page on a phone and it behaves like a native camera
app, no app store or build step needed.

## Setup

```bash
cd camera-test-app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

This starts an HTTPS server on `https://0.0.0.0:5000` using a self-signed
certificate. HTTPS (or `localhost`) is required — browsers block camera
access on plain HTTP for any other host.

## Test on desktop

Open `https://localhost:5000` in your browser. Accept the self-signed
certificate warning, then allow camera access when prompted.

## Test on mobile

1. Make sure your phone and the computer running the app are on the **same
   Wi-Fi network**.
2. Find the computer's local IP address (e.g. `192.168.1.42`):
   - macOS/Linux: `ifconfig` or `ip addr`
   - Windows: `ipconfig`
3. On your phone's browser, go to `https://<your-ip>:5000`.
4. Accept the self-signed certificate warning (browsers show an "advanced /
   proceed anyway" option).
5. Allow camera access when prompted, then tap **Capture Photo**.

If your phone isn't on the same network as the machine running the app
(for example, when the app is running in a remote/cloud dev environment),
expose it with a tunnel that provides HTTPS, such as:

```bash
ngrok http 5000
```

or [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/):

```bash
cloudflared tunnel --url https://localhost:5000
```

Then open the tunnel's HTTPS URL on your phone.

## Endpoints

- `GET /` — camera capture page
- `POST /capture` — accepts `{"image": "data:image/jpeg;base64,..."}` and
  saves the photo
- `GET /gallery` — thumbnail grid of everything captured so far

## Notes

- Captured photos are written to `static/captures/` and are git-ignored.
- Use the **Switch Camera** button to toggle between front and rear
  cameras on devices that have both.
