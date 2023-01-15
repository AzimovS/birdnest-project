import React from 'react';
import {
  DataGrid,
  GridColDef,
} from '@mui/x-data-grid';
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
      // loading={isLoading}
      // onPageChange={onPageChange}
      // onRowClicked={navigateToInvoice}
      // initialState={{
      //   sorting: {
      //     sortModel: [{ field: 'updatedAt', sort: 'desc' }],
      //   },
      // }}type + row.locale
      // sortingMode='server'
      // onSortModelChange={onSortChange}
      // style={{ height: '631px', width: '100%' }}
    />
  );
};

export default TableData;
