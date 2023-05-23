import * as React from "react";
import PropTypes from "prop-types";
import LinearProgress from "@mui/material/LinearProgress";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import SettingsIcon from "@mui/icons-material/Settings";
import RefreshIcon from "@mui/icons-material/Refresh";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import { toast } from "react-toastify";

const BASE_URL = "https://api.cybersupport.in";

function LinearProgressWithLabel(props) {
  return (
    <Box sx={{ display: "flex", alignItems: "center" }}>
      <Box sx={{ width: "100%", mr: 1 }}>
        <LinearProgress variant="determinate" {...props} />
      </Box>
      <Box sx={{ minWidth: 35 }}>
        <Typography variant="body2" color="text.secondary">{`${Math.round(
          props.value
        )}%`}</Typography>
      </Box>
    </Box>
  );
}

LinearProgressWithLabel.propTypes = {
  /**
   * The value of the progress indicator for the determinate and buffer variants.
   * Value between 0 and 100.
   */
  value: PropTypes.number.isRequired,
};

export default function LinearWithValueLabel(props) {
  const [progress, setProgress] = React.useState(10);
  const [result, setResult] = React.useState({});
  const [error, setError] = React.useState(null);

  const handleParse = async () => {
    try {
      //console.log(typeof props.fileName);
      if (!props.fileName) {
        toast("Please provide a file name", {
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
      const res = await fetch(
        `${BASE_URL}/api/v1/parse?file=${props.fileName}`
      );
      const data = await res.json();
      if (!res.ok) {
        throw new Error(`This is an HTTP error: The status is ${res.status}`);
      }
      console.log(data.task_id);
      setResult(data);
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
      setResult(null);
    }
  };

  const handleUpdate = async (task) => {
    if (result.task_id) {
      const res = await fetch(`${BASE_URL}/progress-track/${task.task_id}`);
      const body = await res.json();
      //console.log(body);
      console.log(body.progress.percent);
      setProgress(body.progress.percent);
    } else {
      setProgress(0);
    }
  };

  return (
    <div>
      <Box sx={{ width: "100%" }}>
        <LinearProgressWithLabel value={progress} />
      </Box>
      <Button
        variant="contained"
        endIcon={<SettingsIcon />}
        onClick={handleParse}
      >
        Parse Video
      </Button>
      <IconButton
        color="primary"
        aria-label="add to shopping cart"
        onClick={() => handleUpdate(result)}
      >
        <RefreshIcon />
      </IconButton>
    </div>
  );
}
