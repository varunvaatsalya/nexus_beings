import React, { useEffect, useState } from "react";
import { BarChart, PieChart } from "@mui/x-charts";
import lane1 from "../assets/lane1.mp4";
import lane2 from "../assets/lane2.mp4";
import lane3 from "../assets/lane3.mp4";
import lane4 from "../assets/lane4.mp4";
import nikita from "../assets/nikita.mp4";
import nikita2 from "../assets/nikita2.mp4";

function Home() {
  const [unreslovedReports, setUnreslovedReports] = useState([]);
  const [view, setView] = useState(true);

  const [bags, setBags] = useState([]);
  const xLabels = ["Lane1", "Lane2", "Lane3", "Lane4"];
  const cumulativeSalesData = [45, 26, 17, 13];
  const cumulativeOrdersData = [65, 35, 0, 25];
  useEffect(() => {
    async function fetchUnresolvedReports() {
      let url = "http://192.168.137.8:5000/unResolvedReports";
      // let url = "https://server-sih-1.onrender.com/unResolvedReports";
      try {
        let result = await fetch(url);
        result = await result.json();
        if (result.success) {
          setUnreslovedReports(result.data);
        }
      } catch (err) {
        console.log("error: ", err);
      }
    }
    async function fetchBags() {
      let url = "http://192.168.137.8:5000/getBag";
      // let url = "https://server-sih-1.onrender.com/unResolvedReports";
      try {
        let result = await fetch(url);
        result = await result.json();
        if (result.success) {
          setBags(result.data);
        }
      } catch (err) {
        console.log("error: ", err);
      }
    }
    fetchUnresolvedReports();
    fetchBags();
  }, []);
  const stockData = [
    {
      value: view?2:0,
      label: "Men",
      color: "red",
    },
    {
      value: 1,
      label: "Women",
      color: "#4caf50",
    },
  ];
  async function sendConfirmPerson(reportId, isNotify) {
    console.log("caledddd");
    // let url = 'https://server-sih-1.onrender.com/notifyNearByOfficers';
    // if(isNotify) url = 'https://server-sih-1.onrender.com/resolveReport';
    let url = "http://192.168.137.8:5000/notifyNearByOfficers";
    if (isNotify) url = "http://192.168.137.8:5000/resolveReport";
    try {
      let result = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // Set the header for JSON
        },
        body: JSON.stringify({ reportId }), // Properly stringify the data
      });

      // Parsing the response as JSON
      result = await result.json();
      console.log(result);
      // Check if login was successful
      if (result.success) {
        if (!isNotify) {
          const updatedReports = unreslovedReports.map((report) => {
            if (report._id === reportId) {
              return { ...report, isNotify: true };
            }
            return report;
          });
          setUnreslovedReports(updatedReports);
        } else {
          setUnreslovedReports((prevReports) =>
            prevReports.filter((report) => report._id !== reportId)
          );
        }
      }
    } catch (error) {
      console.error("Error submitting application:", error);
    }
  }
  useEffect(() => {}, [unreslovedReports]);
  let videos = [
    { name: "Lane1", url: lane1 },
    { name: "Lane2", url: lane2 },
    { name: "Lane3", url: lane3 },
    { name: "Lane4", url: lane4 },
  ];
  return (
    <>
      <div className="flex w-full min-h-screen">
        <div className="flex flex-col w-3/5 min-h-screen h-screen border-r-2 border-gray-300">
          <div className="px-3 py-2 text-2xl font-semibold text-gray-800">
            Smart Traffic Management
          </div>
          <div className="flex-1 w-full border-y-2 border-gray-300 overflow-y-auto">
            <div className="flex justify-around flex-wrap items-center p-2">
              {videos.map((vid) => (
                <div className="w-[47%] h-48">
                  <div className=" bg-black">
                    <video
                      className="h-40 w-full flex justify-center items-center"
                      src={vid.url}
                      muted
                      loop
                      autoPlay
                      playsInline
                    ></video>
                  </div>
                  <div className="text-center p-2">{vid.name}</div>
                </div>
              ))}
            </div>
            {/* {unreslovedReports.map((unResolvedReport, index) => (
              <div className="flex justify-around items-center p-2">
                <div className="text-xl mx-3">{index + 1 + "."}</div>
                <div className="flex justify-center items-center gap-4">
                  <div className="w-1/3 aspect-square flex justify-center items-center mx-2">
                    <img
                      src={unResolvedReport.url}
                      alt="err"
                      className="rounded-xl object-cover h-full w-full "
                    />
                  </div>
                  <div className="w-1/3 aspect-square flex justify-center items-center mx-2">
                    <img
                      src={
                        unResolvedReport.history[
                          unResolvedReport.history.length - 1
                        ].url
                      }
                      alt="err"
                      className="rounded-xl object-cover h-full w-full"
                    />
                  </div>
                </div>
                <button
                  onClick={() => {
                    sendConfirmPerson(
                      unResolvedReport._id,
                      unResolvedReport.isNotify
                    );
                  }}
                  className="py-2 px-3 text-lg font-semibold bg-blue-500 text-gray-50 rounded-xl"
                >
                  {unResolvedReport.isNotify ? "Resolve" : "Notify"}
                </button>
              </div>
            ))} */}
          </div>
          <div className="max-h-60">
            <BarChart
              className="scale-75"
              width={800}
              height={250}
              borderRadius={15}
              series={[
                {
                  data: cumulativeSalesData,
                  label: "No of Vehicle",
                  yAxisId: "leftAxisId",
                  type: "bar", // Ye important hai
                },
                {
                  data: cumulativeOrdersData,
                  label: "Time (Sec)",
                  yAxisId: "rightAxisId",
                  type: "bar", // Ye bhi bar chart ke liye set karna hoga
                },
              ]}
              xAxis={[
                {
                  scaleType: "band", // BarChart ke liye scaleType "band" use hota hai
                  data: xLabels,
                },
              ]}
              yAxis={[{ id: "leftAxisId" }, { id: "rightAxisId" }]}
            />
          </div>
        </div>
        <div className="flex flex-col w-2/5 min-h-screen h-screen">
          {/* <div className="w-full h-3/5 max-h-3/5 flex flex-col pb-1">
            <div className="font-semibold px-3 py-1 border-b-2 border-gray-200">
              Crime Insights
            </div>
            <div className="flex-1 overflow-y-auto pt-4 flex flex-col items-center gap-2 p-2">
              <div className="flex justify-around items-center gap-3">
                <div className="h-36 aspect-video bg-gray-950 rounded-xl flex justify-center items-center">
                  <video
                    src="https://res.cloudinary.com/ddv1qs3by/video/upload/f_auto,q_auto/v1733600332/crime_clips/hduzr3pd2r6lc0rjcj88.mp4"
                    className="h-full w-full object-contain rounded-xl"
                    controls
                    loop
                    autoPlay
                    muted
                  ></video>
                </div>
                <div className="">
                  <div>Camera: CAM01</div>
                  <div>Zone: 03</div>
                </div>
              </div>
              <div className="flex justify-around items-center gap-3">
                <div className="h-36 aspect-video bg-gray-950 rounded-xl flex justify-center items-center">
                  <video
                    src="https://res.cloudinary.com/ddv1qs3by/video/upload/f_auto,q_auto/v1733600332/crime_clips/hduzr3pd2r6lc0rjcj88.mp4"
                    className="h-full w-full object-contain rounded-xl"
                    controls
                    loop
                    autoPlay
                    muted
                  ></video>
                </div>
                <div className="">
                  <div>Camera: CAM01</div>
                  <div>Zone: 03</div>
                </div>
              </div>
              <div className="flex justify-around items-center gap-3">
                <div className="h-36 aspect-video bg-gray-950 rounded-xl flex justify-center items-center">
                  <video
                    src="https://res.cloudinary.com/ddv1qs3by/video/upload/f_auto,q_auto/v1733600332/crime_clips/hduzr3pd2r6lc0rjcj88.mp4"
                    className="h-full w-full object-contain rounded-xl"
                    controls
                    loop
                    autoPlay
                    muted
                  ></video>
                </div>
                <div className="">
                  <div>Camera: CAM01</div>
                  <div>Zone: 03</div>
                </div>
              </div>
            </div>
          </div> */}
          <div className="w-full flex-1 flex flex-col overflow-y-auto">
            <div className="font-semibold p-3 border-b-2 border-gray-200">
              Women Safety - 1090
            </div>
            <div className="w-full flex-1 overflow-y-auto border-b-2 border-gray-200 flex flex-col items-center gap-2 p-2">
              <div className="flex flex-col justify-around items-center gap-3 px-2 bg w-full">
                <div className="w-full bg-black aspect-video flex justify-center items-center mx-2">
                  <video
                    className="object-contain w-full flex justify-center items-center"
                    src={view ? nikita : nikita2}
                    muted
                    loop
                    autoPlay
                    playsInline
                  ></video>
                </div>
                <div className="">
                  <div className="font-semibold">Camera: CAM01</div>
                  <div className="font-semibold">Location: ABC Colony</div>
                </div>
              </div>
              <div className="flex justify-center-items-center gap-3">
                <button
                  className="px-3 py-1 font-semibold bg-gray-600 rounded-lg text-white"
                  onClick={() => {
                    setView(true);
                  }}
                >
                  View 1
                </button>
                <button
                  className="px-3 py-1 font-semibold bg-gray-600 rounded-lg text-white"
                  onClick={() => {
                    setView(false);
                  }}
                >
                  View 2
                </button>
              </div>
              {bags.map((bag, index) => (
                <div
                  key={index}
                  className="flex justify-around items-center gap-3"
                >
                  <div className="w-40 aspect-video flex justify-center items-center mx-2">
                    <img src={bag.url} alt="err" className="rounded-lg" />
                  </div>
                  <div className="">
                    <div>Camera: CAM01</div>
                  </div>
                </div>
              ))}
            </div>
            <div className="flex mt-2 justifycenter items-center scale-80">
              <PieChart
                series={[
                  {
                    data: stockData,
                    innerRadius: 15,
                    outerRadius: 80,
                    paddingAngle: 5,
                    cornerRadius: 5,
                    startAngle: -45,
                    endAngle: 315,
                    cx: 40,
                    cy: 80,
                  },
                ]}
                width={240}
                height={180}
              />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default Home;
