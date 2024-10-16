import Image from "next/image";
import React from "react";
import BravesLogo from "../braves-logo.png";

export default function BravesHeader() {
  return (
    <header className="flex flex-col md:flex-row items-center justify-center md:justify-between bg-white text-black p-2 md:p-4 border-b-2 border-black">
      <div className="flex items-center">
        <Image
          src={BravesLogo}
          alt="Braves Logo"
          width={100}
          height={100}
          className="w-12 h-12 md:w-20 md:h-20"
        />
      </div>
      <h1 className="text-lg md:text-2xl mt-2 md:mt-0 text-center md:text-left">
        Atlanta Braves Analysis Web App
      </h1>
    </header>
  );
}
