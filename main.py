import network
import urequests
import time
from machine import Pin

# --- CONFIG ---
TOUCH_PIN = 14       # GPIO14 = D5 on NodeMCU
LED_PIN = 12         # GPIO12 = D6
WEBHOOK_URL = 'https://discord.com/api/webhooks/your_webhook_url_here'
WIFI_SSID = 'YourWiFiSSID'
WIFI_PASSWORD = 'YourWiFiPassword'

# --- SETUP ---
touch = Pin(TOUCH_PIN, Pin.IN)
led = Pin(LED_PIN, Pin.OUT)

# --- CONNECT TO WIFI ---
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("Connected to WiFi:", wlan.ifconfig())

# --- SEND DISCORD WEBHOOK ---
def send_webhook():
    payload = {"content": "🚪 Door touched! <@390265556357611521>"}
    try:
        r = urequests.post(WEBHOOK_URL, json=payload)
        r.close()
        print("Webhook sent.")
    except Exception as e:
        print("Failed to send webhook:", e)

# --- MAIN LOOP ---
connect_wifi()
last_touch_time = 0
cooldown = 2  # seconds

while True:
    if touch.value() == 1:
        now = time.time()
        if now - last_touch_time > cooldown:
            print("Touch detected!")
            led.value(1)
            send_webhook()
            time.sleep(1)
            led.value(0)
            last_touch_time = now
    time.sleep(0.1)