// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyAzXbfJEARYdML_JmEzCRG0ejWeT7BSPUU",
    authDomain: "easy-check-64688.firebaseapp.com",
    projectId: "easy-check-64688",
    storageBucket: "easy-check-64688.firebasestorage.app",
    messagingSenderId: "498558913683",
    appId: "1:498558913683:web:a9c970106f159c78f25166",
    measurementId: "G-XHKEGY5E53"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);