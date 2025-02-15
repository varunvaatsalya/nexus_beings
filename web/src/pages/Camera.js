import React, { useEffect, useState } from "react";

function Camera() {
  const [ipAddresses, setIpAddresses] = useState([
    // {url:"http://192.168.137.203:4747/video"}
  ]);
  const [inputValue, setInputValue] = useState("");
  // const handleInputChange = (event) => {
  //   setInputValue(event.target.value);
  // };
  // // let url = 'http://192.168.45.24:5000/';
  // let url = 'https://server-sih-1.onrender.com';
  // const handleAddIp = async () => {
  //   if (inputValue.trim() !== "") {
  //     let result = await fetch(`${url}/camUrl`, {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json", // Set the header for JSON
  //       },
  //       body: JSON.stringify({ name: "varun", url: inputValue }), // Properly stringify the data
  //     });
  //     result = await result.json();
  //     if (result.success) {
  //       setIpAddresses([...ipAddresses, result.djangoResponse]);
  //     }
  //     setInputValue("");
  //   }
  // };
  // useEffect(() => {
  //   async function fetchIpData() {
  //     let result = await fetch(`${url}/camUrl`);
  //     result = await result.json();
  //     if (result.success) {
  //       setIpAddresses(result.ipIds);
  //       console.log(result.ipIds);
  //     }
  //   }
  //   fetchIpData();
  // }, [setIpAddresses]);
  return (
    <div className="app-container">
      {" "}
      <h1 className="text-lg font-semibold">IP Address Image Viewer</h1>
      {/* <div className="input-container">
        
        <input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Enter IP Address"
        />
        <button onClick={handleAddIp}>Add IP</button>
      </div> */}
      <div className="mx-auto w-80 aspect-video">
        
        {ipAddresses.length > 0 ? (
          ipAddresses.map((ip, index) => (
            <img
              key={index}
              src={ip.url}
              alt={`IP: ${ip.url}`}
              className="h-full mx-auto object-cover"
            />
          ))
        ) : (
          <div>no camera found</div>
        )}{" "}
      </div>{" "}
    </div>
  );
}

export default Camera;
