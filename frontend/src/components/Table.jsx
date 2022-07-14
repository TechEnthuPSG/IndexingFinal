import React from "react";

const Table = ({ data }) => {
  //console.log("table sender");
  //console.log(data);
  return (
    <div className="text-[#ffffff] overflow-x-auto overflow-y-auto rounded-md p-2">
      <table className="border-[0.5px]  border-opacity-10 border-[#f7fafc] border-spacing-1 border-collapse min-w-full leading-normal rounded-md overflow-auto">
        <thead>
          <tr className="h-[10vh] text-[#2d3748]">
            <th className="border-[0.5px] border-opacity-10 border-[#000000]  text-center text-xs md:text-sm font-semibold text-white uppercase tracking-wider w-[90px] md:w-[200px] lg:w-[250px] bg-[#ebf4ff] bg-opacity-90">
              Word
            </th>
            <th className="border-[0.5px] border-opacity-10 border-[#000000]  text-center text-xs md:text-sm font-semibold text-white uppercase tracking-wider w-[90px] md:w-[200px] lg:w-[250px] bg-[#ebf4ff] bg-opacity-90">
              Stemmed Words
            </th>
            <th className="border-[0.5px] border-opacity-10 border-[#000000]  text-center text-xs md:text-sm font-semibold text-white uppercase tracking-wider w-[90px] md:w-[200px] lg:w-[250px] bg-[#ebf4ff] bg-opacity-90">
              optimum
            </th>
            <th className="border-[0.5px] border-opacity-10 border-[#000000]  text-center text-xs md:text-sm font-semibold text-white uppercase tracking-wider w-[90px] md:w-[200px] lg:w-[250px] bg-[#ebf4ff] bg-opacity-90">
              Result
            </th>
          </tr>
        </thead>
        <tbody className="break-words overflow-auto">
          {data?.map((value) => {
            //console.log(value);
            return (
              <tr className="break-words h-[10vh]">
                <td className="border-[0.5px] border-opacity-10 border-[#f7fafc] text-center text-xs md:text-sm font-semibold text-white tracking-wider w-[90px] max-w-[90px] md:w-[200px] md:max-w[200px] lg:w-[250px] lg:max-w-[250px] p-2">
                  {value?.value?.word}
                </td>
                <td className="border-[0.5px] border-opacity-10 border-[#f7fafc] text-center text-xs md:text-sm font-semibold text-white tracking-wider w-[90px] max-w-[90px] md:w-[200px] md:max-w[200px] lg:w-[250px] lg:max-w-[250px] p-2">
                  {Object.keys(value?.value?.pystemmer).length !== 0 && (
                    <p>Pystemmer:</p>
                  )}
                  {value?.value?.pystemmer &&
                    Object.keys(value?.value?.pystemmer).map((item) => {
                      return (
                        <div>
                          <span>{item}:</span>
                          <span>{value?.value?.pystemmer[item]}</span>
                          {/* hello */}
                        </div>
                      );
                    })}
                  {Object.keys(value?.value?.word_split).length !== 0 && (
                    <p>Word_split:</p>
                  )}
                  {value?.value?.word_split &&
                    Object.keys(value?.value?.word_split).map((item) => {
                      return (
                        <div>
                          <span>{item}:</span>
                          <span>{value?.value?.word_split[item]}</span>
                          {/* hello */}
                        </div>
                      );
                    })}
                </td>
                <td className="border-[0.5px] border-opacity-10 border-[#f7fafc] text-center text-xs md:text-sm font-semibold text-white tracking-wider w-[90px] max-w-[90px] md:w-[200px] md:max-w[200px] lg:w-[250px] lg:max-w-[250px] p-2">
                  {value?.value?.optimum &&
                    Object.keys(value?.value?.optimum).map((item) => {
                      return (
                        <div>
                          <span>{item}:</span>
                          <span>{value?.value?.optimum[item]}</span>
                          {/* hello */}
                        </div>
                      );
                    })}
                </td>
                <td className="border-[0.5px] border-opacity-10 border-[#f7fafc] text-center text-xs md:text-sm font-semibold text-white tracking-wider w-[90px] max-w-[90px] md:w-[200px] md:max-w[200px] lg:w-[250px] lg:max-w-[250px] p-2">
                  {value?.value?.result &&
                    Object.keys(value?.value?.result).map((item) => {
                      return (
                        <div>
                          <span>{item}</span>
                        </div>
                      );
                    })}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
