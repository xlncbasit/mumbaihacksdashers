// client/src/pages/task-completion.js

import React, { useState } from 'react';
import axios from 'axios';

function TaskCompletion() {
    const [employeeId, setEmployeeId] = useState('');
    const [completedStatus, setCompletedStatus] = useState('');
    const [timeTaken, setTimeTaken] = useState('');
    const [taskQualityScore, setTaskQualityScore] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:5000/task-complete', {
                input: {
                    EmployeeId: employeeId,
                    Completed: completedStatus,
                    Time_taken: timeTaken,
                    task_quality_score: taskQualityScore
                }
            });
            console.log('Response:', response.data);
        } catch (error) {
            console.error('Error marking task as completed:', error);
        }
    };

    return (
        <div>
            <h1>Mark Task as Completed</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Employee ID:
                    <input 
                        type="text" 
                        value={employeeId} 
                        onChange={(e) => setEmployeeId(e.target.value)} 
                    />
                </label>
                <label>
                    Completed Status:
                    <input 
                        type="text" 
                        value={completedStatus} 
                        onChange={(e) => setCompletedStatus(e.target.value)} 
                    />
                </label>
                <label>
                    Time Taken For Task:
                    <input 
                        type="text" 
                        value={timeTaken} 
                        onChange={(e) => setTimeTaken(e.target.value)} 
                    />
                </label>
                <label>
                    Task Quality Score:
                    <input 
                        type="text" 
                        value={taskQualityScore} 
                        onChange={(e) => setTaskQualityScore(e.target.value)} 
                    />
                </label>
                <button type="submit">Mark as Completed</button>
            </form>
        </div>
    );
}

export default TaskCompletion;

