from flask import Flask, jsonify, render_template_string, request

from node import Node
from network import Network


app = Flask(__name__)

network = Network()

home = Node("Home")
hilltop = Node("Hilltop")
town = Node("Town")
south_relay = Node("SouthRelay")
community = Node("CommunityCenter")

for node in [
    home,
    hilltop,
    town,
    south_relay,
    community,
]:
    network.add_node(node)

home.connect(hilltop)
hilltop.connect(town)

home.connect(south_relay)
south_relay.connect(town)

town.connect(community)


messages = []


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>GNOMEMESH</title>

    <meta name="viewport"
          content="width=device-width, initial-scale=1">

    <style>
        body {
            background: #102016;
            color: #f0f5e8;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }

        h1 {
            text-align: center;
            font-size: 32px;
        }

        .subtitle {
            text-align: center;
            color: #b8c9a8;
            margin-bottom: 25px;
        }

        .panel {
            background: #172b1d;
            border: 1px solid #35543b;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 20px;
        }

        select,
        textarea,
        button {
            width: 100%;
            box-sizing: border-box;
            margin-top: 8px;
            margin-bottom: 14px;
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #48654d;
            font-size: 16px;
        }

        textarea {
            min-height: 90px;
            resize: vertical;
        }

        button {
            background: #315b39;
            color: white;
            cursor: pointer;
            font-weight: bold;
        }

        button:hover {
            background: #42734b;
        }

        .message {
            background: #1c3322;
            border-radius: 10px;
            padding: 14px;
            margin-top: 10px;
        }

        .route {
            color: #a9d5a8;
            font-size: 14px;
            margin-top: 6px;
        }

        .queued {
            color: #e6c76a;
        }

        .delivered {
            color: #78d681;
        }
    </style>
</head>

<body>

<h1>🌲 GNOMEMESH 📡</h1>

<div class="subtitle">
    Off-Grid Community Messaging
</div>

<div class="panel">

    <h2>📨 Send Message</h2>

    <form method="POST" action="/send">

        <label>From</label>

        <select name="source">
            {% for node in node_names %}
            <option value="{{ node }}">{{ node }}</option>
            {% endfor %}
        </select>

        <label>To</label>

        <select name="destination">
            {% for node in node_names %}
            <option value="{{ node }}">{{ node }}</option>
            {% endfor %}
        </select>

        <label>Message</label>

        <textarea
            name="message"
            placeholder="Type your message..."
            required></textarea>

        <button type="submit">
            📡 SEND THROUGH GNOMEMESH
        </button>

    </form>

</div>


<div class="panel">

    <h2>💬 Message History</h2>

    {% if messages %}

        {% for message in messages %}

        <div class="message">

            <strong>
                {{ message.source }}
                →
                {{ message.destination }}
            </strong>

            <div>
                {{ message.text }}
            </div>

            {% if message.delivered %}

                <div class="route delivered">
                    🟢 Delivered<br>
                    Route:
                    {{ message.route | join(" → ") }}
                </div>

            {% else %}

                <div class="route queued">
                    🟡 Queued — no route available
                </div>

            {% endif %}

        </div>

        {% endfor %}

    {% else %}

        <p>No messages yet.</p>

    {% endif %}

</div>


<div class="panel">

    <h2>📊 Network</h2>

    {% for node in nodes %}

        <div>
            {{ "🟢" if node.status == "ONLINE" else "🔴" }}
            <strong>{{ node.node }}</strong>
            — {{ node.status }}
        </div>

    {% endfor %}

</div>

</body>
</html>
"""


@app.route("/", methods=["GET"])
def dashboard():

    node_status = [
        node.status()
        for node in network.nodes.values()
    ]

    return render_template_string(
        HTML,
        nodes=node_status,
        node_names=list(network.nodes.keys()),
        messages=messages,
    )


@app.route("/send", methods=["POST"])
def send_message():

    source = request.form["source"]
    destination = request.form["destination"]
    message = request.form["message"]

    route = network.find_route(
        source,
        destination
    )

    delivered = network.send_message(
        source,
        destination,
        message
    )

    messages.append({
        "source": source,
        "destination": destination,
        "text": message,
        "delivered": delivered,
        "route": route or [],
    })

    return """
    <script>
        window.location.href = "/";
    </script>
    """


@app.route("/api/status")
def api_status():

    return jsonify({
        "nodes": [
            node.status()
            for node in network.nodes.values()
        ]
    })


if __name__ == "__main__":

    print()
    print("================================")
    print("      GNOMEMESH ONLINE")
    print("================================")
    print()
    print("Dashboard:")
    print("http://127.0.0.1:5000")
    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
