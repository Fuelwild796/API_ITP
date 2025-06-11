// Mock data for attendants
export const attendantsData = [
  { name: 'Henrique', score: 32 },
  { name: 'Gabriela', score: 24 },
  { name: 'Eduarda', score: 15 },
  { name: 'Ana', score: 9 },
  { name: 'Felipe', score: 0 },
  { name: 'Carla', score: -8 },
  { name: 'Bruno', score: -19 },
  { name: 'Daniel', score: -25 },
  { name: 'Luciana', score: 18 },
  { name: 'Paulo', score: 5 },
  { name: 'Marina', score: -12 },
  { name: 'Ricardo', score: 7 },
];

// Mock data for clients with 96 total records
export const clientsData = [
  { name: 'Felipe', score: 20 },
  { name: 'Thiago', score: 20 },
  { name: 'Henrique', score: 20 },
  { name: 'Luz', score: 10 },
  { name: 'Cecília', score: 10 },
  { name: 'Bruna', score: 10 },
  { name: 'Jorge', score: 10 },
  { name: 'Letícia', score: 10 },
  { name: 'Lucas', score: 10 },
  { name: 'Carolina', score: 10 },
  // Generate additional clients to reach 96 total
  ...Array.from({ length: 86 }, (_, i) => {
    const names = ['João', 'Maria', 'Carlos', 'Sandra', 'Pedro', 'Amanda', 'Roberto', 'Fernanda'];
    const scores = [5, 10, 15, 20, 25];
    
    return {
      name: `${names[i % names.length]} ${Math.floor(i / names.length) + 1}`,
      score: scores[i % scores.length]
    };
  })
];