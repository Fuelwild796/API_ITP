import React, { useState, useEffect } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { fetchData } from '../../data/api';

interface Client {
  nome: string;
  score: number;
}

interface ClientsResponse {
  items: Client[];
  total: number;
}

const ClientsTable: React.FC = () => {
  const [currentPage, setCurrentPage] = useState(1);
  const [clients, setClients] = useState<Client[]>([]);
  const [total, setTotal] = useState(0);
  const itemsPerPage = 10;
  
  useEffect(() => {
    loadClients();
  }, [currentPage]);

  const loadClients = async () => {
    const data = await fetchData<ClientsResponse>(`clientes?page=${currentPage}&limit=${itemsPerPage}`);
    if (data) {
      setClients(data.items);
      setTotal(data.total);
    }
  };
  
  const totalPages = Math.ceil(total / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = Math.min(startIndex + itemsPerPage, total);
  
  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };
  
  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm p-5 flex-1 min-w-[300px] lg:flex-[0_0_calc(50%-10px)] h-full flex flex-col">
      <h2 className="text-base font-medium text-gray-800 pb-3 border-b border-gray-100 mb-4">
        Nome do Cliente 
        <span className="float-right font-normal text-sm">Score do Cliente</span>
      </h2>
      
      <div className="flex-1 overflow-auto">
        <table className="w-full text-sm">
          <tbody>
            {clients.map((item, index) => (
              <tr key={index} className="border-b border-gray-100 last:border-b-0">
                <td className="py-2 text-gray-700">
                  {index + 1}. {item.nome}
                </td>
                <td className="py-2 text-right font-medium text-gray-700">
                  {item.score}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      <div className="flex items-center justify-center mt-4 text-sm text-gray-600">
        <button 
          onClick={handlePrevPage}
          disabled={currentPage === 1}
          className="bg-blue-500 text-white px-3 py-1 rounded disabled:bg-gray-300 mr-2"
        >
          <ChevronLeft size={16} />
        </button>
        <span className="mx-2">
          {startIndex + 1} - {endIndex} / {total}
        </span>
        <button 
          onClick={handleNextPage}
          disabled={currentPage >= totalPages}
          className="bg-blue-500 text-white px-3 py-1 rounded disabled:bg-gray-300 ml-2"
        >
          <ChevronRight size={16} />
        </button>
      </div>
    </div>
  );
};

export default ClientsTable;