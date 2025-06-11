import React, { useEffect, useState } from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { fetchData } from '../../data/api';

ChartJS.register(ArcElement, Tooltip, Legend);

interface PieChartData {
  labels: string[];
  valores: number[];
}

const PieChart: React.FC = () => {
  const [chartData, setChartData] = useState<PieChartData | null>(null);

  useEffect(() => {
    loadChartData();
  }, []);

  const loadChartData = async () => {
    const data = await fetchData<PieChartData>('performance-geral');
    if (data) {
      setChartData(data);
    }
  };

  if (!chartData) return null;

  const data = {
    labels: chartData.labels,
    datasets: [
      {
        data: chartData.valores,
        backgroundColor: [
          '#6E7E8F',
          '#4DAFAC',
          '#54B399',
          '#E7664C',
          '#906ADA',
        ],
        borderWidth: 0,
      },
    ],
  };
  
  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'right' as const,
        labels: {
          boxWidth: 10,
          padding: 10,
          font: {
            size: 11,
          }
        },
      },
      tooltip: {
        callbacks: {
          label: function(context: any) {
            return `${context.label}: ${context.raw}%`;
          }
        }
      }
    },
    layout: {
      padding: 0
    },
    maintainAspectRatio: true,
  };

  return <Pie data={data} options={options} />;
};

export default PieChart;