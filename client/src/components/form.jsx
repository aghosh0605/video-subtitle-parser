import React, { useState } from "react";
import CircularIndeterminate from "./uploading";
import Button from "@mui/material/Button";
import BasicTable from "./fileTable";
import { purple } from "@mui/material/colors";
import { styled } from "@mui/material/styles";
import CloudQueueIcon from "@mui/icons-material/CloudQueue";
import RefreshIcon from "@mui/icons-material/Refresh";
import IconButton from "@mui/material/IconButton";
import { toast } from "react-toastify";

const ColorButton = styled(Button)(({ theme }) => ({
  color: theme.palette.getContrastText(purple[500]),
  backgroundColor: "#4caf50",
  "&:hover": {
    backgroundColor: "#357a38",
  },
}));

const BASE_URL = "https://api.cybersupport.in";

export const FileUpload = (props) => {
  const [selectedFile, setSelectedFile] = useState();
  const [isFilePicked, setIsFilePicked] = useState(false);
  const [isFileSent, setIsFileSent] = useState(true);
  const [data, setData] = useState({});
  const [error, setError] = useState(null);

  const changeHandler = (event) => {
    setSelectedFile(event.target.files[0]);
    setIsFilePicked(true);
  };
  const handleSubmission = async () => {
    try {
      const formData = new FormData();

      formData.append("file", selectedFile);
      formData.append("remark", "File to parse");
      const response = await fetch(`${BASE_URL}/api/v1/upload/file`, {
        method: "POST",
        body: formData,
      });
      const result = await response.json();
      if (!response.ok) {
        throw new Error(
          `This is an HTTP error: The status is ${result.file[0]}`
        );
      }
      setData(result);
      //console.log(result.filename);
      props.setFileName(result.filename);
      //console.log(result.file[0]);
      setIsFileSent(false);
      toast(result.message, {
        position: "top-center",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: "dark",
      });
      setError(null);
    } catch (err) {
      toast(err.message, {
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
    }
  };

  const handleRefresh = async (task_id) => {
    if (task_id) {
      console.log(task_id);
      const res = await fetch(`${BASE_URL}/api/v1/status/file/${task_id}`, {
        method: "PATCH",
      });
      const body = await res.json();
      console.log(body);
      setIsFileSent(body);
    } else {
      setIsFileSent(false);
    }
  };

  return (
    <div>
      <input
        className="border border-gray-300 rounded-md px-4 py-2 w-full"
        type="file"
        name="file"
        onChange={changeHandler}
      />
      {isFilePicked ? (
        <BasicTable rows={[selectedFile]} />
      ) : (
        <p className="text-base font-bold text-purple-600">
          Select a file to show details
        </p>
      )}
      <br />
      <div>
        {!isFileSent && <CircularIndeterminate />}
        <ColorButton
          variant="contained"
          onClick={() => handleSubmission()}
          endIcon={<CloudQueueIcon />}
        >
          Upload Video
        </ColorButton>

        <IconButton color="primary" aria-label="add to shopping cart">
          {data && <RefreshIcon onClick={() => handleRefresh(data.task_id)} />}
        </IconButton>
        {error && <div>{`There is a problem fetching data - ${error}`}</div>}
      </div>
    </div>
  );
};
