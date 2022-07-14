import React from "react";

const Header = () => {
  return (
    // flex justify-around
    <div className="h-[10vh] w-auto  border-b-[0.5px] border-opacity-10 border-[#f7fafc]">
      {/* {"// border-[#f7fafc]"} */}
      <div className="text-[#e6e8e6] h-full w-full md:w-2/3 lg:w-1/2 flex justify-start pl-10 items-center text-lg md:text-3xl font-bold">
        Venmurasu Programming Team
      </div>
      {/* <div className="h-full text-[#e6e8e6] w-1/2 flex justify-end pr-10 items-center text-2xl font-semibold">
        Credits
      </div> */}
    </div>
  );
};

export default Header;
