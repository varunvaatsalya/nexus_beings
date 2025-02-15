import React, { useState } from "react";
import { Link } from "react-router-dom";
import MP_POLICE_LOGO from "../assets/MP_POLICE_LOGO.png";
import MP_GOV_LOGO from "../assets/MP_GOV_LOGO.png";
import { TbLogout2, TbReportSearch, TbShoppingBagExclamation } from "react-icons/tb";
import { TiHomeOutline } from "react-icons/ti";
import { HiOutlineStatusOnline } from "react-icons/hi";
import { CgDanger } from "react-icons/cg";
import { LuCctv } from "react-icons/lu";
import { MdOutlineLocalPolice, MdOutlineSettings } from "react-icons/md";
function Sidebar() {
  const [active, setActive] = useState(0);
  let links = [
    {
      name: "Home",
      url: "/",
      icon: <TiHomeOutline className="text-xl" />,
    },
    {
      name: "Streams",
      url: "/camera",
      icon: <LuCctv className="text-xl" />,
    },
    {
      name: "Reports",
      url: "/reportMissingPerson",
      icon: <TbReportSearch className="text-xl" />,
    },
    // {
    //   name: "Report Status",
    //   url: "/missingPersonList",
    //   icon: <HiOutlineStatusOnline className="text-xl" />,
    // },
    // {
    //   name: "Object Detection",
    //   url: "/objectDetection",
    //   icon: <CgDanger className="text-xl" />,
    // },
    {
      name: "Crime Detection",
      url: "/crime",
      icon: <TbShoppingBagExclamation className="text-xl" />,
    },
    {
      name: "Records",
      url: "/policeReg",
      icon: <MdOutlineLocalPolice className="text-xl" />,
    },
  ];
  return (
    <div className="h-screen w-80 bg-gray-100 flex flex-col">
      <div className="flex justify-between items-center border-b-2 border-gray-300 p-2">
        <div className=" mx-2">
          <div className="text-2xl font-bold">Dashboard</div>
          <div className="text-sm font-light">IIIT LUCKNOW</div>
        </div>
        {/* <div className="flex">
          <img src={MP_GOV_LOGO} alt="logo" className="w-16" />
          <img src={MP_POLICE_LOGO} alt="logo" className="w-16" />
        </div> */}
      </div>
      <div className="w-full p-2 flex-1 text-lg font-semibold">
        {links.map((link, index) => (
          <Link
            to={link.url}
            key={index}
            onClick={()=>{setActive(index)}}
            className={"flex hover:bg-gray-300 p-2 gap-2 items-center rounded-lg" + (active===index?' bg-gray-300':'')}
          >
            {link.icon}
            <div>{link.name}</div>
          </Link>
        ))}
      </div>
      <div className="w-full p-2 h-12 flex items-center text-xl border-t-2 border-gray-300 justify-between">
        <TbLogout2 className="hover:text-gray-800 cursor-pointer"/>
        <MdOutlineSettings className="hover:text-gray-800 cursor-pointer"/>
      </div>
    </div>
  );
}

export default Sidebar;
