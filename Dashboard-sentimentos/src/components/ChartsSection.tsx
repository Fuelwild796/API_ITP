import React from 'react';
import PieChart from './charts/PieChart';
import BarChart from './charts/BarChart';

const ChartsSection: React.FC = () => {
  return (
    <div className="flex flex-wrap gap-5 justify-between h-full">
      <div className="bg-white rounded-lg shadow-sm p-5 flex-1 min-w-[280px] lg:flex-[0_0_30%] h-full">
        <PieChart />
      </div>
      <div className="bg-white rounded-lg shadow-sm p-5 flex-1 min-w-[400px] lg:flex-[0_0_calc(70%-20px)] h-full">
        <BarChart />
      </div>
    </div>
  );
};

export default ChartsSection;