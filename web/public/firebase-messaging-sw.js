importScripts('https://www.gstatic.com/firebasejs/9.17.1/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.17.1/firebase-messaging-compat.js');

const firebaseConfig = {
    apiKey: "AIzaSyBRIKhGqmYlKOQ8woS2khCx9NgVJ8GnOtM",
  authDomain: "nexus-beings.firebaseapp.com",
  projectId: "nexus-beings",
  storageBucket: "nexus-beings.firebasestorage.app",
  messagingSenderId: "543824000886",
  appId: "1:543824000886:web:0e21101b3a8093f881ac57",
};

firebase.initializeApp(firebaseConfig);

const messaging = firebase.messaging();

// Background message handler
messaging.onBackgroundMessage((payload) => {
    console.log('[firebase-messaging-sw.js] Received background message: ', payload);

    const notificationTitle = payload.notification.title || 'Default Title';
    const notificationOptions = {
        body: payload.notification.body || 'Default body',
        icon: payload.notification.icon || '/firebase-logo.png', // Optional icon
    };

    self.registration.showNotification(notificationTitle, notificationOptions);
});

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistration('/firebase-messaging-sw.js')
        .then((registration) => {
            if (!registration) {
                navigator.serviceWorker.register('/firebase-messaging-sw.js')
                    .then((reg) => console.log('Service Worker registered:', reg))
                    .catch((err) => console.error('Service Worker registration failed:', err));
            }
        });
}
