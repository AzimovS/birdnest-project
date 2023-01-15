import React from 'react';
import { DataGrid, GridColDef } from '@mui/x-data-grid';
import { Drone } from '../../types';

const columns: GridColDef[] = [
  {
    field: 'serialNumber',
    headerName: 'Serial Number',
    flex: 0.5,
  },
  {
    field: 'distanceFromCentre',
    headerName: 'Distance From Centre',
    flex: 0.5,
  },
  {
    field: 'time',
    headerName: 'Detected at',
    flex: 0.5,
  },
  {
    field: 'name',
    headerName: 'Name',
    flex: 0.5,
  },
  {
    field: 'email',
    headerName: 'Email',
    flex: 0.5,
  },
  {
    field: 'phoneNumber',
    headerName: 'phoneNumber',
    flex: 0.5,
  },
];

type Props = {
  drones: Drone[];
};

const TableData: React.FC<Props> = ({ drones }) => {
  return (
    <DataGrid
      columns={columns}
      rows={drones}
      getRowId={(row: Drone) => row.serialNumber}
    />
  );
};

export default TableData;
