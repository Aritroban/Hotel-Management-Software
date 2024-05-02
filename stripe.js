const stripe = Stripe('stripe_publishable_key');
const elements = stripe.elements();


const form = document.getElementById('payment-form');
form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const { token } = await stripe.createToken(card);

    const response = await fetch('/confirm-payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            paymentIntentId: clientSecret,
            token: token.id
        })
    });
