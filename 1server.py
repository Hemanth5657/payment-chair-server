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


@app.route("/pay")
def pay():

    order = client.order.create({
        "amount": 100,
        "currency": "INR",
        "payment_capture": 1
    })

    order_id = order["id"]

    return f"""
<html>
<body>
<h2>Massage Chair Payment</h2>

<button id="paybtn">Pay Now</button>

<script src="https://checkout.razorpay.com/v1/checkout.js"></script>

<script>
var options = {{
    "key": "rzp_test_SP4S084OvRUPj2",
    "amount": "100",
    "currency": "INR",
    "name": "Massage Chair",
    "description": "Usage Payment",
    "order_id": "{order_id}",
    "handler": function (response){{
        alert("Payment Successful");
    }}
}};

var rzp = new Razorpay(options);

document.getElementById('paybtn').onclick = function(e){{
    rzp.open();
    e.preventDefault();
}}
</script>

</body>
</html>
"""


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