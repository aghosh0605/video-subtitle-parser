import * as React from "react";
import PropTypes from "prop-types";
import LinearProgress from "@mui/material/LinearProgress";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import SettingsIcon from "@mui/icons-material/Settings";
import RefreshIcon from "@mui/icons-material/Refresh";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";

const BASE_URL = "http://127.0.0.1:8000";
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

  const handleParse = async () => {
    console.log(typeof props.fileName);
    const res = await fetch(`${BASE_URL}/api/v1/parse?file=${props.fileName}`);
    const data = await res.json();
    console.log(data.task_id);
    setResult(data);
  };

  const handleUpdate = async (task) => {
    if (result.task_id) {
      const res = await fetch(`${BASE_URL}/progress-track/${task.task_id}`);
      const body = await res.json();
      console.log(body);
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
