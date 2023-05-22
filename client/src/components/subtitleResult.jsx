import * as React from "react";
import { styled } from "@mui/material/styles";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell, { tableCellClasses } from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
  [`&.${tableCellClasses.body}`]: {
    fontSize: 14,
  },
}));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  "&:nth-of-type(odd)": {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  "&:last-child td, &:last-child th": {
    border: 0,
  },
}));

export default function SubtitleTables(rows) {
  // console.log(rows);
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 700 }} aria-label="customized table">
        <TableHead>
          <TableRow>
            <StyledTableCell>Subtitle ID</StyledTableCell>
            <StyledTableCell align="right">Subtitle Text</StyledTableCell>
            <StyledTableCell align="right">Start Time</StyledTableCell>
            <StyledTableCell align="right">End Time</StyledTableCell>
            <StyledTableCell align="right">Video URL</StyledTableCell>
            <StyledTableCell align="right">Subtitle URL</StyledTableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.rows.map((row) => (
            <StyledTableRow key={row.SubtitleID}>
              <StyledTableCell component="th" scope="row">
                {row.SubtitleID}
              </StyledTableCell>
              <StyledTableCell align="right">{row.subtitle}</StyledTableCell>
              <StyledTableCell align="right">{row.start_time}</StyledTableCell>
              <StyledTableCell align="right">{row.end_time}</StyledTableCell>
              <StyledTableCell align="right">{row.media_path}</StyledTableCell>
              <StyledTableCell align="right">
                {row.subtitle_url}
              </StyledTableCell>
            </StyledTableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
