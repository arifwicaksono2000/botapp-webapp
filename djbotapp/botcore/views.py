import requests, os
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from dotenv import load_dotenv
from .models import Segments

load_dotenv()

BOT_API_BASE = "http://127.0.0.1:9000"
BOT_TOKEN = os.getenv("BOT_API_TOKEN")
HEADERS = {"Authorization": f"Bearer {BOT_TOKEN}"}

@login_required
def dashboard_view(request):
    try:
        print("📤 Sending request to bot...")
        print("URL: http://127.0.0.1:9000/status")
        print("Headers:", HEADERS)
        resp = requests.get(f"{BOT_API_BASE}/status", headers=HEADERS, timeout=2)
        print("📬 Response:", resp.status_code, resp.text)

        bot_state = resp.json().get("state", "unknown")
    except Exception as e:
        print("❌ Error contacting bot:", e)
        bot_state = "offline"

    return render(request, "dashboard.html", {"bot_state": bot_state})

@login_required
def trades_view(request):
    headers = {"Authorization": f"Bearer {BOT_TOKEN}"}
    resp = requests.get(f"{BOT_API_BASE}/status", headers=headers)

    if resp.status_code != 200:
        trade_statuses = {}
    else:
        trade_statuses = resp.json()

    return render(request, "trades.html", {"trades": trade_statuses})

@login_required
def segments_view(request):
    segments_list = []
    try:
        segments = Segments.objects.select_related('subaccount', 'milestone').order_by('-opened_at')[:20]

        for segment in segments:
            segments_list.append({
                'id': segment.id,
                'uuid': str(segment.uuid),
                'subaccount_name': segment.subaccount.name if segment.subaccount else 'N/A',
                'milestone_id': segment.milestone.id if segment.milestone else 'N/A',
                'total_positions': segment.total_positions,
                'total_balance': float(segment.total_balance),
                'pair': segment.pair,
                'opened_at': segment.opened_at,
                'closed_at': segment.closed_at,
                'status': 'Open' if segment.closed_at is None else 'Closed',
            })
    except Exception as e:
        print(f"Error fetching segments for template: {e}")
        segments_list = []

    return render(request, "segments.html", {'initial_segments': segments_list})


@login_required
def start_trade(request):
    import requests, os
    if request.method == "POST":
        side = request.POST.get("side", "buy")
        volume = request.POST.get("volume", "1000")
        hold = request.POST.get("hold", "60")

        headers = {"Authorization": f"Bearer {BOT_TOKEN}"}

        data = {
            "side": side,
            "volume": volume,
            "hold": hold
        }

        resp = requests.post(f"{BOT_API_BASE}/start", headers=headers, params=data)
        if resp.status_code == 200:
            messages.success(request, "✅ Trade started!")
        else:
            messages.error(request, f"❌ Error starting trade: {resp.text}")

    return redirect('trades')


@login_required
def emergency_close(request):
    if request.method == "POST":
        try:
            r = requests.post(f"{BOT_API_BASE}/stop", headers=HEADERS)
            messages.warning(request, r.json().get("msg", "Emergency close issued"))
        except Exception as e:
            messages.error(request, f"❌ Failed: {e}")
    return redirect("dashboard")
    