import React, { useEffect, useState } from 'react'
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import {Grid, Box, Paper,styled } from '@mui/material'
import { Pie } from 'react-chartjs-2';



/* A styled component. */
const Item = styled(Paper)(({ theme }) => ({
    backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
    ...theme.typography.body2,
    padding: theme.spacing(1),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  }));
  
function SalaryStats() {
    const [data, setData] = useState([]);
    const [dataTwo, setDataTwo] = useState([]);
    const [dataAge, setDataAge] = useState([]);
    const [dataEd, setDataEd] = useState([]);

/* A hook that is called when the component is mounted. It is used to fetch data from the backend. */
    useEffect(()=>{
        axios.get('http://localhost:8080/salarystats')
        .then(res => {
            setData(res.data.data)
            setDataTwo(res.data.data2)
            setDataAge(res.data.age)
            setDataEd(res.data.ed_level)
        })
        .catch(err => console.log(err))
    },[])
    

    // console.log(pie_labels)

    const dataOne = {
        labels: data.map(x=>x.country),
        datasets: [
          {
            label: '# Votes',
            data: data.map(x=>x.counts),
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
              ],
              borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
              ],
            borderWidth: 1.2,
          },
        ],
      };

    return (
        <div style={{
            position: 'absolute', left: '50%', top: '50%',
            transform: 'translate(-50%, -12%)'}}>
            <Paper>

            <Box sx={{ flexGrow: 1, overflow: 'hidden', px: 6 } }>
                <Grid container direction="column" alignItems="stretch" justifyContent="space-between" spacing={12}>
                <Grid sx={{ m: 2 }} item style = {{minWidth: "900px"}}  xs={12}>
                <Pie data={dataOne} />
                </Grid>

                <Grid item style = {{minWidth: "900px"}}  xs={12}>
                <ResponsiveContainer height={600} width="100%">
                    <BarChart
                    width={1000}
                    height={700}
                    data={dataTwo}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                    }}
                    >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="country" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="salary" fill="#8884d8" />
                    </BarChart>
                    </ResponsiveContainer>
                </Grid>

                <Grid item style = {{minWidth: "900px"}}  xs={12}>
                <ResponsiveContainer height={600} width="100%">
                    <BarChart
                    width={1000}
                    height={700}
                    data={dataAge}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                    }}
                    >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="age" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="count" fill="#8884d8" />
                    </BarChart>
                    </ResponsiveContainer>
                </Grid>

                <Grid item style = {{minWidth: "900px"}}  xs={12}>
                <ResponsiveContainer height={600} width="100%">
                    <BarChart
                    width={1000}
                    height={700}
                    data={dataEd}
                    margin={{
                        top: 5,
                        right: 30,
                        left: 20,
                        bottom: 5,
                    }}
                    >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="ed" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="count" fill="#8884d8" />
                    </BarChart>
                    </ResponsiveContainer>
                </Grid>

                
                </Grid>
            </Box>
            </Paper>
        </div>
    );

}

export default SalaryStats;
