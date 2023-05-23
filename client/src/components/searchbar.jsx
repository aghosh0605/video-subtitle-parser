import React, { useState } from "react";
import IconButton from "@mui/material/IconButton";
import SearchIcon from "@mui/icons-material/Search";
import SubtitleTables from "./subtitleResult";
import { toast } from "react-toastify";

const BASE_URL = "https://api.cybersupport.in";

const Search = ({ details }) => {
  const [searchField, setSearchField] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const getData = async () => {
    try {
      if (!searchField) {
        toast("Please Provide a query to search", {
          position: "top-center",
          autoClose: 5000,
          hideProgressBar: false,
          closeOnClick: true,
          pauseOnHover: true,
          draggable: true,
          progress: undefined,
          theme: "dark",
        });
      }
      const response = await fetch(
        `${BASE_URL}/api/v1/subtitle/find?query=${searchField}`
      );
      if (!response.ok) {
        throw new Error(
          `This is an HTTP error: The status is ${response.status}`
        );
      }
      let actualData = await response.json();
      setData(actualData.Items);
      setError(null);
    } catch (err) {
      toast(err, {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "dark",
      });
      setError(err.message);
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setSearchField(e.target.value);
  };

  const handleForm = (event) => {
    event.preventDefault();
    getData();
  };

  return (
    <div>
      <br />
      <form className="flex items-center border border-gray-300 rounded-md px-2 py-1">
        <input
          className="border border-gray-300 rounded-l-md px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-400"
          type="search"
          placeholder="Search Subtitles"
          onChange={handleChange}
        />
        <IconButton color="primary" aria-label="add to shopping cart">
          <SearchIcon onClick={handleForm} />
        </IconButton>
      </form>
      <br />
      <h3 className="text-2xl font-medium text-red-500 font-mono">
        Subtitle Results
      </h3>
      {loading && (
        <div className="text-base font-bold text-purple-600">
          A moment please...
        </div>
      )}
      {error && (
        <div>{`There is a problem fetching the post data - ${error}`}</div>
      )}
      <ul>{data && <SubtitleTables rows={data} />}</ul>
    </div>
  );
};

export default Search;
