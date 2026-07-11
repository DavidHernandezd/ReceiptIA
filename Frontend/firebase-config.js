// firebase-config.js

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-firestore.js";

const firebaseConfig = {
    apiKey: "AIzaSyDiS8gnptrcT9qf9rSEFJl-FhwrpvVNy5w",
    authDomain: "receiptia-fcdd5.firebaseapp.com",
    projectId: "receiptia-fcdd5",
    storageBucket: "receiptia-fcdd5.firebasestorage.app",
    messagingSenderId: "166280154540",
    appId: "1:166280154540:web:2816cbcf72dbcb267f3e09",
    measurementId: "G-9QJ505G1VS"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

export { app, auth, db };