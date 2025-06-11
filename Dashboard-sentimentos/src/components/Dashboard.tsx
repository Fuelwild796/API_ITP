import React from 'react';
import TablesSection from './TablesSection';
import ChartsSection from './ChartsSection';

const Dashboard: React.FC = () => {
  return (
    <div className="container mx-auto p-5 h-full flex flex-col">
      <div className="flex-1 min-h-0">
        <TablesSection />
      </div>
      <div className="mt-5 flex-1 min-h-0">
        <ChartsSection />
      </div>
    </div>
  );
};

export default Dashboard;