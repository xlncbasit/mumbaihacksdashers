import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import EmployeeEvaluationForm from './pages/employee-evaluation-form';
import TaskCompletion from './pages/task-completion';
import TaskAssignment from './pages/task-assignment';
import Predict from './pages/predict';
import Navbar from './components/navbar.js';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<EmployeeEvaluationForm />} />
          <Route path="/task-completion" element={<TaskCompletion />} />
          <Route path="/task-assignment" element={<TaskAssignment />} />
          <Route path="/predict" element={<Predict />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
