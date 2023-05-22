import React, { useState } from "react";
import CircularIndeterminate from "./uploading";
import Button from "@mui/material/Button";

const BASE_URL = "http://127.0.0.1:8000";

export const FileUpload = () => {
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
        <div>
          <p>Filename: {selectedFile.name}</p>
          <p>Filetype: {selectedFile.type}</p>
          <p>Size in bytes: {selectedFile.size}</p>
          <p>
            lastModifiedDate:{" "}
            {selectedFile.lastModifiedDate.toLocaleDateString()}
          </p>
        </div>
      ) : (
        <p>Select a file to show details</p>
      )}
      <div>
        <Button variant="contained" onClick={handleSubmission}>
          Upload File
        </Button>
        {isFileSent && <CircularIndeterminate />}
      </div>
    </div>
  );
};
