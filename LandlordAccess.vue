<template>
  <div>
    <h1>Landlord Access</h1>
    <form action="">
      <label for="username">Username:</label>
      <input type="text" v-model="username" required aria-label="Username"><br>

      <label for="phone">Phone Number:</label>
      <input type="text" v-model="phone" required aria-label="Phone Number"><br>

      <button type="button" @click="sendCode">Send Verification Code</button><br>

      <label for="code">Verification Code:</label>
      <input type="text" v-model="code" aria-label="Verification Code"><br>

      <button type="button" @click="verifyCode">Verify Code</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      phone: '',
      code: ''
    };
  },
  methods: {
    async sendCode() {
      try {
        const response = await axios.post('http://localhost:3000/send-code', {
          phone: this.phone
        });
        console.log('Send Code Response:', response.data);
      } catch (error) {
        console.error('Error sending code:', error);
      }
    },
    async verifyCode() {
      try {
        const response = await axios.post('http://localhost:3000/verify-code', {
          phone: this.phone,
          code: this.code
        });
        console.log('Verify Code Response:', response.data);
        if (response.data.status === 'approved') {
          alert('Verification successful');
          // Allow access to the form
        } else {
          alert('Invalid verification code');
        }
      } catch (error) {
        console.error('Error verifying code:', error);
      }
    }
  }
};
</script>

<style>
body {
  font-family: Arial, sans-serif;
  margin: 20px;
  padding: 0;
  background-color: #f4f4f4;
}
h1 {
  text-align: center;
}
form {
  max-width: 300px;
  margin: 0 auto;
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}
label {
  margin: 10px 0;
  display: block;
}
input {
  width: calc(100% - 20px);
  padding: 8px;
  margin: 5px 0 10px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:hover {
  background-color: #45a049;
}
</style>
