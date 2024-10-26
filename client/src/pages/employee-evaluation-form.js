import React from 'react';
import { Card, CardContent, CardHeader, Typography } from '@mui/material';
import { TextField } from '@mui/material';
import { TextareaAutosize } from '@mui/material';
import { Divider } from '@mui/material';
import { RadioGroup, FormControlLabel, Radio } from '@mui/material';
import { Button } from '@mui/material';
import { FormLabel } from '@mui/material';

const RatingOptions = ({ name }) => (
  <RadioGroup className="space-y-2">
    <div className="flex items-center space-x-2">
      <FormControlLabel control={<Radio value="exceeds" id={`${name}-exceeds`} />} label="Exceeds expectations" />
    </div>
    <div className="flex items-center space-x-2">
      <FormControlLabel control={<Radio value="meets" id={`${name}-meets`} />} label="Meets expectations" />
    </div>
    <div className="flex items-center space-x-2">
      <FormControlLabel control={<Radio value="needs" id={`${name}-needs`} />} label="Needs improvement" />
    </div>
    <div className="flex items-center space-x-2">
      <FormControlLabel control={<Radio value="unacceptable" id={`${name}-unacceptable`} />} label="Unacceptable" />
    </div>
  </RadioGroup>
);

const EmployeeEvaluationForm = () => {
  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-4xl mx-auto p-6 space-y-8">
      <Card>
        <CardHeader>
          <Typography variant="h5" className="text-2xl font-bold text-center">
            Employee Evaluation Form
          </Typography>
        </CardHeader>
        <CardContent className="space-y-8">
          {/* Section I: Employee Information */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">I. Employee Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <FormLabel htmlFor="employee-name">Employee Name</FormLabel>
                <TextField id="employee-name" required />
              </div>
              <div className="space-y-2">
                <FormLabel htmlFor="employee-id">Employee ID</FormLabel>
                <TextField id="employee-id" required />
              </div>
              <div className="space-y-2">
                <FormLabel>Supervisor/Reviewer</FormLabel>
                <TextField id="supervisor" required />
              </div>
              <div className="space-y-2">
                <FormLabel>Review Period</FormLabel>
                <div className="flex gap-2">
                  <TextField type="date" className="w-full" required />
                  <TextField type="date" className="w-full" required />
                </div>
              </div>
            </div>
          </div>

          <Divider />

          {/* Section II: Core Values and Objectives */}
          <div className="space-y-6">
            <h2 className="text-xl font-semibold">II. Core Values and Objectives</h2>
            
            <div className="space-y-6">
              <div className="space-y-2">
                <FormLabel>Quality of Work</FormLabel>
                <RatingOptions name="quality" />
              </div>

              <div className="space-y-2">
                <FormLabel>Attendance & Punctuality</FormLabel>
                <RatingOptions name="attendance" />
              </div>

              <div className="space-y-2">
                <FormLabel>Reliability/Dependability</FormLabel>
                <RatingOptions name="reliability" />
              </div>

              <div className="space-y-2">
                <FormLabel>Communication Skills</FormLabel>
                <RatingOptions name="communication" />
              </div>

              <div className="space-y-2">
                <FormLabel>Judgment & Decision-Making</FormLabel>
                <RatingOptions name="judgment" />
              </div>

              <div className="space-y-2">
                <FormLabel>Initiative & Flexibility</FormLabel>
                <RatingOptions name="initiative" />
              </div>

              <div className="space-y-2">
                <FormLabel>Cooperation & Teamwork</FormLabel>
                <RatingOptions name="teamwork" />
              </div>
            </div>
          </div>

          <Divider />

          {/* Section III: Job-Specific Performance Criteria */}
          <div className="space-y-6">
            <h2 className="text-xl font-semibold">III. Job-Specific Performance Criteria</h2>
            
            <div className="space-y-6">
              <div className="space-y-2">
                <FormLabel>Knowledge of Position</FormLabel>
                <RatingOptions name="knowledge" />
              </div>

              <div className="space-y-2">
                <FormLabel>Training & Development</FormLabel>
                <RatingOptions name="training" />
              </div>
            </div>
          </div>

          <Divider />

          {/* Section IV: Performance Goals */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">IV. Performance Goals</h2>
            <TextareaAutosize 
              placeholder="Enter performance goals and objectives for the next review period"
              className="min-h-[100px]"
            />
          </div>

          <Divider />

          {/* Section V: Overall Rating */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">V. Overall Rating</h2>
            <RatingOptions name="overall" />
          </div>

          <Divider />

          {/* Section VI: Employee Comments */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">VI. Employee Comments (Optional)</h2>
            <TextareaAutosize 
              placeholder="Enter any additional comments or feedback"
              className="min-h-[100px]"
            />
          </div>

          <Divider />

          {/* Section VII: Acknowledgement */}
          <div className="space-y-4">
            <h2 className="text-xl font-semibold">VII. Acknowledgement</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <FormLabel>Employee Signature</FormLabel>
                <TextField />
              </div>
              <div className="space-y-2">
                <FormLabel>Date</FormLabel>
                <TextField type="date" />
              </div>
              <div className="space-y-2">
                <FormLabel>Reviewer Signature</FormLabel>
                <TextField />
              </div>
              <div className="space-y-2">
                <FormLabel>Date</FormLabel>
                <TextField type="date" />
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <div className="flex justify-end">
        <Button variant="contained" color="primary" type="submit" className="w-full md:w-auto">
          Submit Evaluation
        </Button>
      </div>
    </form>
  );
};

export default EmployeeEvaluationForm;
