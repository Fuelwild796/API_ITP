import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { fetchData } from '../../data/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface BarChartData {
  meses: string[];
  negativo: number[];
  positivo: number[];
  neutro: number[];
}

const BarChart: React.FC = () => {
  const [chartData, setChartData] = useState<BarChartData | null>(null);

  useEffect(() => {
    loadChartData();
  }, []);

  const loadChartData = async () => {
    const data = await fetchData<BarChartData>('evolucao-mensal');
    if (data) {
      setChartData(data);
    }
  };

  if (!chartData) return null;

  const data = {
    labels: chartData.meses,
    datasets: [
      {
        label: 'Negativo',
        data: chartData.negativo,
        backgroundColor: '#E7664C',
        barPercentage: 0.8,
      },
      {
        label: 'Positivo',
        data: chartData.positivo,
        backgroundColor: '#54B399',
        barPercentage: 0.8,
      },
      {
        label: 'Neutro',
        data: chartData.neutro,
        backgroundColor: '#BBBBBB',
        barPercentage: 0.8,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    scales: {
      x: {
        stacked: false,
        grid: {
          display: false,
        },
      },
      y: {
        max: 8,
        beginAtZero: true,
        ticks: {
          stepSize: 2,
        },
        grid: {
          color: '#f0f0f0',
        },
      },
    },
    plugins: {
      legend: {
        position: 'bottom' as const,
        labels: {
          boxWidth: 12,
          usePointStyle: true,
          padding: 20,
          font: {
            size: 11,
          }
        },
      },
    },
    layout: {
      padding: {
        left: 0,
        right: 0,
        top: 0,
        bottom: 0,
      },
    },
  };

  return <Bar data={data} options={options} />;
};

export default BarChart;