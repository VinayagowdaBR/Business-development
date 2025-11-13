import React from 'react';
import { User, CheckCircle, AlertCircle, Info } from 'lucide-react';

const ActivityFeed = ({ activities }) => {
  const getIcon = (type) => {
    switch(type) {
      case 'success': return <CheckCircle size={20} color="#10b981" />;
      case 'warning': return <AlertCircle size={20} color="#f59e0b" />;
      case 'info': return <Info size={20} color="#3b82f6" />;
      default: return <User size={20} color="#6366f1" />;
    }
  };

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Activity Feed</h3>
      <div style={styles.feed}>
        {activities.map((activity, index) => (
          <div key={index} style={styles.item}>
            <div style={styles.iconContainer}>
              {getIcon(activity.type)}
            </div>
            <div style={styles.content}>
              <p style={styles.action}>{activity.action}</p>
              <p style={styles.time}>{activity.time}</p>
              {activity.description && (
                <p style={styles.description}>{activity.description}</p>
              )}
            </div>
          </div>
        ))}
      </div>
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
  feed: {
    maxHeight: '400px',
    overflowY: 'auto',
  },
  item: {
    display: 'flex',
    gap: '15px',
    padding: '15px 0',
    borderBottom: '1px solid #f0f0f0',
  },
  iconContainer: {
    width: '40px',
    height: '40px',
    borderRadius: '50%',
    background: '#f5f5f5',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    flexShrink: 0,
  },
  content: {
    flex: 1,
  },
  action: {
    fontSize: '14px',
    fontWeight: '500',
    color: '#333',
    margin: '0 0 4px 0',
  },
  time: {
    fontSize: '12px',
    color: '#999',
    margin: '0 0 4px 0',
  },
  description: {
    fontSize: '13px',
    color: '#666',
    margin: 0,
  },
};

export default ActivityFeed;
