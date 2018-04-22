var config = {
  apiKey: "AIzaSyD2rfrga7gEv9s9nK3HBH13rH3BvJzbDHU",
  authDomain: "popcornu-user.firebaseapp.com",
  databaseURL: "https://popcornu-user.firebaseio.com",
  projectId: "popcornu-user",
  storageBucket: "popcornu-user.appspot.com",
  messagingSenderId: "249396109468"
};
firebase.initializeApp(config);


  initApp = function() {
    firebase.auth().onAuthStateChanged(function(user) {
      if (user) {
        // User is signed in.
        var email = user.email;
        var uid = user.uid;
        user.getIdToken().then(function(accessToken) {
        document.getElementById('user').textContent = email + ', you have signed in.';
        });
        console.log('signin');
      } else {
        // User is signed out.
        document.getElementById('user').textContent = 'No user signed in.';
        console.log('no signin');
      }
    }, function(error) {
      console.log(error);
    });
  };

  window.addEventListener('load', function() {
    initApp()
  });