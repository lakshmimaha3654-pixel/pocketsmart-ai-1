# ============================================================
# POCKETSMART AI - COMPLETE SINGLE FILE
# ============================================================

import os
from flask import Flask, jsonify, render_template_string, request
from dotenv import load_dotenv

try:
    import google.generativeai as genai
except ImportError:
    genai = None


# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY", "")

if API_KEY and genai:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None


# ------------------------------------------------------------
# PRODUCT DATA
# ------------------------------------------------------------

PRODUCTS = [
    {
        "name": "Modern Sofa",
        "category": "Home Decor",
        "price": 18000,
        "platform": "Amazon",
        "description": "Modern comfortable sofa for home decoration",
    },
    {
        "name": "LED Smart Light",
        "category": "Home Decor",
        "price": 2500,
        "platform": "Flipkart",
        "description": "Smart LED light for modern home decoration",
    },
    {
        "name": "Artificial Flower Set",
        "category": "Home Decor",
        "price": 1200,
        "platform": "Meesho",
        "description": "Affordable artificial flowers for decoration",
    },
    {
        "name": "Gold Plated Necklace",
        "category": "Jewelry",
        "price": 4500,
        "platform": "Myntra",
        "description": "Elegant necklace suitable for functions",
    },
    {
        "name": "Traditional Jhumka",
        "category": "Jewelry",
        "price": 1800,
        "platform": "Myntra",
        "description": "Traditional jhumka earrings for special occasions",
    },
    {
        "name": "Pearl Bracelet",
        "category": "Jewelry",
        "price": 1500,
        "platform": "Amazon",
        "description": "Simple pearl bracelet",
    },
    {
        "name": "Birthday Decoration Set",
        "category": "Event Planning",
        "price": 1800,
        "platform": "Amazon",
        "description": "Complete birthday decoration kit",
    },
    {
        "name": "Engagement Decoration Set",
        "category": "Event Planning",
        "price": 5500,
        "platform": "Flipkart",
        "description": "Elegant decoration set for engagement functions",
    },
    {
        "name": "Mehndi Decoration Set",
        "category": "Event Planning",
        "price": 3500,
        "platform": "Meesho",
        "description": "Colorful decoration set for mehndi functions",
    },
    {
        "name": "Wireless Earbuds",
        "category": "Electronics",
        "price": 1999,
        "platform": "Amazon",
        "description": "Wireless earbuds with good sound quality",
    },
    {
        "name": "Smart Fitness Band",
        "category": "Electronics",
        "price": 2499,
        "platform": "Flipkart",
        "description": "Smart fitness tracking band",
    },
    {
        "name": "Bluetooth Speaker",
        "category": "Electronics",
        "price": 1799,
        "platform": "Amazon",
        "description": "Portable Bluetooth speaker",
    },
    {
        "name": "Cotton Kurti",
        "category": "Fashion",
        "price": 899,
        "platform": "Myntra",
        "description": "Comfortable cotton casual kurti",
    },
    {
        "name": "Anarkali Dress",
        "category": "Fashion",
        "price": 2499,
        "platform": "Myntra",
        "description": "Festive Anarkali dress",
    },
    {
        "name": "Traditional Cotton Saree",
        "category": "Fashion",
        "price": 2199,
        "platform": "Amazon",
        "description": "Traditional cotton saree",
    },
]


# ------------------------------------------------------------
# AI RECOMMENDATION LOGIC
# ------------------------------------------------------------


def generate_ai_recommendation(category, budget, preference):
    products = [
        p
        for p in PRODUCTS
        if p["category"].lower() == category.lower() and p["price"] <= budget
    ]

    if not products:
        return "No products found within your budget."

    product_text = ""
    for product in products:
        product_text += (
            f"\nProduct: {product['name']}"
            f"\nPrice: ₹{product['price']}"
            f"\nPlatform: {product['platform']}"
            f"\nDescription: {product['description']}\n"
        )

    prompt = f"""
You are PocketSmart AI.
You are a smart budget-based recommendation assistant.

User Category:
{category}

User Budget:
₹{budget}

User Preference:
{preference}

Available Products:
{product_text}

Recommend the most suitable products.

For each product provide:
1. Product Name
2. Price
3. Platform
4. Why it fits the user's preference
5. Budget status

Do not invent products.
Do not change prices.
Do not recommend products outside the given budget.
Give a simple and clear answer.
"""

    if model:
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as error:
            print("Gemini Error:", error)

    # Fallback
    result = "PocketSmart AI Recommendations\n\n"
    total = 0
    for product in products[:5]:
        result += (
            f"🛍️ {product['name']}\n"
            f"💰 Price: ₹{product['price']}\n"
            f"🛒 Platform: {product['platform']}\n"
            f"✨ {product['description']}\n\n"
        )
        total += product["price"]

    result += f"Estimated Total: ₹{total}\n"
    result += f"Remaining Budget: ₹{max(budget - total, 0)}"
    return result


# ------------------------------------------------------------
# HTML TEMPLATE
# ------------------------------------------------------------

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PocketSmart AI</title>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            min-height: 100vh;
        }
        .container {
            width: 90%;
            max-width: 900px;
            margin: auto;
            padding: 30px 10px;
        }
        .header { text-align: center; color: white; padding: 20px; }
        .header h1 { font-size: 42px; margin-bottom: 10px; }
        .card {
            background: white;
            padding: 25px;
            margin-top: 20px;
            border-radius: 18px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        label { display: block; margin-top: 15px; font-weight: bold; }
        input, select, textarea {
            width: 100%;
            padding: 13px;
            margin-top: 8px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
        }
        textarea { height: 100px; resize: none; }
        button {
            width: 100%;
            padding: 15px;
            margin-top: 20px;
            border: none;
            border-radius: 10px;
            background: #667eea;
            color: white;
            font-size: 18px;
            cursor: pointer;
        }
        button:hover { background: #4f5ed1; }
        .result {
            background: white;
            margin-top: 25px;
            padding: 25px;
            border-radius: 18px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .result h2 { color: #667eea; }
        #output { white-space: pre-wrap; line-height: 1.7; font-size: 16px; }
        .footer { text-align: center; color: white; margin-top: 25px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>💰 PocketSmart AI</h1>
            <p>GenAI-Powered Budget Recommendation System</p>
        </div>

        <div class="card">
            <label>Choose Category</label>
            <select id="category">
                <option value="Home Decor">Home Decor</option>
                <option value="Event Planning">Event Planning</option>
                <option value="Jewelry">Jewelry</option>
                <option value="Electronics">Electronics</option>
                <option value="Fashion">Fashion</option>
            </select>

            <label>Enter Your Budget</label>
            <input type="number" id="budget" placeholder="Enter budget in ₹">

            <label>Your Preference</label>
            <textarea id="preference" placeholder="Example: Modern, affordable, traditional, stylish..."></textarea>

            <button onclick="getRecommendation()">🤖 Get AI Recommendation</button>
        </div>

        <div class="result">
            <h2>✨ Recommendation</h2>
            <div id="output">Your AI recommendation will appear here...</div>
        </div>

        <div class="footer">
            PocketSmart AI © 2026
        </div>
    </div>

    <script>
        async function getRecommendation() {
            const category = document.getElementById("category").value;
            const budget = parseFloat(document.getElementById("budget").value);
            const preference = document.getElementById("preference").value;
            const output = document.getElementById("output");

            if (!budget || budget <= 0) {
                output.innerHTML = "❌ Please enter a valid budget.";
                return;
            }

            output.innerHTML = "🤖 AI is generating your recommendation...";

            try {
                const response = await fetch("/recommend", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ category, budget, preference })
                });

                const data = await response.json();

                if (data.success) {
                    output.innerHTML = data.recommendation;
                } else {
                    output.innerHTML = "❌ " + data.error;
                }
            } catch (error) {
                output.innerHTML = "❌ Something went wrong. Please try again.";
            }
        }
    </script>
</body>
</html>
"""


# ------------------------------------------------------------
# FLASK ROUTES
# ------------------------------------------------------------


@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        data = request.get_json() or {}
        category = data.get("category", "Home Decor")
        budget = float(data.get("budget", 0))
        preference = data.get("preference", "")

        recommendation = generate_ai_recommendation(
            category, budget, preference
        )
        return jsonify({"success": True, "recommendation": recommendation})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


# ------------------------------------------------------------
# RUN SERVER
# ------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)