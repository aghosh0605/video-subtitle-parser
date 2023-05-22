import React, { useState } from "react";
import CircularIndeterminate from "./uploading";
import Button from "@mui/material/Button";
import BasicTable from "./fileTable";
import { purple } from "@mui/material/colors";
import { styled } from "@mui/material/styles";
import CloudQueueIcon from "@mui/icons-material/CloudQueue";
import RefreshIcon from "@mui/icons-material/Refresh";
import IconButton from "@mui/material/IconButton";

const ColorButton = styled(Button)(({ theme }) => ({
  color: theme.palette.getContrastText(purple[500]),
  backgroundColor: "#4caf50",
  "&:hover": {
    backgroundColor: "#357a38",
  },
}));

const BASE_URL = "http://127.0.0.1:8000";

export const FileUpload = (props) => {
  const [selectedFile, setSelectedFile] = useState();
  const [isFilePicked, setIsFilePicked] = useState(false);
  const [isFileSent, setIsFileSent] = useState(false);

  const changeHandler = (event) => {
    setSelectedFile(event.target.files[0]);
    setIsFilePicked(true);
  };

  const handleSubmission = async () => {
    const formData = new FormData();

    formData.append("file", selectedFile);
    formData.append("remark", "File to parse");

    await fetch(`${BASE_URL}/api/v1/upload/file`, {
      method: "POST",
      body: formData,
    })
      .then(async (response) => response.json())
      .then(async (result) => {
        console.log(result.filename);
        props.setFileName(result.filename);
        console.log("Success:", result);
        const res = await fetch(
          `${BASE_URL}/api/v1/status/file/${result.task_id},`,
          { method: "PATCH" }
        );
        setIsFileSent(res);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
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
        <p>Select a file to show details</p>
      )}
      <br />
      <div>
        {isFileSent && <CircularIndeterminate />}
        <ColorButton
          variant="contained"
          onClick={handleSubmission}
          endIcon={<CloudQueueIcon />}
        >
          Upload Video
        </ColorButton>
        <IconButton color="primary" aria-label="add to shopping cart">
          <RefreshIcon />
        </IconButton>
      </div>
    </div>
  );
};
