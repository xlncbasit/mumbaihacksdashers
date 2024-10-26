// client/src/pages/task-assignment.js

import React, { useState } from 'react';
import axios from 'axios';

function TaskAssignment() {
    const [employeeId, setEmployeeId] = useState('');
    const [task, setTask] = useState('');
    const [managerId, setManagerId] = useState(''); // New state for ManagerId

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:5000/task-assign', {
                EmployeeId: employeeId,
                Task: task,
                ManagerId: managerId // Include ManagerId in the request
            });
            console.log(response.data);
        } catch (error) {
            console.error('Error creating task:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Employee ID"
                value={employeeId}
                onChange={(e) => setEmployeeId(e.target.value)}
                required
            />
            <input
                type="text"
                placeholder="Task"
                value={task}
                onChange={(e) => setTask(e.target.value)}
                required
            />
            <input
                type="text"
                placeholder="Manager ID" // New input for ManagerId
                value={managerId}
                onChange={(e) => setManagerId(e.target.value)}
                required
            />
            <button type="submit">Assign Task</button>
        </form>
    );
}


export default TaskAssignment;