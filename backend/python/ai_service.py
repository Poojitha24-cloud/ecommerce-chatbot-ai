# ai_service.py
# Flask service with OpenAI GPT integration (if OPENAI_API_KEY provided)
# Fallback: TF-IDF product search for recommendations.
import os, json, re
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

with open('products.json', 'r', encoding='utf8') as f:
    products = json.load(f)

# lightweight TF-IDF vectorizer for product matching
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    corpus = [p['title'] + ' ' + p.get('description','') for p in products]
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(corpus)
except Exception:
    vectorizer = None
    X = None

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY') or os.environ.get('OPENAI_KEY')
USE_OPENAI = bool(OPENAI_API_KEY)
if USE_OPENAI:
    import openai
    openai.api_key = OPENAI_API_KEY

def tfidf_search(query, topn=5, max_price=None):
    if not vectorizer or X is None:
        # fallback simple substring search
        res = [p for p in products if query.lower() in (p['title']+p.get('description','')).lower()]
        return res[:topn]
    qv = vectorizer.transform([query])
    sims = cosine_similarity(qv, X).flatten()
    idx = sims.argsort()[::-1][:topn]
    res = []
    for i in idx:
        p = products[i]
        if max_price and p.get('price') and p['price']>max_price:
            continue
        res.append(p)
    return res

def extract_max_price(text):
    m = re.search(r'under\s*₹?\s*(\d[\d,]*)', text)
    if m:
        return float(m.group(1).replace(',', ''))
    return None

@app.route('/health')
def health():
    return jsonify({'ok':True, 'mode': 'openai' if USE_OPENAI else 'tfidf'})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    message = (data.get('message') or '').strip()
    user_id = data.get('user_id')
    # Extract price constraint
    max_price = extract_max_price(message.lower())

    # If OpenAI available, use GPT for interactive replies and product suggestions
    if USE_OPENAI:
        try:
            import openai
            response = openai.ChatCompletion.create(
                model='gpt-4o-mini',
                messages=[{'role':'system','content':'You are a helpful e-commerce assistant.'},{'role':'user','content': message}],
                max_tokens=250,
            )
            reply_text = response['choices'][0]['message']['content'].strip()
            # still provide structured product suggestions using TF-IDF
            recs = tfidf_search(message, topn=5, max_price=max_price)
            return jsonify({'reply': reply_text, 'products': recs})
        except Exception as e:
            # on error, fallback to TF-IDF behavior
            pass
    # Fallback: rule-based + tfidf
    intent = 'search'
    if any(k in message.lower() for k in ['track','where is my order','order status']):
        intent = 'track'
    if intent == 'track':
        return jsonify({'reply':'Please provide your order ID to check status.'})
    # default search
    recs = tfidf_search(message, topn=5, max_price=max_price)
    if recs:
        reply = f'I found {len(recs)} products that match your query.'
    else:
        reply = 'Sorry, I couldn\'t find matching products. Try different keywords.'
    return jsonify({'reply': reply, 'products': recs})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
