import React, { useEffect, useState } from "react";

function MissingPersonList() {
  const [lists, setLists] = useState([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const url = "https://server-sih-1.onrender.com/";
        // const url = 'http://192.168.45.24:5000/';
        let result = await fetch(`${url}listReport`);
        result = await result.json();
        if (result.success) {
          setLists(result.data);
        }
      } catch (err) {
        console.log("error: ", err);
      }
    }
    fetchData();
  }, []);
  return (
    <div className="max-h-[100vh] flex flex-col p-2">
      <div className="py-3 text-center text-4xl font-bold text-gray-800">
        Missing Person List
      </div>
      <div className="flex-1 flex flex-wrap mx-auto gap-2 w-full justify-center items-center overflow-y-auto">
        {lists.map((list, index) => (
          <div className="w-60 rounded-xl bg-red-400" key={index}>
            <div className="w-full h-80 flex justify-center items-center">
              <img
                src={list.url}
                alt="img"
                className="object-cover h-full w-full rounded-xl"
              />
            </div>
            <div className="p-2 text-center">{list.name}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MissingPersonList;
