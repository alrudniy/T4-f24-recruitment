<template>
    <div id="fplogo"><img src="https://familypromise.org/wp-content/uploads/2021/03/FP-logo-horiz.png" alt="FP Logo" 
    style="width:200px;height:75px;"></div>
    <div class="login-page">
            <h2> Welcome! Select an option to get started :</h2>
            <div id="buttons">
                <button @click="goToAdmin">Admin Login</button>
                <button @click="goToHomeowner">Homeowner Login</button>
            </div>
    </div>
</template>
  
<script>
export default {
    name: 'rec_login',
    methods: {
      goToAdmin() {
        this.$router.push('/admin');
    },
      goToHomeowner() {
        this.$router.push('/homeowner');
    },
  },
};
  </script>
  
  <style scoped>

  #fplogo {
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1; /* ensure it's on top of other elements */
  }
  .login-page {
    text-align: center;
    margin-top: 50px;
    }
  #buttons {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
        button {   
            margin: 10px;
            padding: 10px 20px;
            font-size: 16px;
        } 
    }
  </style>
  