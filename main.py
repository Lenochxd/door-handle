import network
import urequests
import time
from machine import Pin

# --- CONFIG ---
TOUCH_PIN = 14       # GPIO14 = D5 on NodeMCU
LED_PIN = 12         # GPIO12 = D6
WIFI_SSID = 'YourWiFiSSID'
WIFI_PASSWORD = 'YourWiFiPassword'
WEBHOOK_URL = 'http://192.168.3.8:5050/door'

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
    if not network.WLAN(network.STA_IF).isconnected():
        print("Wi-Fi not connected, reconnecting...")
        connect_wifi()

    payload = {"touched": True}
    try:
        r = urequests.post(WEBHOOK_URL, json=payload, headers={"Content-Type": "application/json"})
        if r.status_code == 200:
            print("Webhook sent successfully!")
        else:
            print("Failed to send webhook:", r.status_code, r.text)
        r.close()
        print("Webhook sent.")
    except Exception as e:
        print("Failed to send webhook:", e)

def wait_for_stable_touch():
    count = 0
    for _ in range(10):
        if touch.value() == 1:
            count += 1
        time.sleep(0.01)
    return count >= 8  # 80% stable touch

# --- MAIN LOOP ---
connect_wifi()
last_touch_time = 0
cooldown = 2  # seconds

while True:
    if touch.value() == 1 and wait_for_stable_touch():
        now = time.time()
        if now - last_touch_time > cooldown:
            print("Touch detected!")
            led.value(1)
            send_webhook()
            time.sleep(1)
            led.value(0)
            last_touch_time = now
    time.sleep(0.07)