const express = require('express');
const twilio = require('twilio');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;
const accountSid = 'AC42c1f752b7714a9d581bdab2378ee9e7';
const authToken = '393f9f3011cd18ad1ba4965f17e7ed50';
const client = twilio(accountSid, authToken);

app.use(bodyParser.urlencoded({ extended: false }));

app.post('/send-code', (req, res) => {
  const { phone } = req.body;
  client.messages.create({
    body: 'Your verification code is: 123456',
    to: phone,
    from: '+19733495428' // Your Twilio phone number
  })
  .then(message => {
    res.status(200).send('Code sent');
  })
  .catch(error => {
    res.status(500).send('Error sending code');
  });
});

app.post('/verify-code', (req, res) => {
  const { phone, code } = req.body;
  // Add your verification logic here
  if (code === '123456') {
    res.status(200).send({ status: 'approved' });
  } else {
    res.status(200).send({ status: 'denied' });
  }
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
