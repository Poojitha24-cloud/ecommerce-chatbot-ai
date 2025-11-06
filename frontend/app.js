const AI_API = "https://e-commerce-chatbot.onrender.com/chat";
const AUTH_API = "https://myshopbot.in";
let token = null;
let user = null;
function appendMessage(sender, text){
  const m = document.createElement('div');
  m.className = 'msg';
  m.innerHTML = `<strong>${sender}:</strong> ${text}`;
  document.getElementById('messages').appendChild(m);
  document.getElementById('messages').scrollTop = 1e9;
}
async function sendQuery(){
  const q = document.getElementById('inputQuery').value;
  if(!q) return;
  appendMessage('You', q);
  document.getElementById('inputQuery').value = '';
  const payload = { message: q, user_id: user ? user.id : null };
  try {
    const res = await fetch(AI_API, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) });
    const data = await res.json();
    appendMessage('Bot', data.reply);
    renderProducts(data.products || []);
  } catch (e) {
    appendMessage('Bot', 'Service currently unavailable.');
  }
}
function renderProducts(products){
  const container = document.getElementById('productCards');
  container.innerHTML = '';
  products.forEach(p => {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.innerHTML = `
      <img src="${p.image_url}" alt="${p.title}" />
      <div>
        <div><strong>${p.title || p.name}</strong></div>
        <div>₹${p.price} &nbsp;⭐ ${p.rating || ''}</div>
        <div><button onclick='addToWishlist("${p.id}")'>Wishlist</button>
        <button onclick='addToCart("${p.id}")'>Add to cart</button></div>
      </div>`;
    container.appendChild(card);
  });
}
async function addToWishlist(productId){
  if(!user){ alert('Login to use wishlist'); return; }
  try {
    const res = await fetch(AUTH_API + '/wishlist.php', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({user_id:user.id, product_id:productId}) });
    const d = await res.json();
    if(d.ok) alert('Added to wishlist');
  } catch(e){ alert('Failed'); }
}
async function addToCart(productId){ alert('Cart placeholder — implement server-side cart API'); }
document.getElementById('sendBtn').addEventListener('click', sendQuery);
document.getElementById('btnSignup').addEventListener('click', async ()=>{
  const name = prompt('Name'); const email = prompt('Email'); const pass = prompt('Password');
  const res = await fetch(AUTH_API + '/signup.php', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({name, email, password: pass}) });
  const d = await res.json(); if(d.ok) alert('Signed up'); else alert(JSON.stringify(d));
});
document.getElementById('btnLogin').addEventListener('click', async ()=>{
  const email = prompt('Email'); const pass = prompt('Password');
  const res = await fetch(AUTH_API + '/login.php', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({email, password: pass}) });
  const d = await res.json(); if(d.ok){ user = d.user; document.getElementById('profileBox').innerText = user.name; alert('Logged in'); } else alert(JSON.stringify(d));
});
