import { FC } from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <div className="py-4 bg-white shadow-lg font-karla">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center flex-wrap gap-4">
          <Link
            to="/"
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            Employee Evaluation Form
          </Link>
          
          <Link
            to="/task-assignment"
            className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
          >
            Task Assign
          </Link>
          
          <Link
            to="/task-completion"
            className="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors"
          >
            Task Completion Form
          </Link>
          
          <Link
            to="/predict"
            className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
          >
            Predict Burn Out
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Navbar;