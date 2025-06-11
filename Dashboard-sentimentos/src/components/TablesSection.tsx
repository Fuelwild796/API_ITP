import React from 'react';
import AttendantsTable from './tables/AttendantsTable';
import ClientsTable from './tables/ClientsTable';

const TablesSection: React.FC = () => {
  return (
    <div className="flex flex-wrap gap-5 justify-between h-full">
      <AttendantsTable />
      <ClientsTable />
    </div>
  );
};

export default TablesSection;