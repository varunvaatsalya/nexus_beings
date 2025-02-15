import React, { useEffect } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import PoliceRegister from "./pages/PoliceRegister";
import Camera from "./pages/Camera";
import Home from "./pages/Home";
import MissingPersonList from "./pages/MissingPersonList";
import ReportMissingPerson from "./pages/ReportMissingPerson";
import Sidebar from "./components/Sidebar";
import Crime from "./pages/Crime";
import { getFCMToken, requestNotificationPermission } from "./firebase";
import { Toaster} from "react-hot-toast";

function App() {
  useEffect(() => {
    const setupNotifications = async () => {
      console.log('noti called');
        const permissionGranted = await requestNotificationPermission();
        if (permissionGranted) {
            // Fetch FCM token
            const token = await getFCMToken();
            if (token) {
                console.log("your FCM Token: ", token);
            }
        }
        else{
          console.log('denied')
        }
    };
    setupNotifications();
}, []);

  return (
    <BrowserRouter>
    <Toaster/>
      <div className="flex">
        <div>
          <Sidebar />
        </div>
        <div className="w-full">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/policeReg" element={<PoliceRegister />} />
            <Route path="/camera" element={<Camera />} />
            <Route path="/missingPersonList" element={<MissingPersonList />} />
            <Route path="/crime" element={<Crime />} />
            <Route
              path="/reportMissingPerson"
              Component={ReportMissingPerson}
            />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;

// home,
// stream
// reports krne
// repoet dekhne status
// heat map
// crime detection
// police records
