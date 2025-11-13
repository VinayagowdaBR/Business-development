import React from 'react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const ChartCard = ({ title, data, type = 'line' }) => {
  return (
    <div style={styles.container}>
      <h3 style={styles.title}>{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        {type === 'line' ? (
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="name" stroke="#999" fontSize={12} />
            <YAxis stroke="#999" fontSize={12} />
            <Tooltip />
            <Line 
              type="monotone" 
              dataKey="value" 
              stroke="#6366f1" 
              strokeWidth={3}
              dot={{ fill: '#6366f1', r: 4 }}
            />
          </LineChart>
        ) : (
          <AreaChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis dataKey="name" stroke="#999" fontSize={12} />
            <YAxis stroke="#999" fontSize={12} />
            <Tooltip />
            <Area 
              type="monotone" 
              dataKey="value" 
              stroke="#6366f1" 
              fill="url(#colorGradient)"
              strokeWidth={2}
            />
            <defs>
              <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#6366f1" stopOpacity={0.1}/>
              </linearGradient>
            </defs>
          </AreaChart>
        )}
      </ResponsiveContainer>
    </div>
  );
};

const styles = {
  container: {
    background: 'white',
    borderRadius: '12px',
    padding: '24px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
  },
  title: {
    fontSize: '18px',
    fontWeight: '600',
    marginBottom: '20px',
    color: '#333',
  },
};

export default ChartCard;
