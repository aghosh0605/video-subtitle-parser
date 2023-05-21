import React, { useState } from "react";

const BASE_URL = "http://127.0.0.1:8000";

const Search = ({ details }) => {
  const [searchField, setSearchField] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const getData = async () => {
    try {
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
      console.log(actualData.Items);
      setError(null);
    } catch (err) {
      setError(err.message);
      setData(null);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setSearchField(e.target.value);
    // getData();
  };

  const handleForm = (event) => {
    event.preventDefault();
    getData();
  };

  return (
    <div>
      <form onSubmit={handleForm}>
        <input
          className="pa3 bb br3 grow b--none bg-lightest-blue ma3"
          type="search"
          placeholder="Search People"
          onChange={handleChange}
        />
        <button type="submit">Search </button>
      </form>
      <h1>API Posts</h1>
      {loading && <div>A moment please...</div>}
      {error && (
        <div>{`There is a problem fetching the post data - ${error}`}</div>
      )}
      <ul>
        {data &&
          data.map((item, index) => (
            <li
              key={index}
              style={{ textAlign: "left", fontSize: "12px", fontWeight: "400" }}
            >
              <h3>{item.subtitle_url}</h3>
            </li>
          ))}
      </ul>
    </div>
  );
};

export default Search;
