import React, { useState, useEffect } from 'react'
import axios from "axios"
import Papa from 'papaparse'; 

const Predict = () => {
    const [prediction, setPrediction] = useState("")
    const [answer, setAnswer] = useState("")
    const [employeesAtRisk, setEmployeesAtRisk] = useState([]); // State for employees at risk

    // Function to fetch and parse CSV data
    const fetchEmployeeData = () => {
        Papa.parse('/path/to/your/employee_data.csv', { // Update with your CSV file path
            download: true,
            header: true,
            complete: (results) => {
                const atRiskEmployees = results.data.filter(employee => employee.burnoutRisk === 'high'); // Adjust condition as needed
                setEmployeesAtRisk(atRiskEmployees.map(emp => emp.id)); // Assuming 'id' is the employee ID field
            }
        });
    };

    useEffect(() => {
        fetchEmployeeData(); // Fetch employee data on component mount
    }, []);

    const handleChange = (event) => {
        setPrediction(event.target.value);
    };

    console.log(prediction)
    const handleClick= async (e) => {
        console.log(prediction);
        try {
            const response = await axios.post('http://127.0.0.1:5000/process',{
                input: prediction,
            },{
                headers: {
                  "Content-Type": "application/json",
                  "Access-Control-Allow-Origin": "*",
                },
              })
            console.log(response.data)
            setAnswer(response.data.final_prediction)
        }
        
         catch (error) {
            console.log(error)
        }
    }

    return (
        <div>
            <h1>Employees at Risk of Burnout</h1>
            <ul>
                {employeesAtRisk.map(id => (
                    <li key={id}>{id}</li> // Displaying employee IDs
                ))}
            </ul>
        </div>
    )
}

export default Predict
