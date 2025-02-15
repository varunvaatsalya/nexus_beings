import React, { useState } from "react";

function ReportMissingPerson() {
  const [name, setName] = useState("");
  const [image, setImage] = useState(null);

  const handleSubmit = async () => {
    if (!image) {
      console.error("No image selected");
      return;
    }

    const formData = new FormData();
    formData.append("photo", image);
    formData.append("name", name);
    formData.append("isAdmin", true);

    try {
      // let url = 'http://192.168.45.24:5000/';
      let url = 'https://server-sih-1.onrender.com';
      const response = await fetch(`${url}/report`, {
        method: "POST",
        body: formData, // No need for 'Content-Type'
      });

      const text = await response.text(); // Get raw response
      try {
        const result = JSON.parse(text); // Parse JSON if valid
        if (response.ok) {
          console.log("Server Response:", result);
        } else {
          console.error("Error Response:", result);
        }
      } catch (e) {
        console.error("Non-JSON Response:", text);
      }
    } catch (error) {
      console.error("Upload Error:", error);
    }
  };

  return (
    <div>
      <div className="py-3 text-center text-4xl font-bold text-gray-800">
        Report Missing Person
      </div>
      <div className="flex flex-col mx-auto space-y-2 justify-center items-center">
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-1/2 p-3 rounded-xl outline-2 outline-offset-2 outline-gray-500 border-2 border-gray-500"
        />
        <div className="flex p-2 w-full justify-around">
          {image && (
            <img
              src={URL.createObjectURL(image)}
              alt="Preview"
              className="w-20 h-20 object-cover object-center rounded-lg"
            />
          )}
          <input
            type="file"
            onChange={(e) => setImage(e.target.files[0])}
          />
        </div>
        <button
          onClick={handleSubmit}
          className="p-3 bg-blue-500 text-white rounded-lg"
        >
          Submit
        </button>
      </div>
    </div>
  );
}

export default ReportMissingPerson;
