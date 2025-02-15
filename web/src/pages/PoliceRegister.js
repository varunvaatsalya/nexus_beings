import React from "react";
import { useForm } from "react-hook-form";

function PoliceRegister() {
  const { register, handleSubmit } = useForm();

  const onSubmit = async (data) => {
    try {
      // let url = 'http://192.168.45.24:5000/';
      let url = 'https://server-sih-1.onrender.com';
        let result = await fetch(`${url}/signupWeb`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json", // Set the header for JSON
          },
          body: JSON.stringify(data), // Properly stringify the data
        });

        // Parsing the response as JSON
        result = await result.json();
        // Check if login was successful
        console.log(result)
    } catch (error) {
      console.error("Error submitting application:", error);
    }
  };
  return (
    <div className="">
      <div className="py-3 text-center text-4xl font-bold text-gray-800">
        Police Regsitration
      </div>
      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex flex-col mx-auto space-y-2 justify-center items-center"
      >
        <input
          type="text"
          placeholder="Name"
          {...register("name", { required: "Name is required" })}
          className="w-1/2 p-3 rounded-xl outline-2 outline-offset-2 outline-gray-500 border-2 border-gray-500"
        />
        <input
          type="text"
          placeholder="Unique Id"
          {...register("uniqueId")}
          className="w-1/2 p-3 rounded-xl outline-2 outline-offset-2 outline-gray-500 border-2 border-gray-500"
        />
        <input
          type="number"
          placeholder="Contact"
          {...register("contact", { required: "Contact is required" })}
          className="w-1/2 p-3 rounded-xl outline-2 outline-offset-2 outline-gray-500 border-2 border-gray-500"
        />
        <input
          type="password"
          placeholder="Password"
          {...register("password", { required: "Password is required" })}
          className="w-1/2 p-3 rounded-xl outline-2 outline-offset-2 outline-gray-500 border-2 border-gray-500"
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default PoliceRegister;
