from flask import Flask, request
import razorpay

app = Flask(__name__)

client = razorpay.Client(auth=("rzp_test_SP4S084OvRUPj2", "yjBcrsjg1dodn8j3BWdVuxYE"))

device_status = {
    "chair_01": "OFF"
}

@app.route("/")
def home():
    return "Server Running"


@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.json
    print("Webhook received:", data)

    if data and data.get("event") == "payment.captured":
        print("Payment Success")
        device_status["chair_01"] = "ON"

    return {"status": "ok"}


@app.route("/device/<device_id>")
def device(device_id):

    status = device_status.get(device_id, "OFF")

    if status == "ON":
        device_status[device_id] = "OFF"
        return "ON"

    return "OFF"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
