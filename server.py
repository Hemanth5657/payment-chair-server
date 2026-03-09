from flask import Flask, redirect, request
import razorpay
import requests

app = Flask(__name__)

# Razorpay API keys
client = razorpay.Client(auth=("YOUR_KEY_ID", "YOUR_SECRET"))

# NodeMCU IP
ESP_IP = "192.168.137.31"

last_payment_id = None


# QR scan route
@app.route("/pay")
def pay():

    order = client.order.create({
        "amount": 100,   # ₹1 = 100 paise
        "currency": "INR",
        "payment_capture": 1
    })

    order_id = order["id"]

    payment_url = f"https://checkout.razorpay.com/v1/checkout.js?order_id={order_id}"

    return redirect(payment_url)


# Razorpay webhook
@app.route('/webhook', methods=['POST'])
def webhook():

    global last_payment_id

    data = request.json
    print("Webhook received:", data)

    if data and data.get("event") == "payment.captured":

        payment = data["payload"]["payment"]["entity"]
        payment_id = payment["id"]

        if payment_id == last_payment_id:
            print("Duplicate ignored")
            return {"status": "duplicate"}

        last_payment_id = payment_id

        print("Payment Success")

        try:
            requests.get(f"http://{ESP_IP}/start")
            print("Relay Trigger Sent")
        except:
            print("ESP not reachable")

    return {"status": "ok"}


app.run(host="0.0.0.0", port=5000)