import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

const StatCard = ({ title, value, change, changeType, icon: Icon, color }) => {
  const isPositive = changeType === 'up';
  
  return (
    <div style={styles.card}>
      <div style={styles.header}>
        <div>
          <p style={styles.title}>{title}</p>
          <h2 style={styles.value}>{value}</h2>
        </div>
        <div style={{...styles.iconContainer, background: color}}>
          <Icon size={24} style={styles.icon} />
        </div>
      </div>
      
      <div style={styles.footer}>
        <div style={{...styles.change, color: isPositive ? '#10b981' : '#ef4444'}}>
          {isPositive ? <TrendingUp size={16} /> : <TrendingDown size={16} />}
          <span style={styles.changeText}>{change}</span>
        </div>
        <span style={styles.period}>Since last month</span>
      </div>
    </div>
  );
};

const styles = {
  card: {
    background: 'white',
    borderRadius: '12px',
    padding: '24px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
    transition: 'transform 0.2s, box-shadow 0.2s',
    cursor: 'pointer',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '20px',
  },
  title: {
    fontSize: '14px',
    color: '#999',
    margin: '0 0 8px 0',
    fontWeight: '500',
  },
  value: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#333',
    margin: 0,
  },
  iconContainer: {
    width: '50px',
    height: '50px',
    borderRadius: '12px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  icon: {
    color: 'white',
  },
  footer: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  change: {
    display: 'flex',
    alignItems: 'center',
    gap: '5px',
    fontWeight: '600',
    fontSize: '14px',
  },
  changeText: {
    marginLeft: '4px',
  },
  period: {
    fontSize: '12px',
    color: '#999',
  },
};

export default StatCard;
