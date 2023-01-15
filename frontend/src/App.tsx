import React, { useState, useEffect } from 'react';
import TableData from './components/tableData/TableData';
import CssBaseline from '@mui/material/CssBaseline';
import { getDrones } from './services/drones';
import { Drone } from './types';
import {
  Box,
  Container,
  createTheme,
  Grid,
  Paper,
  ThemeProvider,
  Toolbar,
} from '@mui/material';
import { format } from 'date-fns';

const mdTheme = createTheme();

function App() {
  const [drones, setDrones] = useState<Drone[]>([]);
  const [time, setTime] = useState(Date.now());

  useEffect(() => {
    const interval = setInterval(() => {
      setTime(Date.now());

      getDrones().then((res) => {
        setDrones(res);
        console.log(res);
      });
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <ThemeProvider theme={mdTheme}>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        <Box
          component='main'
          sx={{
            backgroundColor: (theme) =>
              theme.palette.mode === 'light'
                ? theme.palette.grey[100]
                : theme.palette.grey[900],
            flexGrow: 1,
            height: '100vh',
            overflow: 'auto',
          }}
        >
          <Toolbar />
          <Container maxWidth='lg' sx={{ mt: 4, mb: 4 }}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Paper
                  sx={{
                    p: 2,
                    display: 'flex',
                    flexDirection: 'column',
                    height: 800,
                  }}
                >
                  <h3>Pilots who recently violated the NDZ perimeter.</h3>
                  <p>
                    The last updated at {format(time, 'dd.MM.yyyy HH:mm:ss')}.
                    Updates every 5 seconds
                  </p>
                  <TableData drones={drones} />
                </Paper>
              </Grid>
            </Grid>
          </Container>
        </Box>
      </Box>
    </ThemeProvider>
  );
}

export default App;
