import React, { useState } from "react";
import Table from "./Table";
import axios from "axios";
import Loading from "./Loading";

const Search = () => {
  const [value, setValue] = useState("");
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const formSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    if (value.length === 0) return;
    var x = value;
    setValue("");
    await axios
      .get(`http://127.0.0.1:5000/${x}`, {
        headers: { "Access-Control-Allow-Origin": "*" },
      })
      .then((response) => {
        const x = JSON.parse(JSON.stringify(response.data));
        console.log(x);
        // console.log(value?.value?.word_split.length);
        setData((data) => [{ value: x }, ...data]);
        //console.log(data);
      });
    setLoading(false);
    //console.log(x);
  };

  return (
    <div className="flex justify-center align-middle items-center flex-col p-2 md:ml-0">
      <div className="h-[20vh] w-[100vw] flex justify-center align-center items-center">
        <form className="bg-[#2d3748] rounded-lg flex w-10/12 md:6/12 lg:w-3/12 h-[40px]">
          <i className="flex align-center justify-center p-2 ">
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M21 21L16.514 16.506M19 10.5C19 12.7543 18.1045 14.9163 16.5104 16.5104C14.9163 18.1045 12.7543 19 10.5 19C8.24566 19 6.08365 18.1045 4.48959 16.5104C2.89553 14.9163 2 12.7543 2 10.5C2 8.24566 2.89553 6.08365 4.48959 4.48959C6.08365 2.89553 8.24566 2 10.5 2C12.7543 2 14.9163 2.89553 16.5104 4.48959C18.1045 6.08365 19 8.24566 19 10.5V10.5Z"
                stroke="white"
                stroke-width="1"
                stroke-linecap="round"
              />
            </svg>
          </i>
          <input
            type="text"
            placeholder="Type the word..."
            className="placeholder:italic placeholder:text-slate-400 block bg-white w-full  rounded-md shadow-sm focus:outline-none focus:border-none bg-[#2d3748] focus:text-white text-[#ffffff] p-1"
            value={value}
            onChange={(e) => setValue(e.target.value)}
          ></input>
          <button type="submit" onClick={(e) => formSubmit(e)}></button>
        </form>
      </div>
      {!loading ? <></> : <Loading />}
      <Table data={data} className="overflow-scroll h-[80vh]" />
    </div>
  );
};

export default Search;
