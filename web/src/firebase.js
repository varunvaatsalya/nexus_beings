// firebase.js
import { initializeApp } from "firebase/app";
import {
  getMessaging,
  getToken,
  onMessage,
  requestPermission,
} from "firebase/messaging";
import toast from "react-hot-toast";
import { TiWarningOutline } from "react-icons/ti";

const firebaseConfig = {
  apiKey: "AIzaSyBRIKhGqmYlKOQ8woS2khCx9NgVJ8GnOtM",
  authDomain: "nexus-beings.firebaseapp.com",
  projectId: "nexus-beings",
  storageBucket: "nexus-beings.firebasestorage.app",
  messagingSenderId: "543824000886",
  appId: "1:543824000886:web:0e21101b3a8093f881ac57",
  measurementId: "G-YFSQHG8V9N",
};
let YOUR_VAPID_KEY =
  "BIw-cPoIZlDPG7ouau-2tw_56uS4SYYPhOIYSSV-Whi9LjCRQyCmp1rKcwE_nbu_RWDE5qbx5tAe1vHGos3rYIc";
const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

// Get FCM token
export const getFCMToken = async () => {
  try {
    const registration = await navigator.serviceWorker.register(
      "/firebase-messaging-sw.js"
    );
    console.log("Service Worker Registered: ", registration);

    const currentToken = await getToken(messaging, {
      vapidKey: YOUR_VAPID_KEY,
      serviceWorkerRegistration: registration,
    });
    if (currentToken) {
      console.log("FCM Token: ", currentToken);
      return currentToken;
    } else {
      console.log(
        "No registration token available. Request permission to generate one."
      );
    }
  } catch (err) {
    console.error("An error occurred while retrieving token. ", err);
  }
};

export const requestNotificationPermission = async () => {
  try {
    const permission = await Notification.requestPermission();
    if (permission === "granted") {
      console.log("Notification permission granted.");
      return true;
    } else {
      console.log("Notification permission denied.");
      return false;
    }
  } catch (err) {
    console.error("Error requesting notification permission: ", err);
    return false;
  }
};
const CustomToast = ({ title, body }) => (
  <div>
    <div className="text-xl font-semibold">{title}</div> 
    <div className="">{body}</div>
  </div>
);

const handleToggleTheme = (title, body ) => {
  toast(
    <CustomToast title={title} body={body} />,
    {
      icon: <TiWarningOutline className="text-white text-2xl"/>,
      style: {
        borderRadius: "10px",
        background: '#ef4444',
        color: "#fff",
      },
    }
  );
  //   toast(`Theme changed to ${theme === "light" ? "Dark" : "Light"} mode!`, {
  //     icon: `${theme === "light" ? "🌙" : "☀️"}`,
  //     style: {
  //       borderRadius: "10px",
  //       background: `${theme === "light" ? "#333" : "#fff"} `,
  //       color: `${theme === "light" ? "#fff" : "#333"}`,
  //     },
  //   });
};

// Listener for messages
// onMessage(messaging, (payload) => {
//   console.log("Message received: ", payload);
//   handleToggleTheme(payload.notification.title, payload.notification.body);
//   setTimeout(() => { window.location.reload(); }, 2000);
// });

// fxx2dmF0bPIUrYbCCo1vRm:APA91bFIIexCOShjB-k7KfexCB7ylS0kmLS5qd2vPbHFajw00CKTsVA7lGt22e6caGLYSybqd6xSeL_AYRvUJEBr38SAbS70WtLBQRuvnh-5o_3O_T9ENSg
//---varun edge---
